from django.db import models

from django.conf import settings


class Recipient(models.Model):
    """Модель получателя."""
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='recipients'
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    """Модель сообщения."""
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='messages'
    )

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    """Модель рассылки."""
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]
    name = models.CharField(max_length=255, default='Default Name')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Создана')
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='mailings'
    )

    def __str__(self):
        return f"Mailing #{self.id} - {self.status}"


class MailingAttempt(models.Model):
    """Модель попытки рассылки."""
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]

    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField()

    def __str__(self):
        return f"{self.mailing.name} - {self.attempt_time} - {self.status}"
