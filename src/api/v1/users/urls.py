from django.contrib import admin
from django.urls import path, include
from .views import UserViewSet

# defining the endpoint
urlpatterns = [
    path(
        "create/", UserViewSet.as_view({"post": "create"}), name="create-user")
]
