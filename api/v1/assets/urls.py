from django.contrib import admin
from django.urls import path, include
from .views import (
    AssetViewSet,
    AssetActivationView,
    WatchAssetView,
    UnwatchAssetView
)

# defining the endpoint
urlpatterns = [
    path("", AssetViewSet.as_view({"get": "list"}), name="all-assets"),
    path("watching/", AssetViewSet.as_view({"get": "watching"}), name="user-watchlist"),
    path("<slug:symbol>/",
         AssetViewSet.as_view({"get": "retrieve"}), name="detail-asset"),
    path("activate/<slug:symbol>/", AssetActivationView.as_view(), name="activate-asset"),
    path("watch/<slug:symbol>/", WatchAssetView.as_view(), name="watch-asset"),
    path("unwatch/<slug:symbol>/", UnwatchAssetView.as_view(), name="unwatch-asset"),
]
