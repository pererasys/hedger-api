'''
Written by Andrew Perera
Copyright 2020
'''

from hedger.celery import app
from celery.utils.log import get_task_logger
from celery.decorators import periodic_task, task
from celery.schedules import crontab
from .actions import marketstack
from .models import Asset, Report
import numpy as np
import talib

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
        data = marketstack.fetch_reports(symbols=','.join([asset.symbol for asset in assets]))
        logger.info(f'Creating {len(data)} reports.')
        Report.objects.bulk_create(data, ignore_conflicts=True)


@app.task(name="generate_tickers")
def generate_tickers(exchange):
    logger.info('Generating tickers for new exchange.')

    data = marketstack.fetch_assets(exchange)

    logger.info(f'Creating {len(data)} assets.')

    Asset.objects.bulk_create(data, ignore_conflicts=True)


@app.task(name="generate_extended_reports")
def generate_extended_reports(symbol, start_date=None):
    logger.info('Generating daily reports.')

    data = marketstack.fetch_extended_reports(symbol=symbol, start_date=start_date)

    close = [report.close for report in data]
    close = np.array(close)[::-1]
    
    rsi = talib.RSI(close, timeperiod=14)
    ema = talib.EMA(close, timeperiod=30)
    macd, macd_signal, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    i = len(data) - 1
    for report in data:
        if not np.isnan(ema[i]):
            report.ema = float(ema[i])
        if not np.isnan(rsi[i]):
            report.rsi = float(rsi[i])
        if not np.isnan(macd[i]):
            report.macd = float(macd[i])
            report.macd_signal = float(macd_signal[i])
            report.macd_hist = float(macd_hist[i])
        i -= 1

    logger.info(f'Creating {len(data)} reports.')
    Report.objects.bulk_create(data, ignore_conflicts=True)