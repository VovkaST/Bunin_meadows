from news_articles import MosRuParser
from moscow_mchs_ru import EmergencyWarningsParser
from iss_moex_com import CurrencyParser
from yandex_local import YandexLocalParser

if __name__ == '__main__':
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bm_site.settings.dev')
    django.setup()

    for json_parser in [CurrencyParser, MosRuParser, YandexLocalParser]:
        parser = json_parser()
        if parser.request_json():
            parser.parse()
        else:
            parser.logger.info('Parsing is finished with errors.\n')

    for xml_parser in [EmergencyWarningsParser]:
        parser = xml_parser()
        if parser.request_xml():
            parser.parse()
        else:
            parser.logger.info('Parsing is finished with errors.\n')

    # for json_parser in [YandexLocalParser]:
    #     parser = json_parser()
    #     if parser.request_json():
    #         parser.parse()
    #     else:
    #         parser.logger.info('Parsing is finished with errors.\n')



