# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-21 14:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_auto_20200921_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2120, 8, 28, 17, 48, 45, 81773)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 21, 17, 48, 45, 86649), editable=False),
        ),
    ]
