import requests

from payment_config.models import DollarExchangeHistory


def get_bcv():
    
    response = requests.get('https://pydolarve.org/api/v1/dollar',
                           params={'page': 'bcv',
                                   'monitor': 'usd',
                                   'format_date': 'iso',
                                   'rounded_price': 'true'})

    if response.status_code == 200:
        bcv = response.json()

        obj = DollarExchangeHistory.objects.create(
            date=bcv['last_update'],
            value=bcv['price'],
            page='Banco Central de Venezuela'
        )
    return {'status_code': response.status_code,
            'obj': obj}