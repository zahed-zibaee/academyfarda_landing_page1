# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import * 
from time import sleep


@admin.register(Sent)
class Sent_admin(admin.ModelAdmin):

    def check_sms_status(self, request, queryset):
        rows_updated = 0
        for item in queryset:
            if rows_updated >= 50:
                break
            if item.gone == True and item.status != None:
                try:
                    status = int(item.status)
                except:
                    pass
                if status <= 5:
                    item.check_status()
                    rows_updated += 1
        if rows_updated == 1:
            message_bit = "1 status was"
        elif rows_updated == 0:
            message_bit = "0 statuses was"
        else:
            message_bit = "%s statuses were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)
        
    check_sms_status.short_description = "Check selected SMS status"
    list_display = ('id',"user",'receptor',"message","created_date","gone","get_status_display")
    list_display_links = ['user','receptor']
    actions = [check_sms_status]

@admin.register(Verify)
class Verify_admin(admin.ModelAdmin):

    def get_sent_receptor(self, obj):
        if obj.sent:
            return obj.sent.receptor
        else:
            return ""

    def get_sent_message(self, obj):
        if obj.sent:
            return obj.sent.message
        else:
            return ""

    get_sent_receptor.short_description = "Receptor"
    get_sent_message.short_description = "Message"
    list_display = (
        'id',
        'get_sent_receptor',
        "get_sent_message",
        "status",
        )
    list_display_links = ['get_sent_receptor',]
    raw_id_fields = ("sent",)
    
