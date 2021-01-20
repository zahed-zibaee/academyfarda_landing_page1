# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-21 14:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0010_auto_20200921_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sent',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 21, 17, 49, 48, 889739), editable=False),
        ),
        migrations.AlterField(
            model_name='verify',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 21, 17, 54, 48, 890482), editable=False),
        ),
        migrations.AlterField(
            model_name='verify',
            name='token1',
            field=models.CharField(default='136', max_length=3),
        ),
        migrations.AlterField(
            model_name='verify',
            name='token2',
            field=models.CharField(default='780', max_length=3),
        ),
    ]