from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # Вход/выход
    path('tasks/', include('tasks.urls')),
    path('', RedirectView.as_view(url='/tasks/', permanent=False)), # Редирект с корня
]