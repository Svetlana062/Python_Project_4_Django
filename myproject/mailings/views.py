import datetime

from django.shortcuts import render, redirect

from .forms import MailingForm
from .models import Mailing, Recipient, Message, MailingAttempt
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipient
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from . import utils
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


def my_view(request):
    # Попытка получить данные из кеша
    data = cache.get('my_key')

    # Если данные не найдены в кеше, выполняем вычисления и сохраняем результат в кеш
    if not data:
        data = 'some expensive computation'
        cache.set('my_key', data, 60 * 15)  # Кешируем данные на 15 минут

    # Возвращаем ответ с данными
    return HttpResponse(data)


def index(request):
    """Главная страница."""
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='Запущена').count()
    total_recipients = Recipient.objects.count()

    context={
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'total_recipients': total_recipients,
    }
    return render(request, 'index.html', context)


# CRUD для Recipient
@method_decorator(cache_page(60*15), name='dispatch')
class RecipientListView(LoginRequiredMixin, ListView):
    """Список получателей."""
    model = Recipient
    template_name = 'recipients/list.html' # путь к шаблону
    context_object_name = 'recipients' # переменная в шаблоне

    def get_queryset(self):
        # фильтруем по текущему пользователю (owner)
        return Recipient.objects.filter(owner=self.request.user)

class RecipientCreateView(LoginRequiredMixin, CreateView):
    """Создание нового получателя."""
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = 'recipients/form.html' # путь к шаблону
    success_url = reverse_lazy('recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление существующего получателя."""
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = 'recipients/form.html' # путь к шаблону
    success_url = reverse_lazy('recipient_list')

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление получателя с подтверждением."""
    model = Recipient
    template_name = 'recipients/confirm_delete.html' # путь к шаблону
    success_url = reverse_lazy('recipient_list')

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей получателя."""
    model = Recipient
    template_name = 'recipients/detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


# CRUD для Message
@method_decorator(cache_page(60*15), name='dispatch')
class MessageListView(ListView):
    """Список сообщений."""
    model = Message
    template_name = 'messages/list_messages.html' # путь к шаблону
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание нового сообщения."""
    model = Message
    fields = ['subject', 'body']
    template_name = 'messages/form_message.html'
    success_url = reverse_lazy('list_messages')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление существующего сообщения."""
    model = Message
    fields = ['subject', 'body']
    template_name = 'messages/form_message.html'
    success_url = reverse_lazy('list_messages')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения."""
    model = Message
    template_name = 'messages/confirm_delete_message.html'
    success_url = reverse_lazy('list_messages')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей сообщения."""
    model = Message
    template_name = 'messages/detail_message.html'
    context_object_name = 'message'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


# CRUD для Mailing
@method_decorator(cache_page(60*15), name='dispatch')
class MailingListView(LoginRequiredMixin, ListView):
    """Просмотр списка рассылок."""
    model = Mailing
    template_name = 'mailings/list_mailing.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        # фильтруем по владельцу (owner)
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создание рассылки."""
    model = Mailing
    fields = ['name', 'status']
    template_name = 'mailings/form_mailing.html'
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление существующей рассылки."""
    model = Mailing
    fields = ['name', 'status']
    template_name = 'mailings/form_mailing.html'
    success_url = reverse_lazy('mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление рассылки."""
    model = Mailing
    template_name = 'mailings/confirm_delete_mailing.html'
    success_url = reverse_lazy('mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей рассылки."""
    model = Mailing
    template_name = 'mailings/detail_mailing.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


# Страница попыток рассылки (может быть отдельной или внутри рассылки)
class MailingAttemptListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_attempts.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        mailing_id = self.kwargs.get('pk')
        return MailingAttempt.objects.filter(mailing_id=mailing_id).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = get_object_or_404(Mailing, pk=self.kwargs.get('pk'))
        return context


# Запуск рассылки
@require_POST
def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    # Обновляем статус на "Запущена"
    mailing.status = 'Запущена'
    mailing.start_time = timezone.now()
    mailing.save()

    # Запускаем отправку писем
    utils.send_mailing(pk)

    # После завершения обновляем статус на "Завершена"
    mailing.status = 'Завершена'
    mailing.end_time = timezone.now()
    mailing.save()
    return HttpResponseRedirect(reverse('mailing_detail', args=[pk]))

def create_mailing(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save()
            # Можно перенаправить на страницу деталей или обратно к списку
            return redirect('detail_mailing', mailing.id)
    else:
        form = MailingForm()
    return render(request, 'mailings/form_mailing.html', {'form': form})
