# Generated by Django 2.0.7 on 2018-07-11 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180711_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_registration',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 11, 15, 34, 6, 347708), verbose_name='User registration date'),
        ),
    ]
