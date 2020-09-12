# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import * 

# Register your models here.
@admin.register(TextSave)
class TextSave_admin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links = ['name',]
@admin.register(Sent)
class Sent_admin(admin.ModelAdmin):
    list_display = ('id',"user",'receptor',"text","created_date","gone","get_status_display")
    list_display_links = ['user','receptor']
@admin.register(Verify)
class Verify_admin(admin.ModelAdmin):
    list_display = ('id','sent',"ip","get_status_display")
    list_display_links = ['sent',]
    raw_id_fields = ("sent",)
    
