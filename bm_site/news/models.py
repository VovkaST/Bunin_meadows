from django.db import models
from .app_settings import DB_PREFIX


class ExchangeRates(models.Model):
    """ Волатильность курса валют (Доллар США, Евро) """
    dollar_rate = models.FloatField(verbose_name='Курс Доллара')
    dollar_volatility = models.FloatField(verbose_name='Изменение курса Доллара')
    euro_rate = models.FloatField(verbose_name='Курс Евро')
    euro_volatility = models.FloatField(verbose_name='Изменение курса Евро')
    relevance = models.DateTimeField(auto_now_add=True, verbose_name='Актуальность', primary_key=True)

    def __str__(self):
        return f'{self.relevance.strftime("%Y-%m-%d %H:%M")} - \u0024 {self.dollar_rate}, \u20AC {self.euro_rate}'

    class Meta:
        db_table = f'{DB_PREFIX}_exchange_rate'
        ordering = ['-relevance']
        verbose_name = 'Курсы валют'


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

    def __str__(self):
        return f'{self.pub_date.strftime("%Y-%m-%d %H:%M")} - {self.title}'

    class Meta:
        db_table = f'{DB_PREFIX}_emergency_warnings'
        ordering = ['-pub_date']
        verbose_name = 'Предупреждения МЧС'
