'''
Written by Andrew Perera
Copyright 2020
'''

from celery.utils.log import get_task_logger
from .helpers import paginated_fetch, transform_report, transform_asset
from datetime import datetime, timedelta

logger = get_task_logger(__name__)

'''

Marketstack API docs
https://marketstack.com/documentation

'''

def fetch_reports(symbols):
    query_params = {
        "symbols": symbols,
    }
    return paginated_fetch(endpoint="/eod/latest", transform=transform_report, query_params=query_params)


def fetch_assets(exchange):
    query_params = {
        "exchange": exchange,
    }
    return paginated_fetch(endpoint="/tickers", transform=transform_asset, query_params=query_params)


def fetch_extended_reports(symbol, start_date):
    if not start_date:
        start_date = datetime.now() - timedelta(days=365)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S%z")

    query_params = {
        "symbols": symbol,
        "date_from": datetime.strftime(start_date, "%Y-%m-%d")
    }
    return paginated_fetch(endpoint="/eod", transform=transform_report, query_params=query_params)

