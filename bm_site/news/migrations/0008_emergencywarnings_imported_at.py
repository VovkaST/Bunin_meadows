# Generated by Django 2.2 on 2020-06-25 09:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20200614_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencywarnings',
            name='imported_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата и время импорта'),
            preserve_default=False,
        ),
    ]