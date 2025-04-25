from celery import shared_task

from .utils.email import send_notify_email


@shared_task
def send_notify_email_task(subject, message, recipient):
    send_notify_email(subject, message, recipient)
