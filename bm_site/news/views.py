from datetime import datetime

from django.views.generic import TemplateView
from .models import ExchangeRates


class NewsView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = {
            'euro': ExchangeRates.objects.filter(currency='EUR', rate_date__lte=datetime.now()).first(),
            'dollar': ExchangeRates.objects.filter(currency='USD', rate_date__lte=datetime.now()).first()
        }
        return context['data']
