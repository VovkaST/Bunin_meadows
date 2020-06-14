import logging.config
import requests
from bs4 import BeautifulSoup
from conf import LOG_CONFIG


class Parser:
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
        return self._request(url=self.URL, features='lxml')

    def request_html(self):
        return self._request(url=self.URL, features='html.parser')

    def clean_html(self):
        pass

    def parse(self):
        pass
