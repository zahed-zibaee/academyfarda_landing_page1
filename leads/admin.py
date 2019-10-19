# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Lead, Token, Comment, LabelDefinition, Label
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.contrib.admin import DateFieldListFilter
from datetime import datetime
import csv

class Labels_inline(admin.StackedInline):
    model = Label  
    extra = 0
class Comments_inline(admin.StackedInline):
    model = Comment  
    extra = 0
    readonly_fields = ['author']

@admin.register(Label)
class Label_admin(admin.ModelAdmin):
    #make post field chose base
    raw_id_fields = ("post",)
    list_display = ('id','post','colored_name',)

@admin.register(LabelDefinition)
class LabelDefinition(admin.ModelAdmin):
    #make post field chose base
    radio_fields = {'color_code': admin.HORIZONTAL}
    list_display = ('id','colored_name','color_code',)

admin.site.register(Token)
@admin.register(Lead)
class Lead_admin(admin.ModelAdmin):
    #TODO: add action to change operator, operator view, filter make for all admin objs, inline object in leads
    inlines = [Labels_inline, Comments_inline,]
    def save_formset(self, request, form, formset, change):
        #TODO: change marketing previlages
        if request.user.is_superuser:
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.author = request.user
                instance.save()
            formset.save_m2m()
        elif change:
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:
                pass
            for instance in instances:
                instance.author = request.user
                instance.save()
            formset.save_m2m()
        else:
            pass
    #TODO: date range
    #limit show up content
    list_per_page = 50
    #search field
    search_fields = ('phone_number', 'name_and_family', 'question')
    #calumn value on Lead
    list_display = ['id','name_and_family','phone_number','gender','led_time_jalali_str', \
        'origin','register_status','question']
    #calumn value on Lead get 
    list_display_links = ['name_and_family',]
    #make editable 
    list_editable = ['register_status','gender',]
    #to filter by date 
    list_filter = (
        ('led_time', DateFieldListFilter,),
        'register_status',
        'origin',
    )
    #define actions
    actions = ['csv_export','delete_selected']
    #marketing users have no actions permitions
    def get_actions(self, request):
        actions = super(Lead_admin, self).get_actions(request)
        if request.user.groups.filter(name__in=['marketing']).exists():
            pass
            #del actions['csv_export']
        return actions
    #marketing users can't change name_and_family, phone_number and description
    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['marketing']).exists():
            if 'name_and_family' not in form.changed_data  \
                    and 'phone_number' not in form.changed_data  \
                    and 'question' not in form.changed_data:
                super(Lead_admin, self).save_model(request, obj, form, change)
            else:
                pass
        else:
            super(Lead_admin, self).save_model(request, obj, form, change)
    #for export as csv
    #TODO: need to be modified
    def csv_export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}_{}.csv' \
            .format("Leads-Export", datetime.now().strftime("%Y-%m-%d_%H-%M"))
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
            smart_str(u"ID"),
            smart_str(u"Origin"),
            smart_str(u"Name"),
            smart_str(u"Phone"),
            smart_str(u"Gender"),
            smart_str(u"Led Time"),
            smart_str(u"Registered"),
            smart_str(u"Question"),
            ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.id),
                smart_str(obj.origin),
                smart_str(obj.name_and_family),
                smart_str(obj.phone_number),
                smart_str(obj.gender),
                smart_str(obj.led_time),
                smart_str(obj.register_status),
                smart_str(obj.question),
            ])
        return response

    csv_export.short_description = u"Export Selected"
    actions = ["csv_export"]
    ####################################
    

@admin.register(Comment)
class Comment_admin(admin.ModelAdmin):
    #calumn value on Lead
    list_display = ['id','author','post','created_date_jalali_str','approved_comment','text']
    #calumn value on Lead get 
    list_display_links = ['author',]
    #make editable
    list_editable = ['approved_comment',]
    #limit show up content
    list_per_page = 50
    #search field
    search_fields = ("post__phone_number",'post__name_and_family','text')
    #to filter by date 
    list_filter = (
        ('created_date', DateFieldListFilter,),
        'author',
        'approved_comment',
    )
    #make post field chose base
    raw_id_fields = ("post",)
    #marketing users can't change data
    readonly_fields = ['author']

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.author = request.user
            super(Comment_admin, self).save_model(request, obj, form, change)
        elif change and 'author' not in form.changed_data \
            and 'post' not in form.changed_data \
                and 'text' not in form.changed_data \
                    and  obj.author == request.user:
            super(Comment_admin, self).save_model(request, obj, form, change)
        elif request.user.groups.filter(name__in=['marketing']).exists():
            if not change:
                obj.author = request.user
                super(Comment_admin, self).save_model(request, obj, form, change)
        else:
            pass
    #define actions
    actions = ['delete_selected']
    #marketing users have no actions permitions
    def get_actions(self, request):
        actions = super(Comment_admin, self).get_actions(request)
        if request.user.groups.filter(name__in=['marketing']).exists():
            del actions['delete_selected']
        return actions
