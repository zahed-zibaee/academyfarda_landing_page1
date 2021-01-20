# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-15 11:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0002_auto_20200915_1536'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='verification',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_info',
        ),
        migrations.AddField(
            model_name='cart',
            name='payment_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_info', to='payments.PaymentInformation'),
        ),
        migrations.AddField(
            model_name='payment',
            name='verification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SMS.Verify'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discount',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2120, 8, 22, 15, 36, 8, 533049)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 15, 15, 36, 8, 537842), editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]