from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views
from rest_framework.response import Response
from django.db.models import Q
from assets.models import Asset
from assets.tasks import generate_extended_reports
from .serializers import ListSerializer, DetailSerializer


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


class AssetActivationView(views.APIView):

    def post(self, request, symbol):
        queryset = Asset.objects.all()
        asset = get_object_or_404(queryset, symbol=symbol)

        asset.activate()

        # celery task to fetch last 5 years of data
        generate_extended_reports.delay(symbol=symbol, start_date=asset.latest_report.timestamp)

        return Response({"detail": "Successfully activated asset."})


class WatchAssetView(views.APIView):

    def post(self, request, symbol):
        queryset = Asset.objects.all()
        user = request.user

        asset = get_object_or_404(queryset, symbol=symbol)

        if asset.watched_by.count() == 0:
            asset.activate()
            print(asset.latest_report.timestamp)
            # celery task to fetch last 5 years of data
            generate_extended_reports.delay(symbol=symbol, start_date=asset.latest_report.timestamp)

        user.watch_list.add(asset)

        return Response({"detail": f'Added {symbol} to watch list.'})


class UnwatchAssetView(views.APIView):

    def post(self, request, symbol):
        queryset = Asset.objects.all()
        user = request.user

        asset = get_object_or_404(queryset, symbol=symbol)
        user.watch_list.remove(asset)

        if asset.watched_by.count() == 0:
            asset.deactivate()

        return Response({"detail": f'Removed {symbol} from watch list.'})
            