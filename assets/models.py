'''
Written by Andrew Perera
Copyright 2020
'''

from django.db import models
import uuid

class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticker = models.CharField(max_length=10, unique=True)
    display_name = models.CharField(max_length=255)
    bid = models.DecimalField(max_digits=9, decimal_places=2)
    ask = models.DecimalField(max_digits=9, decimal_places=2)
    last = models.DecimalField(max_digits=9, decimal_places=2)


    class Meta:
        verbose_name = "asset"
        verbose_name_plural = "assets"

    def __str__(self):
        return self.display_name
