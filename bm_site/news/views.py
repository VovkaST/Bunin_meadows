from datetime import datetime

from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from .models import ExchangeRates, EmergencyWarnings, News


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # test_date = datetime.strptime('19.06.2020', '%d.%m.%Y')
        context['data'] = {
            'euro': ExchangeRates.objects.filter(currency='EUR', rate_date__lte=datetime.now()).first(),
            'dollar': ExchangeRates.objects.filter(currency='USD', rate_date__lte=datetime.now()).first(),
            'emergency': EmergencyWarnings.objects.filter(pub_date__date=datetime.now()),
            'main_news': News.objects.filter(image__isnull=False)[:4]
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
