from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import Mailing
from ...utils import send_mailing as send_mailing_func

class Command(BaseCommand):
    help = 'Автоматическая отправка всех запланированных рассылок, время которых наступило'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        # ищем все неподтвержденные и запланированные рассылки, время которых прошло
        mailings = Mailing.objects.filter(
            scheduled_time__lte=now,
            status=['Создана', 'Запущена']
        )

        for mailing in mailings:
            try:
                # вызываем вашу существующую функцию отправки по ID
                send_mailing_func(mailing.id)
                mailing.is_sent = True
                mailing.save()
                self.stdout.write(self.style.SUCCESS(f'Рассылка "{mailing.title}" успешно отправлена'))
            except Exception as e:
                self.stderr.write(f'Ошибка при отправке "{mailing.title}": {e}')
