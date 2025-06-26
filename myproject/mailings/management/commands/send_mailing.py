from django.core.management.base import BaseCommand, CommandError
from ...utils import send_mailing as send_mailing_func


class Command(BaseCommand):
    help = 'Запуск отправки рассылки по ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int)

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            send_mailing_func(mailing_id)
            self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing_id} успешно запущена'))
        except Exception as e:
            raise CommandError(f'Ошибка при запуске рассылки: {e}')
