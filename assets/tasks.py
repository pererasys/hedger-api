'''
Written by Andrew Perera
Copyright 2020
'''

from hedger.celery import app
from celery.utils.log import get_task_logger
from celery.decorators import periodic_task, task
from celery.schedules import crontab
from .models import Asset, Report
from .actions.marketstack import fetch_reports, fetch_assets, fetch_extended_reports

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(hour=0, minute=0)), # Run at midnight
    name="generate_daily_reports",
    ignore_result=True
)
def generate_daily_reports():
    logger.info('Generating daily reports.')

    assets = Asset.objects.filter(active=True)

    if assets.count() > 0:
        data = fetch_reports(symbols=','.join([asset.symbol for asset in assets]))
        logger.info(f'Creating {len(data)} reports.')
        Report.objects.bulk_create(data, ignore_conflicts=True)


@app.task(name="generate_tickers")
def generate_tickers(exchange):
    logger.info('Generating tickers for new exchange.')

    data = fetch_assets(exchange)

    logger.info(f'Creating {len(data)} assets.')

    Asset.objects.bulk_create(data, ignore_conflicts=True)


@app.task(name="generate_extended_reports")
def generate_extended_reports(symbol, start_date=None):
    logger.info('Generating daily reports.')

    data = fetch_extended_reports(symbol=symbol, start_date=start_date)

    logger.info(f'Creating {len(data)} reports.')
    Report.objects.bulk_create(data, ignore_conflicts=True)
