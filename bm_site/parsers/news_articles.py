import logging
from pprint import pprint

from parsers.parser import Parser


class MosRuParser(Parser):
    """ Парсер новостей mos.ru """

    logger = logging.getLogger('mos.ru')
    URL = 'https://www.mos.ru/aisearch/frontend/api/v1/search/newsfeed/'

    def __init__(self):
        super().__init__()
        self.data = {
            'q': 'бутово',
            'page': '1',
            'pagesize': '20',
        }
        from news.models import News
        MosRuParser.db_model = News

    def parse(self):
        assert isinstance(self.json_response, dict)
        pprint(self.json_response['results'])


