from django.utils import timezone
from django.core.mail import send_mail
from .models import Mailing, MailingAttempt


def send_mailing(mailing_id):
    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        # Можно логировать или выбрасывать исключение
        return

    # Обновляем статус рассылки на "Запущена"
    mailing.status = 'Запущена'
    mailing.start_time = timezone.now()
    mailing.save()

    recipients = mailing.recipients.all()

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email='your_email@example.com',
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            # Записываем успешную попытку
            MailingAttempt.objects.create(
                mailing=mailing,
                status='Успешно',
                server_response='Письмо успешно отправлено'
            )
        except Exception as e:
            # Записываем ошибку
            MailingAttempt.objects.create(
                mailing=mailing,
                status='Не успешно',
                server_response=str(e)
            )

    # Обновляем статус рассылки на "Завершена"
    mailing.status = 'Завершена'
    mailing.end_time = timezone.now()
    mailing.save()
