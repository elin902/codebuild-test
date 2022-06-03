"""Definiowanie wzorców adresów url dla aplikacji users"""

from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # dołączenie domyślnych adresów URL uwierzytelniania
    path('', include('django.contrib.auth.urls')),
    # Rejestracja nowego użytkownika
    path('register/', views.register, name='register'),
]
