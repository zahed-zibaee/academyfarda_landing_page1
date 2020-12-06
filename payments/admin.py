# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import *

from persiantools.jdatetime import JalaliDateTime
from time import sleep

# Register your models here.
@admin.register(Teacher)
class Teacher_admin(admin.ModelAdmin):
    list_display = ('id', "family", 'name')
    list_display_links = ['family',]

@admin.register(PersonalInformation)
class PersonalInformation_admin(admin.ModelAdmin):
    list_display = ('id', 'name', "family", "gender", "father_name",\
                    "code_meli", "phone_number")
    list_display_links = ['name',"family"]

def resend_receipt(self, request, queryset):
    rows_updated = 0
    for item in queryset:
        if item.status == True:
            sleep(0.5)
            item.send_receipt_course()
            rows_updated += 1
    if rows_updated == 1:
        message_bit = "1 receipt"
    else:
        message_bit = "%s receipts" % rows_updated
    self.message_user(request, "%s sent." % message_bit)
    
resend_receipt.short_description = "Resend receipt"

@admin.register(Payment)
class Payment_admin(admin.ModelAdmin):
    
    def personal_info_get_name(self, obj):
        if obj.personal_info:
            return u"" + obj.personal_info.name + " " + obj.personal_info.family 
        elif obj.cart and obj.cart.personal_info_old:
            return u"" + obj.cart.personal_info_old.name + " "\
                   + obj.cart.personal_info_old.family 
        else:
            return ""

    def personal_info_get_phone(self, obj):
        if obj.personal_info:
            return u"" + obj.personal_info.phone_number
        elif obj.cart and  obj.cart.personal_info_old:
            return u"" + obj.cart.personal_info_old.phone_number
        else:
            return ""
            


    def operator_get_name(self, obj):
        if obj.operator:
            return u"" + obj.operator.first_name + " "  + obj.operator.last_name
        else:
            return ""

    def get_date(self, obj):
        return u"" + JalaliDateTime(obj.created_date).strftime("%Y/%m/%d")

    def get_time(self, obj):
        return u"" + JalaliDateTime(obj.created_date).strftime("%H:%M:%S")
    
    def get_cart_course_get_name(self, obj):
        if obj.cart and len(obj.cart.course.all()) == 1:
            return u"" + obj.cart.course.all().first().get_name()
        else:
            return ""

    def get_cart_discount_code(self, obj):
        if obj.cart and len(obj.cart.discount.all()) == 1:
            return u"" + obj.cart.discount.all().first().code
        else:
            return ""

    personal_info_get_name.short_description = 'Name'
    personal_info_get_phone.short_description = 'Phone'
    operator_get_name.short_description = "Operator"
    get_date.short_description = "Date"
    get_time.short_description = "Time"
    get_cart_course_get_name.short_description = "Course"
    get_cart_discount_code.short_description = "Discount"
    list_display = ('id', "personal_info_get_name", "personal_info_get_phone",\
                    "get_cart_course_get_name", "get_cart_discount_code",\
                    "operator_get_name", "total", "get_date",\
                    "get_time", "status", "ref_id", "send_receipt")
    list_display_links = ["personal_info_get_name"]
    raw_id_fields = ("verification","cart","personal_info","operator")
    list_filter = (
        ('created_date', DateFieldListFilter,),
        'status',
        "send_receipt",

    )
    search_fields = ("id",'ref_id')
    actions = [resend_receipt]
@admin.register(Cart)
class Cart_admin(admin.ModelAdmin):
    list_display = ('id', "get_courses", "get_discounts")
    list_display_links = ["id"]
    raw_id_fields = ("personal_info_old",)
@admin.register(Discount)
class Discount_admin(admin.ModelAdmin):
    list_display = ('id', "name", "code", "amount", "expiration_time", "active")
    list_display_links = ["name"]
@admin.register(Course)
class Course_admin(admin.ModelAdmin):
    list_display = ('id',"get_name","show","price","active")
    list_display_links = ["get_name"]