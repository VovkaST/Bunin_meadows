# Generated by Django 2.2 on 2020-06-13 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_emergencywarnings'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencywarnings',
            name='description',
            field=models.CharField(max_length=1000, null=True, verbose_name='Описание'),
        ),
    ]
