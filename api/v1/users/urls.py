from django.contrib import admin
from django.urls import path, include
from .views import CreateUserView

# defining the endpoint
urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create-user")
]
