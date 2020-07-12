# Generated by Django 2.2 on 2020-07-12 18:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0023_auto_20200705_2240'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalYandex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dirty_data', django.contrib.postgres.fields.jsonb.JSONField(default=dict, verbose_name='Грязные данные от Яндекса')),
                ('imported_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время импорта')),
            ],
            options={
                'verbose_name': 'Новости с Яндекс.Район',
                'db_table': 'bm_local_yandex',
            },
        ),
    ]
