from django.views.generic import TemplateView
from .models import ExchangeRates


class NewsView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = {'rates': ExchangeRates.objects.first()}
        return context['data']



