# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Score


# Register your models here.
@admin.register(Score)
class Score_admin(admin.ModelAdmin):
    list_display=["id","name","family","id_card","score_t1","score_t2","score_a1","score_a2","code_govahi","confirmation"]