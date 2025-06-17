from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileEditView, ViewProfile

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile'),
    path('profile/', ViewProfile.as_view(), name='view_profile')
]
