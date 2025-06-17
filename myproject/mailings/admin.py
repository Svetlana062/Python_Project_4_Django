from django.contrib import admin
from .models import Mailing, Message, Recipient, MailingAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_time', 'end_time')
    list_filter = ('status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'status', 'attempt_time')
    