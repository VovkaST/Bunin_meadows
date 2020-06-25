import datetime
import logging
from django.db import IntegrityError
from parsers.parser import Parser


class CurrencyParser(Parser):
    """ Парсер курсов валюты """

    logger = logging.getLogger('iss.moex.com')
    URL = 'https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json'

    def __init__(self):
        super().__init__()
        from news.models import ExchangeRates
        CurrencyParser.db_model = ExchangeRates

    def parse(self):
        assert isinstance(self.json_response, dict)
        added = 0
        columns = self.json_response['cbrf']['columns']
        values = self.json_response['cbrf']['data'][0]
        data = dict(zip(columns, values))
        for currency in ['USD', 'EUR']:
            record_data = {
                'currency': currency,
                'rate': data.get(f'CBRF_{currency}_LAST'),
                'rate_volatility': data.get(f'CBRF_{currency}_LASTCHANGEPRCNT'),
                'rate_date': datetime.datetime.strptime(data.get(f'CBRF_{currency}_TRADEDATE'), '%Y-%m-%d'),
            }
            prev_currency = self.db_model.objects.filter(currency=currency,
                                                         rate_date__lt=record_data['rate_date']).first()
            if prev_currency and prev_currency.rate > record_data['rate']:
                record_data['rate_volatility'] = 0 - record_data['rate_volatility']
            try:
                record = self.db_model(**record_data)
                record.save()
                added += 1
            except IntegrityError as exc:
                if 'duplicate key value' in exc.args[0]:
                    pass
        self.logger.info(f'Parsing completed. Added {added} new records\n')



