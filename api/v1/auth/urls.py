from django.contrib import admin
from django.urls import path, include
from .views import LoginView, LogoutView

urlpatterns = [
    path( "login/", LoginView.as_view(), name="login-user"),
    path( "logout/", LogoutView.as_view(), name="logout-user")
]
