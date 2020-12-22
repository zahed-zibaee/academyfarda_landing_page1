# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-21 13:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20200921_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2120, 8, 28, 16, 56, 29, 238318)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 21, 16, 56, 29, 243847), editable=False),
        ),
    ]
