from django.urls import path
from . import views
from .views import MailingAttemptListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),

    # CRUD для Recipient
    path('recipients/', views.RecipientListView.as_view(), name='recipient_list'),
    path('recipients/add/', views.RecipientCreateView.as_view(), name='recipient_add'),
    path('recipients/<int:pk>/edit/', views.RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipients/<int:pk>/delete/', views.RecipientDeleteView.as_view(), name='recipient_delete'),
    path('recipients/<int:pk>/', views.RecipientDetailView.as_view(), name='recipient_detail'),

   # CRUD для Message
    path('messages/', views.MessageListView.as_view(), name='list_messages'),
    path('messages/add/', views.MessageCreateView.as_view(), name='message_add'),
    path('messages/<int:pk>/edit/', views.MessageUpdateView.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),

    # CRUD для Mailing
    path('mailings/', views.MailingListView.as_view(), name='mailing_list'),
    path('mailings/add/', views.MailingCreateView.as_view(), name='mailing_add'),
    path('mailings/<int:pk>/edit/', views.MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/send/', views.send_mailing, name='send_mailing'),
    path('mailings/<int:pk>/', views.MailingDetailView.as_view(), name='detail_mailing'),
    path('mailings/<int:pk>/attempts/', MailingAttemptListView.as_view(), name='mailing_attempts'),

    # Страница попыток рассылки (может быть отдельной или внутри рассылки)
    path('attempts/', views.MailingAttemptListView.as_view(), name='attempt_list'),

    # Добавление URL-ов для восстановления пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
