# Generated by Django 2.2 on 2020-06-28 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0019_auto_20200628_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления импортом'),
        ),
    ]
