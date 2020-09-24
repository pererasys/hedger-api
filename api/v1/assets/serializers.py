from rest_framework import serializers, exceptions
from assets.models import Exchange, Asset, Report
from datetime import datetime, timedelta


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

    class Meta:
        model = Asset
        fields = ['symbol', 'name', 'exchange']


class DetailSerializer(serializers.ModelSerializer):
    exchange = ExchangeSerializer(read_only=True)
    latest_report = ReportSerializer(read_only=True)
    historical_data = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = [
            'symbol',
            'name',
            'exchange',
            'latest_report',
            'historical_data'
        ]

    def get_historical_data(self, obj):
        params = self.context.get("request").query_params

        default_start_date = datetime.strftime(datetime.now() - timedelta(days=365), "%Y-%m-%d")

        start_date = params.get("start_date", default_start_date)
        indicators = params.get("indicators", None)

        reports = Report.objects.filter(timestamp__gte=start_date).order_by('timestamp')
        res = {
            "pps": [{"value": report.close, "timestamp": report.timestamp} for report in reports],
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
                    "histagram": [report.macd_hist for report in reports],
                }
            
        return res