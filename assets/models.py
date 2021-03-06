'''
Written by Andrew Perera
Copyright 2020
'''

from django.db import models
from django.utils.timezone import now
from datetime import datetime
import uuid


class Exchange(models.Model):
    mic = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    acronym = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "exchange"
        verbose_name_plural = "exchanges"

    def __str__(self):
        return self.name


class Asset(models.Model):
    symbol = models.CharField(primary_key=True, max_length=10, unique=True)
    exchange = models.ForeignKey(
        Exchange, on_delete=models.CASCADE, related_name="assets")
    name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "asset"
        verbose_name_plural = "assets"

    def __str__(self):
        return self.symbol
    
    def activate(self):
        self.active = True
        self.save()
    
    def deactivate(self):
        self.active = False
        self.save()

    def is_user_watching(self, user):
        return self in user.watch_list.all()

    @property
    def latest_report(self):
        latest_reports = self.reports.order_by("-timestamp")
        if latest_reports.count() > 0:
            return latest_reports[0]
    
    @property
    def last(self):
        report = self.latest_report
        if report:
            return report.close
    
    @property
    def percent_change(self):
        reports = self.reports.all().order_by('-timestamp')
        if reports.count() > 1:
            reports = reports[:2]
            diff = reports[0].close - reports[1].close
            return round((diff / reports[1].close) * 10**2, 2)


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="reports")

    # EOD data
    open = models.DecimalField(max_digits=9, decimal_places=2)
    high = models.DecimalField(max_digits=9, decimal_places=2)
    low = models.DecimalField(max_digits=9, decimal_places=2)
    close = models.DecimalField(max_digits=9, decimal_places=2)
    volume = models.IntegerField()
    adj_open = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    adj_high = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    adj_low = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    adj_close = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    adj_volume = models.IntegerField(null=True)

    # Indicators
    ema = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    macd = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    macd_signal = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    macd_hist = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    rsi = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    timestamp = models.DateTimeField()

    class Meta:
        verbose_name = "daily report"
        verbose_name_plural = "daily reports"
        unique_together = ['asset', 'timestamp']

    def __str__(self):
        return f'{self.asset} {datetime.strftime(self.timestamp, "%m-%d-%Y")}'
