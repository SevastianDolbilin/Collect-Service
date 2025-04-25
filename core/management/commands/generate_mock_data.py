from random import choice, randint

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from core.models import Collect, Payment, User

fake = Faker()


class Command(BaseCommand):
    help = "Генерирует тестовые данные для пользователей, сборов и платежей"

    def handle(self, *args, **kwargs):
        users_to_create = []
        for i in range(1100):
            user = User(
                username=f"{fake.user_name()}_{i}",
                email=fake.email(),
                password=fake.password(),
            )
            users_to_create.append(user)

        with transaction.atomic():
            User.objects.bulk_create(users_to_create)
            self.stdout.write(
                self.style.SUCCESS("Пользователи успешно созданы!")
            )

        users = User.objects.all()

        collects_to_create = []
        for _ in range(1000):
            collect = Collect(
                title=fake.sentence(),
                goal_amount=randint(1000, 50000),
                author=choice(users),
                deadline=fake.date_this_year(),
            )
            collects_to_create.append(collect)

        with transaction.atomic():
            Collect.objects.bulk_create(collects_to_create)
            self.stdout.write(self.style.SUCCESS("Сборы успешно созданы!"))

        collects = Collect.objects.all()

        payments_to_create = []
        for collect in collects:
            for _ in range(randint(1, 100)):
                payment = Payment(
                    amount=randint(100, 10000),
                    collect=collect,
                    donor=choice(users)
                )
                payments_to_create.append(payment)

        with transaction.atomic():
            Payment.objects.bulk_create(payments_to_create)
            self.stdout.write(self.style.SUCCESS("Платежи успешно созданы!"))

        for collect in collects:
            collect.collected_amount = sum(
                payment.amount for payment in collect.payments.all()
            )
            collect.contributors_count = (
                collect.payments.values("donor").distinct().count()
            )
            collect.save()

        self.stdout.write(
            self.style.SUCCESS("Мок-данные успешно сгенерированы!")
        )
