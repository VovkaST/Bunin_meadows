import logging.config
import datetime
import pytz
import re
import requests
from bs4 import BeautifulSoup, Tag
from parser import Parser


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
            record = self.db_model(**record_data)
            record.save()
        self.logger.info('Parsing completed.\n')


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






# RSS_URL = 'https://moscow.mchs.ru/deyatelnost/press-centr/operativnaya-informaciya/shtormovye-i-ekstrennye-preduprezhdeniya/rss1'
# re_link = re.compile(pattern=r'<(\/)?(link)>', flags=re.IGNORECASE)
#
# session = requests.Session()
# # session.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) '
# #                                  'Chrome/79.0.3945.117 YaBrowser/20.2.0.1043 Yowser/2.5 Safari/537.36',
# #                    'accept-language': 'ru,en;q=0.9',
# #                    }
# try:
#     response = session.get(url=RSS_URL)
#     if response.status_code == 200:
#         cleaned_text = re.sub(pattern=re_link, repl=r'<\1source_\2>', string=response.text)
#         bs = BeautifulSoup(cleaned_text, features='lxml')
#         record = {}
#         for item in bs.select('item'):
#             for tag in item.children:
#                 if not isinstance(tag, Tag):
#                     continue
#                 if tag.name in ('title', 'source_link', 'yandex:full-text'):
#                     record[tag.name] = tag.text.strip()
#                 elif tag.name == 'pubdate':
#                     record['pub_date'] = datetime.datetime.strptime(tag.text, '%a, %d %b %Y %H:%M:%S MSK')
#                 elif tag.name == 'enclosure':
#                     record['enc_link'] = tag.attrs.get('url')
#                     record['enc_length'] = tag.attrs.get('length')
#                     record['enc_type'] = tag.attrs.get('type')
#             break
#         pprint(record)
#     else:
#         response.raise_for_status()
# except Exception as exc:
#     print(exc.args[0])