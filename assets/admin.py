'''
Written by Andrew Perera
Copyright 2020
'''

from django.contrib import admin
from .models import Exchange, Asset, Report
from datetime import datetime

class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['name', 'acronym', 'total_assets']

    def total_assets(self, obj):
        return obj.assets.count()

    total_assets.short_description = "total assets"

class AssetAdmin(admin.ModelAdmin):
    ordering = ['-active']
    search_fields = ['symbol', 'name']
    list_display = ['name', 'symbol', 'exchange', 'active']


class ReportAdmin(admin.ModelAdmin):
    ordering = ['-timestamp']
    list_display = ['date','asset', 'open', 'close']

    def date(self, obj):
        return datetime.strftime(obj.timestamp, "%Y-%m-%d")


admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Report, ReportAdmin)