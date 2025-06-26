from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'phone_number', 'country']


class RegistrationForm(UserCreationForm):
    """Форма для регистрации"""
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar', 'phone_number', 'country')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
