import logging.config
import requests
from bs4 import BeautifulSoup
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

    def _request(self, url, features):
        """
        Метод отправляет запрос к источнику и преобразует ответ в объект BeautifulSoup4, присваивая его
        атрибуту self.bs_response. Чистый ответ хранится в атрибуте self.response. Факт сетевой активности
        записывается в лог self.logger (по умолчанию используется handler_parser).

        :param url: Адрес источника данных
        :param features: Используемый парсер
        :return Boolean: Успешность выполнения запроса к источнику данных
        """
        try:
            self.logger.info(f'Sending request {self.URL}')
            self.response = self.session.get(url=url)
            self.logger.info('Response received.')
            if self.response.status_code != 200:
                self.response.raise_for_status()
            self.clean_html()
            self.bs_response = BeautifulSoup(self.response, features=features)
            return True
        except Exception as exc:
            self.logger.error(exc.args[0])
            return False

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

    def clean_html(self):
        """ Метод для предварительной обработки полученных от источника данных (при необходимости) """
        pass

    def parse(self):
        """ Метод непосредственно парсинга (для каждого парсера индивидуален) """
        pass
