'''
Written by Andrew Perera
Copyright 2020
'''

from celery.utils.log import get_task_logger
from .helpers import paginated_fetch, transform_report, transform_asset

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

