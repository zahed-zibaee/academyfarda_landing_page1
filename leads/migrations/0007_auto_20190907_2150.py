# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-07 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0006_auto_20190907_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='token',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.Token'),
        ),
    ]
