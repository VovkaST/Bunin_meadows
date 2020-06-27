import logging.config
import datetime
import pytz
import re
import requests
from bs4 import BeautifulSoup, Tag

from bm_site.exceptions import DuplicateKeyError
from parsers.parser import Parser


class EmergencyWarningsParser(Parser):
    """ Парсер штормовых и экстренных предупреждений МЧС г. Москвы  """

    logger = logging.getLogger('moscow.mchs.ru')
    URL = 'https://moscow.mchs.ru/deyatelnost/press-centr/operativnaya-informaciya/' \
          'shtormovye-i-ekstrennye-preduprezhdeniya/rss'
    re_link = re.compile(pattern=r'<(\/)?(link)>', flags=re.IGNORECASE)

    def __init__(self):
        super().__init__()
        from news.models import EmergencyWarnings
        EmergencyWarningsParser.db_model = EmergencyWarnings

    def clean_html(self):
        assert isinstance(self.response, requests.models.Response)
        self.response = re.sub(pattern=EmergencyWarningsParser.re_link, repl=r'<\1source_\2>',
                               string=self.response.text)

    def parse(self):
        assert isinstance(self.bs_response, BeautifulSoup)
        for item in self.bs_response.select('item'):
            record_data = {}
            for tag in item.children:
                if not isinstance(tag, Tag):
                    continue
                if tag.name in ('title', 'source_link'):
                    record_data[tag.name] = tag.text.strip()
                elif tag.name == 'yandex:full-text':
                    record_data['full_text'] = tag.text.strip()
                elif tag.name == 'pubdate':
                    date = datetime.datetime.strptime(tag.text[:25], '%a, %d %b %Y %H:%M:%S')
                    record_data['pub_date'] = pytz.timezone('Europe/Moscow').localize(date)
                elif tag.name == 'enclosure':
                    record_data['enc_link'] = tag.attrs.get('url')
                    record_data['enc_length'] = tag.attrs.get('length')
                    record_data['enc_type'] = tag.attrs.get('type')
            try:
                self.insert_record(record_data=record_data)
            except DuplicateKeyError:
                pass
        log_str = 'Parsing completed. Added {} new records, {} skipped due to duplication.\n'
        self.logger.info(log_str.format(self.save_results['added'], self.save_results['duplicates']))
