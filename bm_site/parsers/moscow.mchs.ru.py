import logging.config
import datetime
import pytz
import re
import requests
from bs4 import BeautifulSoup, Tag
from parsers.parser import Parser
from django.db import IntegrityError


class EmergencyWarningsParser(Parser):
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
        added = 0
        duplicates = 0
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
                record = self.db_model(**record_data)
                record.save()
                added += 1
            except IntegrityError as exc:
                if 'duplicate key value' in exc.args[0]:
                    duplicates += 1
                else:
                    self.logger.error(f'Save error: {exc.args[0]}')
        self.logger.info(f'Parsing completed. Added {added} new records, {duplicates} skipped due to duplication.\n')


if __name__ == '__main__':
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bm_site.settings.dev')
    django.setup()

    parser = EmergencyWarningsParser()
    if parser.request_xml():
        parser.parse()
    else:
        parser.logger.info('Parsing is finished with errors.\n')
