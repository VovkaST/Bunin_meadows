import datetime
import logging

from bm_site.exceptions import DuplicateKeyError
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
            try:
                self.insert_record(record_data=record_data)
            except DuplicateKeyError:
                pass
        self.logger.info(f'Parsing completed. Added {self.save_results["added"]} new records.\n')




