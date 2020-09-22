from django.contrib import admin
from django.urls import path, include
from .views import AssetViewSet

# defining the endpoint
urlpatterns = [
    path("", AssetViewSet.as_view({"get": "list"}), name="all-assets"),
    path("<slug:symbol>/",
         AssetViewSet.as_view({"get": "retrieve"}), name="detail-asset"),
]
