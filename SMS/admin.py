# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from persiantools.jdatetime import JalaliDateTime

from .models import * 


@admin.register(Sent)
class Sent_admin(admin.ModelAdmin):

    def get_jalali_send_date(self, obj):
        return  JalaliDateTime(
            obj.send_date.astimezone(timezone.get_default_timezone())
            ).strftime("%Y/%m/%d %H:%M:%S")

    def get_status_code(self, obj):
        try:
            return obj.get_status_code_display()
        except:
            return obj.status_code

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
            message_bit = "0 status was"
        else:
            message_bit = "%s statuses were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)

    def resend_sms(self, request, queryset):
        rows_updated = 0
        for item in queryset:
            item.send()
            rows_updated += 1
        if rows_updated == 1:
            message_bit = "1 SMS successfully sent"
        elif rows_updated == 0:
            message_bit = "0 SMS sent"
        else:
            message_bit = "%s SMSs were" % rows_updated
        self.message_user(request, "%s successfully sent." % message_bit)

    get_status_code.short_description="Status"
    get_jalali_send_date.short_description="Send date time"
    resend_sms.short_description = "Send or Resend selected SMSs"
    check_sms_status.short_description = "Check selected SMSs status"
    list_display = (
        'id',
        "user",
        'receptor',
        "message",
        "get_jalali_send_date",
        "gone","get_status_code"
        )
    list_display_links = ['user','receptor']
    actions = [check_sms_status, resend_sms]

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
    
