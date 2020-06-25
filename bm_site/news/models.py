from django.db import models
from django.utils import timezone

from .app_settings import DB_PREFIX


class ExchangeRates(models.Model):
    """ Волатильность курса валют (Доллар США, Евро) """
    currency = models.CharField(max_length=3, default='', verbose_name='Валюта')
    rate = models.FloatField(default=0, verbose_name='Курс валюты')
    rate_volatility = models.FloatField(default=0, verbose_name='Изменение курса')
    rate_date = models.DateField(default=timezone.now, verbose_name='Дата курса')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время импорта')

    def __str__(self):
        return f'{self.currency} - {self.rate}'

    class Meta:
        db_table = f'{DB_PREFIX}_exchange_rate'
        ordering = ['-rate_date', 'currency', '-imported_at']
        verbose_name = 'Курсы валют'
        unique_together = ['currency', 'rate', 'rate_date']


class EmergencyWarnings(models.Model):
    """ Штормовые и экстренные предупреждения МЧС г. Москвы """
    pub_date = models.DateTimeField(verbose_name='Дата публикации', unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок сообщения')
    description = models.CharField(max_length=1000, null=True, verbose_name='Описание')
    source_link = models.CharField(max_length=1000, verbose_name='Ссылка на первоисточник')
    full_text = models.CharField(max_length=4000, verbose_name='Текст сообщения')
    enc_link = models.CharField(max_length=2000, null=True, verbose_name='Ссылка на вложение')
    enc_length = models.IntegerField(default=0, verbose_name='Размер вложения')
    enc_type = models.CharField(max_length=50, null=True, verbose_name='Тип вложение')
    imported_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время импорта')

    def __str__(self):
        return f'{self.pub_date.strftime("%Y-%m-%d %H:%M")} - {self.title}'

    class Meta:
        db_table = f'{DB_PREFIX}_emergency_warnings'
        ordering = ['-pub_date']
        verbose_name = 'Предупреждения МЧС г.Москвы'
