from datetime import datetime
from django.views import generic
from django.views.generic import TemplateView
from .models import ExchangeRates, EmergencyWarnings, News, SitesDataCaches
from bm_site.settings.base import MAIN_NEWS_LINE_LENGTH, LOCALS_PER_PAGE


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # test_date = datetime.strptime('19.06.2020', '%d.%m.%Y')
        local_yandex = SitesDataCaches.objects.get(source='local.yandex.ru').dirty_data
        events = local_yandex['state']['events']

        context['data'] = {
            'euro': ExchangeRates.objects.filter(currency='EUR', rate_date__lte=datetime.now()).first(),
            'dollar': ExchangeRates.objects.filter(currency='USD', rate_date__lte=datetime.now()).first(),
            'emergency': EmergencyWarnings.objects.filter(pub_date__date=datetime.now()),
            'main_news': News.objects.filter(image__isnull=False)[:MAIN_NEWS_LINE_LENGTH],
            'local_yandex': [events[k] for k in sorted(events, reverse=True)][:LOCALS_PER_PAGE]
        }
        return context['data']


class NewsView(generic.DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = {
            'euro': ExchangeRates.objects.filter(currency='EUR', rate_date__lte=datetime.now()).first(),
            'dollar': ExchangeRates.objects.filter(currency='USD', rate_date__lte=datetime.now()).first(),
        }
        return context['data']
