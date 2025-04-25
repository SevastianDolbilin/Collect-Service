from rest_framework import serializers

from .models import Collect, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежа."""
    class Meta:
        model = Payment
        fields = [
            "id", "collect", "donor", "full_name", "amount", "created_at"
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        payment = super().create(validated_data)
        collect = payment.collect
        collect.collected_amount += payment.amount
        collect.contributors_count = collect.payments.count()
        collect.save(update_fields=["collected_amount", "contributors_count"])
        return payment


class CollectSerializer(serializers.ModelSerializer):
    """Сериализатор группового денежного сбора."""
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Collect
        fields = [
            "id",
            "author",
            "title",
            "occasion",
            "description",
            "goal_amount",
            "collected_amount",
            "contributors_count",
            "cover_image",
            "deadline",
            "created_at",
            "payments",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "collected_amount",
            "contributors_count",
            "payments",
        ]
