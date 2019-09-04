# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Lead, Token
import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.contrib.admin import DateFieldListFilter

# Register your models here.
admin.site.register(Token)
@admin.register(Lead)
class Lead_admin(admin.ModelAdmin):
    #limit show up content
    list_per_page = 50
    ########################################
    #search field
    search_fields = ('phone_number', 'name_and_family', 'discription')
    ########################################
    #calumn value on Lead
    list_display = ['id','name_and_family','phone_number','led_time','register_status',]
    ########################################
    #to filter by date 
    list_filter = (
        ('led_time', DateFieldListFilter,),
    )
    ########################################
    #for export as csv
    def csv_export(self, request, queryset):
        meta = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
            smart_str(u"ID"),
            smart_str(u"Name"),
            smart_str(u"Phone"),
            smart_str(u"Gender"),
            smart_str(u"Email"),
            smart_str(u"Led Time"),
            smart_str(u"Registered"),
            smart_str(u"Discription"),
            ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.id),
                smart_str(obj.name_and_family),
                smart_str(obj.phone_number),
                smart_str(obj.gender),
                smart_str(obj.email),
                smart_str(obj.led_time),
                smart_str(obj.register_status),
                smart_str(obj.discription),
            ])
        return response

    csv_export.short_description = u"Export Selected"
    actions = ["csv_export"]
    ####################################
    #TODO: date range
