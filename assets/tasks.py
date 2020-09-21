'''
Written by Andrew Perera
Copyright 2020
'''

import requests
from requests.exceptions import RequestException
from datetime import datetime

from django.conf import settings
from hedger.celery import app
from celery.utils.log import get_task_logger
from celery.decorators import periodic_task, task
from celery.schedules import crontab
from .models import Asset, DailyReport

logger = get_task_logger(__name__)


'''

Marketstack API docs
https://marketstack.com/documentation

'''


def build_report(report):
    data =  {
        "asset_id": report.get('symbol', None),
        "open": report.get('open', None),
        "high": report.get('high', None),
        "low": report.get('low', None),
        "close": report.get('close', None),
        "volume": report.get('volume', None),
        "adj_open": report.get('adj_open', None),
        "adj_low": report.get('adj_low', None),
        "adj_high": report.get('open', None),
        "adj_close": report.get('adj_close', None),
        "adj_volume": report.get('adj_volume', None),
    }
    return DailyReport(**data)


def transform_asset(asset, exchange):
    data = {
        "exchange_id": exchange,
        "name": asset['name'],
        "symbol": asset['symbol'],
    }
    return Asset(**data)


def fetch_reports(symbols, offset=0, limit=1000, initial=[]):
    params = {
        "access_key": settings.MARKETSTACK_ACCESS_KEY,
        "symbols": symbols,
        "limit": limit,
        "offset": offset
    }

    try:
        result = requests.get('http://api.marketstack.com/v1/eod/latest', params)
        response = result.json()

        next_offset = offset + response['pagination']['count']
        reports = initial + [build_report(report) for report in response['data']]
        logger.info(f'Collected {len(reports)} reports.')

        if next_offset <= response['pagination']['total']:
            logger.info('Fetching more.')
            return fetch_reports(symbols, offset=next_offset, limit=limit, initial=reports)

        return reports
    except RequestException as e:
        logger.error('Request for eod data threw an exception, returning initial dataset.')
        return initial


def fetch_assets(exchange, offset=0, limit=1000, initial=[]):
    params = {
        "access_key": settings.MARKETSTACK_ACCESS_KEY,
        "exchange": exchange,
        "limit": limit,
        "offset": offset
    }

    try:
        result = requests.get(f'http://api.marketstack.com/v1/tickers', params)
        response = result.json()

        next_offset = offset + response['pagination']['count']
        assets = initial + [transform_asset(asset=asset, exchange=exchange) for asset in response['data']]
        logger.info(f'Collected {len(assets)} assets.')
        
        if next_offset <= response['pagination']['total']:
            logger.info('Fetching more.')
            return fetch_assets(exchange, offset=next_offset, limit=limit, initial=assets)

        return assets
    except RequestException as e:
        logger.error('Request for asset data threw an exception.')
        return initial


@periodic_task(
    run_every=(crontab(hour=16, minute=30)), # Run at 4:30pm, 30min after market close
    name="generate_daily_reports",
    ignore_result=True
)
def generate_daily_reports():
    logger.info('Generating daily reports.')

    assets = Asset.objects.filter(active=True)

    if assets.count() > 0:
        data = fetch_reports(symbols=','.join([asset.symbol for asset in assets]))
        logger.info(f'Creating {len(data)} reports.')
        DailyReport.objects.bulk_create(data, ignore_conflicts=True)


@app.task(name="generate_tickers")
def generate_tickers(exchange):
    logger.info('Generating tickers for new exchange.')

    data = fetch_assets(exchange)

    logger.info(f'Creating {len(data)} assets.')

    Asset.objects.bulk_create(data, ignore_conflicts=True)
