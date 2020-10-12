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
            'timestamp',
        ]

class ListSerializer(serializers.ModelSerializer):
    exchange = serializers.StringRelatedField()
    last = serializers.ReadOnlyField()
    percent_change = serializers.ReadOnlyField()
    is_watching = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ['symbol', 'name', 'exchange', 'last', 'percent_change', 'is_watching']
    
    def get_is_watching(self, obj):
        user = self.context.get('user')
        return obj in user.watch_list.all()
    


class DetailSerializer(serializers.ModelSerializer):
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