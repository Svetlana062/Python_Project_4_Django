from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser


# Регистрация пользователя
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Отправка приветственного письма после регистрации
        self.send_welcome_email()
        return response

    def send_welcome_email(self):
        from django.core.mail import send_mail
        subject = "Добро пожаловать!"
        message = "Спасибо за регистрацию на нашем сайте."
        recipient_list = [self.object.email]
        send_mail(subject, message, None, recipient_list)


# Вход в систему (используем встроенное представление)
class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm


# Выход из системы (используем встроенное представление)
class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')


# Редактирование профиля
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['avatar', 'phone_number', 'country']
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')


# Просмотр профиля
class ViewProfile(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/view_profile.html'  # создайте этот шаблон
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
