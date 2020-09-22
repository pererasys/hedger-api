from assets.models import Asset
from django.shortcuts import get_object_or_404
from .serializers import ListSerializer, DetailSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q


class AssetViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving Assets.
    """

    def list(self, request):
        query = request.query_params.get("search", "")
        queryset = Asset.objects.filter(Q(symbol__icontains=query) | Q(name__icontains=query))
        serializer = ListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, symbol=None):
        queryset = Asset.objects.all()
        asset = get_object_or_404(queryset, symbol=symbol)
        serializer = DetailSerializer(asset)
        return Response(serializer.data)
