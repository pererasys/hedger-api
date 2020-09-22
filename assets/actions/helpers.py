'''
Written by Andrew Perera
Copyright 2020
'''

import requests
from requests.exceptions import RequestException
from django.conf import settings
from assets.models import Asset, Report
from celery.utils.log import get_task_logger
from datetime import datetime

logger = get_task_logger(__name__)

def paginated_fetch(endpoint, transform, query_params={}, offset=0, initial=[]):
    params = {
        "access_key": settings.MARKETSTACK_ACCESS_KEY,
        "limit": 1000,
        "offset": offset,
    }

    params.update(query_params)

    try:
        result = requests.get(f'http://api.marketstack.com/v1{endpoint}', params)
        response = result.json()

        error = response.get('error', None)

        print(error)

        if error:
            raise Exception

        next_offset = offset + response['pagination']['count']
        data = initial + [transform(item) for item in response['data']]
        logger.info(f'Collected {len(data)} items.')

        if next_offset < response['pagination']['total']:
            logger.info('Fetching more.')
            return paginated_fetch(endpoint=endpoint, query_params=query_params, transform=transform, offset=next_offset, initial=data)

        return data
    except RequestException:
        logger.error('Request to marketstack threw an exception, returning initial dataset.')
        return initial
    except:
        logger.error('An unknown error occurred, returning initial dataset.')
        return initial


def transform_report(report):
    default_date = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%z")
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
        "timestamp": datetime.strptime(report.get('date', default_date), "%Y-%m-%dT%H:%M:%S%z")
    }
    return Report(**data)


def transform_asset(asset):
    data = {
        "exchange_id": "XNAS",
        "name": asset['name'],
        "symbol": asset['symbol'],
    }
    return Asset(**data)
