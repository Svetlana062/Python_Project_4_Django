from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mailings.urls')),  # подключение URL-ов приложения mailings
    path('accounts/', include('accounts.urls')),  # подключение URL-ов приложения accounts

]

# Обслуживание медиафайлов при DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
