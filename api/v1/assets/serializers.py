from rest_framework import serializers, exceptions
from assets.models import Exchange, Asset, Report
from django.utils import timezone
from datetime import timedelta
import pytz


class ExchangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exchange
        fields = ['mic', 'name', 'acronym']


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = [
            'id',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'adj_open',
            'adj_high',
            'adj_low',
            'adj_close',
            'adj_volume',
            'macd',
            'macd_hist',
            'macd_signal',
            'ema',
            'rsi',
            'timestamp',
        ]

class ListSerializer(serializers.ModelSerializer):
    last = serializers.ReadOnlyField()
    percent_change = serializers.ReadOnlyField()
    is_watching = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ['symbol', 'name', 'last', 'percent_change', 'is_watching']

    def get_is_watching(self, obj):
        user = self.context.get('user')
        return obj.is_user_watching(user)


class WatchedAssetSerializer(ListSerializer):
    historical_data = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ListSerializer.Meta.fields + ["historical_data"]

    def get_historical_data(self, obj):
        start_date = timezone.now() - timedelta(days=365)
        return [report.close for report in obj.reports.filter(timestamp__gte=start_date).order_by('-timestamp')]



class DetailSerializer(ListSerializer):
    exchange = ExchangeSerializer(read_only=True)
    reports = serializers.SerializerMethodField()
    is_watching = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = [
            'symbol',
            'name',
            'exchange',
            'reports',
            'is_watching',
        ]

    def get_is_watching(self, obj):
        user = self.context.get('user')
        return obj in user.watch_list.all()

    def get_reports(self, obj):
        reports = obj.reports.filter(timestamp__gte=timezone.now() - timedelta(days=365)).order_by('-timestamp')
        serializer = ReportSerializer(reports, many=True, read_only=True)
        return serializer.data