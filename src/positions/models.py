'''
Written by Andrew Perera
Copyright 2020
'''

from django.db import models
from users.models import UserAccount
from assets.models import Asset
from datetime import datetime
import uuid

class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="positions")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="positions")
    date_created = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "position"
        verbose_name_plural = "positions"

    def __str__(self):
        return self.asset.display_name


class Trade(models.Model):
    TYPE_CHOICES = [
        ("SALE", "Sale"),
        ("PURCHASE", "Purchase")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="trades")
    trade_type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = "trade"
        verbose_name_plural = "trades"

    def __str__(self):
        return f'{self.position} - {self.trade_type}'
