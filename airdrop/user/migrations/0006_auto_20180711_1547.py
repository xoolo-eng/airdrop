# Generated by Django 2.0.7 on 2018-07-11 12:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20180711_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_registration',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 11, 15, 47, 22, 232310), verbose_name='User registration date'),
        ),
    ]