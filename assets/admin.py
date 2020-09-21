from django.contrib import admin
from .models import Exchange, Asset, DailyReport

admin.site.register(Exchange)
admin.site.register(Asset)
admin.site.register(DailyReport)