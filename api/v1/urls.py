from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('users/', include('api.v1.users.urls')),
    path('auth/', include('api.v1.auth.urls')),
    path('assets/', include('api.v1.assets.urls')),
]
