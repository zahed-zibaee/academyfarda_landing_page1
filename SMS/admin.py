# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import * 

# Register your models here.
@admin.register(TextSave)
class TextSave_admin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links = ['name',]

def check_status(self, request, queryset):
    rows_updated = queryset.update(check_status())
    if rows_updated == 1:
        message_bit = "1 status was"
    else:
        message_bit = "%s statuses were" % rows_updated
    self.message_user(request, "%s successfully updated." % message_bit)
    
check_status.short_description = "Check selected SMS status"

@admin.register(Sent)
class Sent_admin(admin.ModelAdmin):
    list_display = ('id',"user",'receptor',"text","created_date","gone","get_status_display")
    list_display_links = ['user','receptor']
    actions = [check_status]
    
@admin.register(Verify)
class Verify_admin(admin.ModelAdmin):
    list_display = ('id','sent',"ip","get_status_display")
    list_display_links = ['sent',]
    raw_id_fields = ("sent",)
    
