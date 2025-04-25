from django.contrib.auth.models import User as DjoserUser
from rest_framework import serializers
from rest_framework.validators import ValidationError

from collect_service.constants import NAME_LENGTH, REGISTRATION_NAME


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Кастомный сериалайзер объекта User."""
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(max_length=NAME_LENGTH, required=True)
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$",
        max_length=REGISTRATION_NAME,
        required=True,
        error_messages={
            "invalid": (
                "Имя пользователя может содержать только"
                "буквы, цифры и символы @/./+/-/_"
            ),
            "max_length": "Длина этого поля не должна превышать 150 символов.",
        },
    )
    first_name = serializers.CharField(
        max_length=REGISTRATION_NAME, required=True
    )
    last_name = serializers.CharField(
        max_length=REGISTRATION_NAME, required=True
    )

    class Meta:
        model = DjoserUser
        fields = [
            "id", "username", "email", "first_name", "last_name", "password"
        ]

    def validate_email(self, value):
        """Валидация почты."""
        if DjoserUser.objects.filter(email=value).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return value

    def validate_username(self, value):
        """Валидация имение пользователя."""
        if DjoserUser.objects.filter(username=value).exists():
            raise ValidationError(
                "Пользователь с таким username уже существует."
            )
        return value

    def create(self, validated_data):
        """Создание пользователя."""
        user = DjoserUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user
