from parsers.moscow_mchs_ru import EmergencyWarningsParser
from parsers.iss_moex_com import CurrencyParser

if __name__ == '__main__':
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bm_site.settings.dev')
    django.setup()

    parser = CurrencyParser()
    if parser.request_json():
        parser.parse()
    else:
        parser.logger.info('Parsing is finished with errors.\n')