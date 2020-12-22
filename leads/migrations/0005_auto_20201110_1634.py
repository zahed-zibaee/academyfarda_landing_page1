# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-11-10 13:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0004_auto_20201110_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 10, 16, 34, 37, 619661), editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date_jalali',
            field=models.CharField(default='1399-08-20 16:34:37', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date_jalali_str',
            field=models.CharField(default='Seshanbeh 20 Aban 1399 16:34:37', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='label',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 10, 16, 34, 37, 621370), editable=False),
        ),
        migrations.AlterField(
            model_name='label',
            name='created_date_jalali',
            field=models.CharField(default='1399-08-20 16:34:37', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='label',
            name='created_date_jalali_str',
            field=models.CharField(default='Seshanbeh 20 Aban 1399 16:34:37', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='lead',
            name='led_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 10, 16, 34, 37, 616878), editable=False),
        ),
        migrations.AlterField(
            model_name='lead',
            name='led_time_jalali',
            field=models.CharField(default='1399-08-20 16:34:37', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='lead',
            name='led_time_jalali_str',
            field=models.CharField(default='Seshanbeh 20 Aban 1399 16:34:37', editable=False, max_length=50),
        ),
    ]
