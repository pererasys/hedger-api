from django.contrib import admin
from django.urls import path, include
from .views import CreateUserView, UserViewSet

# defining the endpoint
urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create-user"),
    path("me/", UserViewSet.as_view({'get': 'retrieve'}), name="auth-user")
]
