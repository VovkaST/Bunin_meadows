import os
from bm_site.settings.base import BASE_DIR

PARSERS_DIR = os.path.dirname(os.path.abspath(__file__))
PARSERS_LOG_DIR = os.path.join(BASE_DIR, PARSERS_DIR, 'log')

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'parsing_log': {
            'format': '%(asctime)s %(levelname)s: %(message)s',
            'datefmt': '%Y-%d-%m %H:%M:%S'
        },
    },
    'handlers': {
        'handler_parser': {
            'class': 'logging.FileHandler',
            'formatter': 'parsing_log',
            'filename': os.path.join(PARSERS_LOG_DIR, 'parser.log'),
            'encoding': 'UTF-8'
        },
        'handler_moscow.mchs.ru': {
            'class': 'logging.FileHandler',
            'formatter': 'parsing_log',
            'filename': os.path.join(PARSERS_LOG_DIR, 'moscow.mchs.ru.log'),
            'encoding': 'UTF-8'
        },
        'handler_iss.moex.com': {
            'class': 'logging.FileHandler',
            'formatter': 'parsing_log',
            'filename': os.path.join(PARSERS_LOG_DIR, 'iss.moex.com.log'),
            'encoding': 'UTF-8'
        },
        # 'handler_errors': {
        #     'class': 'logging.FileHandler',
        #     'formatter': 'request_log',
        #     'filename': os.path.join(PARSERS_LOG_DIR, 'errors.log'),
        #     'encoding': 'UTF-8',
        #     'delay': True
        # },
    },
    'loggers': {
        'default': {
            'handlers': ['handler_parser'],
            'level': 'INFO',
        },
        'moscow.mchs.ru': {
            'handlers': ['handler_moscow.mchs.ru'],
            'level': 'INFO',
        },
        'iss.moex.com': {
            'handlers': ['handler_iss.moex.com'],
            'level': 'INFO',
        },
        # 'level_critical': {
        #     'handlers': ['handler_errors'],
        #     'level': 'CRITICAL',
        # }
    },
}

if not os.path.isdir(PARSERS_LOG_DIR):
    os.mkdir(PARSERS_LOG_DIR)
