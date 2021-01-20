# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-11-11 07:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0016_auto_20201110_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='personal_info_old',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personal_info_old', to='payments.PersonalInformation'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2120, 10, 18, 10, 43, 35, 781603)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 10, 43, 35, 789788), editable=False),
        ),
    ]