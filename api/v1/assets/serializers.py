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
    latest_report = ReportSerializer(read_only=True)
    percent_change = serializers.ReadOnlyField()
    historical_data = serializers.SerializerMethodField()
    is_watching = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = [
            'symbol',
            'name',
            'exchange',
            'latest_report',
            'historical_data',
            'is_watching',
            'percent_change'
        ]

    def get_is_watching(self, obj):
        user = self.context.get('user')
        return obj in user.watch_list.all()

    def get_historical_data(self, obj):
        params = self.context.get("params")

        start_date = timezone.now() - timedelta(days=365)

        indicators = params.get("indicators", None)

        reports = obj.reports.filter(timestamp__gte=start_date).order_by('-timestamp')

        if reports.count() == 0:
            return None

        res = {
            "1y": [{"value": report.close, "timestamp": report.timestamp} for report in reports],
            "6m": [{"value": report.close, "timestamp": report.timestamp} for report in reports.filter(timestamp__gte=start_date + timedelta(days=182))],
            "1m": [{"value": report.close, "timestamp": report.timestamp} for report in reports.filter(timestamp__gte=start_date + timedelta(days=337))],
        }

        # Build indicator data
        if indicators:
            indicators = indicators.split(',')

            if "ema" in indicators:
                res['ema'] = [report.ema for report in reports]

            if "rsi" in indicators:
                res['rsi'] = [report.rsi for report in reports]

            if "macd" in indicators:
                res['macd'] = {
                    "value": [report.macd for report in reports],
                    "signal": [report.macd_signal for report in reports],
                    "histogram": [report.macd_hist for report in reports],
                }
            
        return res