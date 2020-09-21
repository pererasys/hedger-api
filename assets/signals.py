'''
Written by Andrew Perera
Copyright 2020
'''

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Exchange
from .tasks import generate_tickers

@receiver(post_save, sender=Exchange)
def create_tickers(sender, instance, created, **kwargs):
    if created:
        # Collect tickers for the new exchange
        generate_tickers.delay(exchange=instance.mic)