from django.contrib import admin
from .models import ExchangeRates, EmergencyWarnings


@admin.register(ExchangeRates)
class ExchangeRatesAdmin(admin.ModelAdmin):
    pass


@admin.register(EmergencyWarnings)
class EmergencyWarningsAdmin(admin.ModelAdmin):
    pass
