import logging.config
import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError

from conf import LOG_CONFIG


class Parser:
    """
    Базовый класс парсера различных данных для сайта. Использует BeautifulSoup4.
    """

    DEFAULT_HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/79.0.3945.117 YaBrowser/20.2.0.1043 Yowser/2.5 Safari/537.36',
                       'accept-language': 'ru,en;q=0.9',
                       }
    URL = None
    logging.config.dictConfig(LOG_CONFIG)
    logger = logging.getLogger('handler_parser')
    db_model = None

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = Parser.DEFAULT_HEADERS
        self.response = None
        self.bs_response = None
        self.json_response = None
        self.save_results = {
            'added': 0,
            'duplicates': 0,
            'other_errors': 0,
        }

    def _request(self, url, features=None, is_json=False):
        """
        Метод отправляет запрос к источнику и преобразует ответ в объект BeautifulSoup4 или json, в зависимости
        от параметра is_json, присваивая его атрибуту self.bs_response. Чистый ответ хранится в атрибуте self.response.
        Факт сетевой активности записывается в лог self.logger (по умолчанию используется handler_parser).

        :param url: Адрес источника данных
        :param str features: Используемый парсер (не используется, если is_json == True)
        :param boolean is_json: Вернуть данные в json
        :return Boolean: Успешность выполнения запроса к источнику данных
        """
        try:
            self.logger.info(f'Sending request {self.URL}')
            self.response = self.session.get(url=url)
            self.logger.info('Response received.')
            if self.response.status_code != 200:
                self.response.raise_for_status()
            if is_json:
                self.json_response = self.response.json()
            else:
                assert features in ('lxml', 'html.parser')
                self.clean_html()
                self.bs_response = BeautifulSoup(self.response, features=features)
            return True
        except Exception as exc:
            self.logger.error(exc.args[0])
            return False

    def _save_data(self, record_data):
        """
        Сохранить строку в БД. Результат сохранения записываются в словарь-счетчик результатов self.save_results,
        текст ошибок также записывается в лог.

        :param dict record_data: Данные для записи в БД. Ключами должны быть имена полей БД,
        значениями - данные для вставки.
        """
        try:
            record = self.db_model(**record_data)
            record.save()
            self.save_results['added'] += 1
        except IntegrityError as exc:
            if 'duplicate key value' in exc.args[0]:
                self.save_results['duplicates'] += 1
            else:
                self.logger.error(f'Save error: {exc.args[0]}')
                self.save_results['other_errors'] += 1
        except Exception as exc:
            self.logger.error(f'Save error: {exc.args[0]}')
            self.save_results['other_errors'] += 1

    def request_xml(self):
        """
        Получение данных через lxml-парсер.

        :return Boolean: Успешность выполнения запроса к источнику данных
        """
        return self._request(url=self.URL, features='lxml')

    def request_html(self):
        """
        Получение данных через html.parser-парсер.

        :return Boolean: Успешность выполнения запроса к источнику данных
        """

        return self._request(url=self.URL, features='html.parser')

    def request_json(self):
        """
        Получение данных в виде json.

        :return Boolean: Успешность выполнения запроса к источнику данных
        """

        return self._request(url=self.URL, is_json=True)

    def clean_html(self):
        """ Метод для предварительной обработки полученных от источника данных (при необходимости) """
        pass

    def parse(self):
        """ Метод непосредственно парсинга (для каждого парсера индивидуален) """
        pass
