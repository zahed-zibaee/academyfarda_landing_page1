# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Lead, Token, Comment
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.contrib.admin import DateFieldListFilter
from datetime import datetime
import csv


# Register your models here.
admin.site.register(Token)
@admin.register(Lead)
class Lead_admin(admin.ModelAdmin):
    #limit show up content
    list_per_page = 50
    #search field
    search_fields = ('phone_number', 'name_and_family', 'description')
    #calumn value on Lead
    list_display = ['id','name_and_family','phone_number','gender','led_time', \
        'token','register_status','description']
    #calumn value on Lead get 
    list_display_links = ['name_and_family',]
    #make editable 
    list_editable = ['register_status','gender',]
    #to filter by date 
    list_filter = (
        ('led_time', DateFieldListFilter,),
        'register_status',
        'token',
    )
    #define actions
    actions = ['csv_export','delete_selected']
    #marketing users have no actions permitions
    def get_actions(self, request):
        actions = super(Lead_admin, self).get_actions(request)
        if request.user.groups.filter(name__in=['marketing']).exists():
            del actions['csv_export']
            del actions['delete_selected']
        return actions
    #marketing users can't change name_and_family, phone_number and description
    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['marketing']).exists():
            if 'name_and_family' not in form.changed_data  \
                    and 'phone_number' not in form.changed_data  \
                    and 'description' not in form.changed_data:
                super(Lead_admin, self).save_model(request, obj, form, change)
            else:
                pass
        else:
            super(Lead_admin, self).save_model(request, obj, form, change)
    #for export as csv
    def csv_export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}_{}.csv' \
            .format("Leads-Export", datetime.now().strftime("%Y-%m-%d_%H-%M"))
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
            smart_str(u"ID"),
            smart_str(u"Token"),
            smart_str(u"Name"),
            smart_str(u"Phone"),
            smart_str(u"Gender"),
            smart_str(u"Led Time"),
            smart_str(u"Registered"),
            smart_str(u"Description"),
            ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.id),
                smart_str(obj.token),
                smart_str(obj.name_and_family),
                smart_str(obj.phone_number),
                smart_str(obj.gender),
                smart_str(obj.led_time),
                smart_str(obj.register_status),
                smart_str(obj.description),
            ])
        return response

    csv_export.short_description = u"Export Selected"
    actions = ["csv_export"]
    ####################################
    #TODO: date range

@admin.register(Comment)
class Comment_admin(admin.ModelAdmin):
    #calumn value on Lead
    list_display = ['id','author','post','created_date','approved_comment','text']
    #calumn value on Lead get 
    list_display_links = ['author',]
    #make editable
    list_editable = ['approved_comment',]
    #limit show up content
    list_per_page = 50
    #search field
    search_fields = ('post__id',"post__phone_number",'post__name_and_family','text')
    #to filter by date 
    list_filter = (
        ('created_date', DateFieldListFilter,),
        'author',
        'approved_comment',
    )
    #marketing users can't change data
    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['marketing']).exists():
            pass
        else:
            super(Comment_admin, self).save_model(request, obj, form, change)
    #define actions
    actions = ['delete_selected']
    #marketing users have no actions permitions
    def get_actions(self, request):
        actions = super(Comment_admin, self).get_actions(request)
        if request.user.groups.filter(name__in=['marketing']).exists():
            del actions['delete_selected']
        return actions