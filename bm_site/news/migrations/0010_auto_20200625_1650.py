# Generated by Django 2.2 on 2020-06-25 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_auto_20200625_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerates',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
