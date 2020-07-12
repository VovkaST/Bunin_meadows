import logging
import pathlib
from datetime import datetime
from bm_site.settings.base import NEWSFEED_ROOT
from parsers.parser import Parser


class MosRuParser(Parser):
    """ Парсер новостей mos.ru """

    logger = logging.getLogger('mos.ru')
    URL = 'https://www.mos.ru/aisearch/frontend/api/v1/search/newsfeed/'

    def __init__(self):
        super().__init__()
        self.request_data = {
            'q': 'бутово',
            'page': '2',
            'pagesize': '20',
        }
        self.source = 'mos.ru'
        from news.models import News
        MosRuParser.db_model = News

    def parse(self):
        assert isinstance(self.json_response, dict)
        for article in self.json_response['results']:
            article_id = article.get('id')
            image = article.get('image')
            image_path = None
            if image:
                image_path = NEWSFEED_ROOT / article_id
                success, error = self.save_file_from_url(url=article.get('image'), path=image_path)
                if success:
                    file_name = article.get('image').split('/')[-1]
                    image_path = f'{article_id}/{file_name}'
                else:
                    image_path = None
                    self.logger.error(f'Article ({article_id}) image save error: {error}')
            record_data = {
                'id': article_id,
                'source': self.source,
                'dirty_data': article,
                'title': article.get('title'),
                'image': image_path,
                'url': article.get('url'),
                'created_at': self.datetime_with_tzone(dtime=datetime.fromtimestamp(article.get('created_at'))),
                'last_modified': self.datetime_with_tzone(dtime=datetime.fromtimestamp(article.get('last_modified'))),
            }
            try:
                record = self.db_model.objects.filter(id=article_id).first()
                if not record:
                    self.insert_record(**record_data)
                else:
                    if record_data['last_modified'] > record.last_modified:
                        for field in ['id', 'source']:
                            record_data.pop(field)
                        self.update_record(record=record, record_data=record_data)

            except Exception as exc:
                self.logger.error(f'Parsing error: {exc.strerror or exc.args[0]}')
        log_str = 'Parsing completed. Added {} new records, {} skipped due to duplication, {} updated.\n'
        self.logger.info(log_str.format(self.save_results['added'],
                                        self.save_results['duplicates'],
                                        self.save_results['updated']))



