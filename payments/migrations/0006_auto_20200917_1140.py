# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-17 07:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20200916_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2120, 8, 24, 11, 40, 18, 329350)),
        ),
        migrations.RemoveField(
            model_name='discount',
            name='product',
        ),
        migrations.AddField(
            model_name='discount',
            name='product',
            field=models.ManyToManyField(to='payments.Product'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 11, 40, 18, 334043), editable=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='ref_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
