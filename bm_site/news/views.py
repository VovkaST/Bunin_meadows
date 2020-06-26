from datetime import datetime

from django.views.generic import TemplateView
from .models import ExchangeRates, EmergencyWarnings


class NewsView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # test_date = datetime.strptime('19.06.2020', '%d.%m.%Y')
        context['data'] = {
            'euro': ExchangeRates.objects.filter(currency='EUR', rate_date__lte=datetime.now()).first(),
            'dollar': ExchangeRates.objects.filter(currency='USD', rate_date__lte=datetime.now()).first(),
            'emergency': EmergencyWarnings.objects.filter(pub_date__date=datetime.now()),
        }
        return context['data']
