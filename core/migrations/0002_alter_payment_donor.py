# Generated by Django 4.2.20 on 2025-04-24 16:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='donor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Жертвователь'),
        ),
    ]
