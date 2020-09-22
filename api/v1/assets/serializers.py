from rest_framework import serializers, exceptions
from assets.models import Exchange, Asset, Report


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
            'ema',
            'macd',
            'rsi',
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

    class Meta:
        model = Asset
        fields = ['symbol', 'name', 'exchange', 'latest_report']
