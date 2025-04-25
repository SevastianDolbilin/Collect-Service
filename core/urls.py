from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import CollectViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r"collects", CollectViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
