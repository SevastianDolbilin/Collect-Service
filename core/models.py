from django.contrib.auth import get_user_model
from django.db import models

from collect_service.constants import (DECIMAL_COUNT, DEFAULT_NUMBER_ONE,
                                       DEFAULT_NUMBER_TWO, DIGITS_COUNT,
                                       TEXT_LENGTH_FIRST, TEXT_LENGTH_SECOND)

User = get_user_model()


class Occasion(models.TextChoices):
    """Перечисление возможных поводов для создания сбора."""
    BIRTHDAY = "birthday", "День рождения"
    WEDDING = "wedding", "Свадьба"
    FUNERAL = "funeral", "Похороны"
    OTHER = "other", "Другое"


class Collect(models.Model):
    """Модель группового денежного сбора"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="collects",
        verbose_name="Автор"
    )
    title = models.CharField(
        max_length=TEXT_LENGTH_FIRST, verbose_name="Название"
    )
    occasion = models.CharField(
        max_length=TEXT_LENGTH_SECOND,
        choices=Occasion.choices,
        verbose_name="Повод для сбора"
    )
    description = models.TextField(verbose_name="Описание")
    goal_amount = models.DecimalField(
        max_digits=DIGITS_COUNT,
        decimal_places=DECIMAL_COUNT,
        null=True,
        blank=True,
        verbose_name="Целевая сумма"
    )
    collected_amount = models.DecimalField(
        max_digits=DIGITS_COUNT,
        decimal_places=DECIMAL_COUNT,
        default=DEFAULT_NUMBER_TWO,
        verbose_name="Собранная сумма"
        )
    contributors_count = models.PositiveIntegerField(
        default=DEFAULT_NUMBER_ONE,
        verbose_name="Количество донатеров"
    )
    cover_image = models.ImageField(
        upload_to="collect_covers/",
        blank=True,
        null=True,
        verbose_name="Обложка сбора"
    )
    deadline = models.DateTimeField(
        verbose_name="Дата и время окончания сбора"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания сбора"
    )

    def __str__(self) -> str:
        return self.title


class Payment(models.Model):
    """Модель платежа"""
    collect = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Сбор"
    )
    donor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Жертвователь"
    )
    full_name = models.CharField(
        max_length=TEXT_LENGTH_FIRST,
        verbose_name="Имя и фамилия пользователя"
    )
    amount = models.DecimalField(
        max_digits=DIGITS_COUNT,
        decimal_places=DECIMAL_COUNT,
        verbose_name="Сумма"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания платежа"
        )

    def __str__(self):
        return f"{self.full_name} → {self.collect.title} : {self.amount} ₽"
