'''
Written by Andrew Perera
Copyright 2020
'''

from django.db import models
from django.utils.timezone import now
from datetime import datetime
import uuid


class Exchange(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=100, unique=True)
    mic = models.CharField(max_length=10, unique=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    class Meta:
        verbose_name = "exchange"
        verbose_name_plural = "exchanges"

    def __str__(self):
        return self.name


class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name="assets")

    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = "asset"
        verbose_name_plural = "assets"

    def __str__(self):
        return self.name



class DailyReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="reports")

    # EOD data
    open = models.DecimalField(max_digits=9, decimal_places=2)
    high = models.DecimalField(max_digits=9, decimal_places=2)
    low = models.DecimalField(max_digits=9, decimal_places=2)
    close = models.DecimalField(max_digits=9, decimal_places=2)
    volume = models.IntegerField()
    adj_open = models.DecimalField(max_digits=9, decimal_places=2)
    adj_high = models.DecimalField(max_digits=9, decimal_places=2)
    adj_low = models.DecimalField(max_digits=9, decimal_places=2)
    adj_close = models.DecimalField(max_digits=9, decimal_places=2)
    adj_volume = models.IntegerField()

    # Indicators
    ema = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    macd = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    rsi = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    date = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "daily report"
        verbose_name_plural = "daily reports"
        unique_together = ['asset', 'date']

    def __str__(self):
        return f'{self.asset} - {datetime.strftime(self.date, "%m-%d-%Y")}'
