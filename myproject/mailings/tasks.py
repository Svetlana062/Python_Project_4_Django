from django.utils import timezone
from .models import Mailing
from .utils import send_mailing
from django.apps import AppConfig


def send_scheduled_mailings():
    """Функция для отправки запланированных рассылок."""
    now = timezone.now()
    mailings_to_send = Mailing.objects.filter(scheduled_time__lte=now, status='scheduled')
    for mailing in mailings_to_send:
        send_mailing(mailing)
        mailing.status = 'sent'
        mailing.save()


class MyAppConfig(AppConfig):
    name = 'myapp'
