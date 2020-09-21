'''
Written by Andrew Perera
Copyright 2020
'''

import requests
from requests.exceptions import RequestException
from hedger.celery import app
from celery.utils.log import get_task_logger
from celery.decorators import periodic_task, task
from celery.schedules import crontab
from django.conf import settings
from .models import Asset, DailyReport
from datetime import datetime

logger = get_task_logger(__name__)


'''

Marketstack API docs
https://marketstack.com/documentation

'''

def build_report(report):
    return DailyReport(asset_symbol=report.get('symbol'), date=datetime.strptime(report.get('date'), "%Y-%m-%dT%H:%M:%S%z"), **report)

def fetch_reports(assets, offset=0, limit=1000, initial=[]):

    params = {
        "access_key": settings.MARKETSTACK_ACCESS_KEY,
        "symbols": ','.join([asset.symbol for asset in assets]),
        "limit": limit,
        "offset": offset
    }

    result = None

    try:
        result = requests.get('https://api.marketstack.com/v1/eod/latest', params)
    except RequestException as e:
        logger.error('Request for eod data threw an exception.')

    if result:
        response = result.json()

        current_index = offset + limit
        reports = initial + response['data']

        if current_index < response['pagination']['total']:
            return fetch_reports(assets, offset=current_index, limit=limit, initial=reports)

        return [build_report(report) for report in reports]
    else:
        logger.info('No request result, returning initial.')
        return initial


@periodic_task(
    run_every=(crontab(hour=16, minute=30)), # Run at 4:30, 30min after market close
    name="generate_daily_reports",
    ignore_result=True
)
def generate_daily_reports():
    logger.info('Generating daily reports.')
    assets = Asset.objects.all()

    reports = fetch_reports(assets)

    DailyReport.objects.bulk_create(reports, 1000, ignore_result=True)

