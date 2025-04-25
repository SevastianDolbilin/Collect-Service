from django.core.mail import send_mail


def send_notify_email(subject, message, recipient):
    """Функция отправки писем."""
    send_mail(
        subject,
        message,
        from_email=None,
        recipient_list=[recipient],
        fail_silently=False
    )
