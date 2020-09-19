'''
Written by Andrew Perera
Copyright 2020
'''

from django.db import models
from datetime import datetime
import uuid

class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    symbol = models.CharField(max_length=10, unique=True)
    exchange = models.CharField(max_length=50, blank=True)
    display_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "asset"
        verbose_name_plural = "assets"

    def __str__(self):
        return self.display_name

class DailyReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="reports")
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
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "daily report"
        verbose_name_plural = "daily reports"

    def __str__(self):
        return f'{self.asset} - {datetime.strftime(self.date, "%m-%d-%Y")}'
