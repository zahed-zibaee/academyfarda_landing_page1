# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-21 14:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_auto_20200921_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2120, 8, 28, 17, 51, 7, 326466)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 21, 17, 51, 7, 331675), editable=False),
        ),
    ]