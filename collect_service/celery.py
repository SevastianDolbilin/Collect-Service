import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collect_service.settings")

app = Celery("collect_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
