from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from collect_service.constants import TIME_NUMBER_ONE, TIME_NUMBER_TWO

from .models import Collect, Payment
from .permissions import Anonymous, Administrator, Author
from .serializers import CollectSerializer, PaymentSerializer
from .tasks import send_notify_email_task


COLLECTS_CACHE_KEY = "collects_list_cache"
COLLECTS_CACHE_TTL = TIME_NUMBER_ONE * TIME_NUMBER_TWO


class CollectViewSet(viewsets.ModelViewSet):
    """Денежный сбор."""

    queryset = Collect.objects.all().select_related("author")
    serializer_class = CollectSerializer

    def get_permissions(self):
        """Получение разрешения в зависимости от типа запроса."""
        if self.request.method in ["POST"]:
            permission_classes = [IsAuthenticated]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [Author, Administrator]
        else:
            permission_classes = [Anonymous]
        return [permission() for permission in permission_classes]

    def clear_collects_cache(self):
        cache.delete(COLLECTS_CACHE_KEY)

    def perform_create(self, serializer):
        collect = serializer.save(author=self.request.user)
        self.clear_collects_cache()

        send_notify_email_task.delay(
            subject="Сбор успешно создан!",
            message=(
                f"Вы создали сбор '{collect.title}'"
                f"на сумму {collect.goal_amount}₽."
            ),
            recipient=self.request.user.email,
        )

    def perform_update(self, serializer):
        serializer.save()
        self.clear_collects_cache()

    def perform_destroy(self, instance):
        instance.delete()
        self.clear_collects_cache()

    def list(self, request, *args, **kwargs):
        cached_response = cache.get(COLLECTS_CACHE_KEY)
        if cached_response:
            return Response(cached_response)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)
        response_data = self.get_paginated_response(
            serializer.data
        ) if page else Response(serializer.data)

        cache.set(COLLECTS_CACHE_KEY, response_data.data, COLLECTS_CACHE_TTL)
        return response_data


class PaymentViewSet(viewsets.ModelViewSet):
    """Платеж."""

    queryset = Payment.objects.all().select_related("collect", "donor")
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        payment = serializer.save(donor=self.request.user)

        cache.delete(COLLECTS_CACHE_KEY)

        send_notify_email_task.delay()(
            subject="Спасибо за пожертвование!",
            message=(
                f"Вы отправили {payment.amount}₽"
                f" в сбор '{payment.collect.title}'.\n"
                f"Дата: {payment.created_at.strftime('%Y-%m-%d %H:%M')}"
            ),
            recipient=self.request.user.email,
        )
