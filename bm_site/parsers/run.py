from parsers.moscow_mchs_ru import EmergencyWarningsParser
from parsers.iss_moex_com import CurrencyParser

if __name__ == '__main__':
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bm_site.settings.dev')
    django.setup()

    for json_parser in [CurrencyParser]:
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
