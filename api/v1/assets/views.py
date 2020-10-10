from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q
from django.db.models import Count
from assets.models import Asset
from assets.tasks import generate_extended_reports
from .serializers import ListSerializer, DetailSerializer


class AssetViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Assets.
    """

    def list(self, request):
        query = request.query_params.get("query", "")
        queryset = Asset.objects.filter(Q(symbol__istartswith=query) | Q(name__istartswith=query)).annotate(symbol_count=Count('symbol')).order_by('symbol_count')
        
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = ListSerializer(page, many=True, context={'user': request.user})
            return self.paginator.get_paginated_response(serializer.data)

        return Response(serializer.data)
    
    def watching(self, request):
        assets = request.user.watch_list.all()

        page = self.paginator.paginate_queryset(assets, request)

        if page is not None:
            serializer = ListSerializer(assets, many=True, context={'user': request.user})
            return self.paginator.get_paginated_response(serializer.data)

        return Response(serializer.data)


    def retrieve(self, request, symbol=None):
        queryset = Asset.objects.all()
        asset = get_object_or_404(queryset, symbol=symbol)
        serializer = DetailSerializer(asset, context={"params": request.query_params})
        
        return Response(serializer.data)


class AssetActivationView(views.APIView):

    def post(self, request, symbol):
        queryset = Asset.objects.all()
        asset = get_object_or_404(queryset, symbol=symbol)

        asset.activate()

        start_date = None

        if asset.latest_report:
            start_date = asset.latest_report.timestamp

        # celery task to fetch data
        generate_extended_reports.delay(symbol=symbol, start_date=start_date)

        return Response({"detail": "Successfully activated asset."})


class WatchAssetView(views.APIView):

    def post(self, request, symbol):
        queryset = Asset.objects.all()
        user = request.user

        asset = get_object_or_404(queryset, symbol=symbol)

        start_date = None

        if asset.latest_report:
            start_date = asset.latest_report.timestamp

        if asset.watchers.count() == 0:
            asset.activate()

        # celery task to fetch data
        generate_extended_reports.delay(symbol=symbol, start_date=start_date)

        user.watch_list.add(asset)

        return Response({"detail": f'Added {symbol} to watch list.'})


class UnwatchAssetView(views.APIView):

    def post(self, request, symbol):
        queryset = Asset.objects.all()
        user = request.user

        asset = get_object_or_404(queryset, symbol=symbol)
        user.watch_list.remove(asset)

        if asset.watchers.count() == 0:
            asset.deactivate()

        return Response({"detail": f'Removed {symbol} from watch list.'})
            