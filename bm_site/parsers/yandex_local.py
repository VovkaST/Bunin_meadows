import logging
from django.core.exceptions import ObjectDoesNotExist
from parsers.parser import Parser


class YandexLocalParser(Parser):

    logger = logging.getLogger('cached_sites')
    URL = 'https://local.yandex.ru/api/page/moscow/yuzhnoye-butovo'

    def __init__(self):
        super().__init__()
        from news.models import SitesDataCaches
        YandexLocalParser.db_model = SitesDataCaches
        self.source = 'local.yandex.ru'

    def parse(self):
        assert isinstance(self.json_response, dict)
        try:
            cache = self.db_model.objects.get(source=self.source)
            self.update_record(record=cache, record_data=self.json_response)
        except ObjectDoesNotExist:
            record_data = {
                'source': self.source,
                'dirty_data': self.json_response
            }
            self.insert_record(**record_data)
        self.logger.info('{} bytes of data cached.\n'.format(self.content_length))
