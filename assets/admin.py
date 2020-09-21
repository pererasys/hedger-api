'''
Written by Andrew Perera
Copyright 2020
'''

from django.contrib import admin
from .models import Exchange, Asset, Report

class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['name', 'acronym', 'total_assets']

    def total_assets(self, obj):
        return obj.assets.count()

    total_assets.short_description = "total assets"

class AssetAdmin(admin.ModelAdmin):
    ordering = ['-active']
    search_fields = ['symbol', 'name']
    list_display = ['name', 'symbol', 'exchange', 'active']



admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Report)