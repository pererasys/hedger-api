from django.contrib import admin
from .models import Asset, DailyReport

admin.site.register(Asset)
admin.site.register(DailyReport)