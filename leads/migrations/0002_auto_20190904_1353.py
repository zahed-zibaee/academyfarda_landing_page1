# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-04 09:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Leads',
            new_name='Lead',
        ),
    ]
