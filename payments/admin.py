# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from persiantools.jdatetime import JalaliDateTime

from .models import *


@admin.register(Discount)
class Discount_admin(admin.ModelAdmin):
    list_display = ('id', "name", "code", "amount", "expiration_time", "active")
    list_display_links = ["name"]


@admin.register(PersonalInformation)
class PersonalInformation_admin(admin.ModelAdmin):
    list_display = (
        'id',
        'name', 
        "family", 
        "phone_number", 
        "gender", 
        "father_name",
        "code_meli",
    )
    list_display_links = ['name',"family"]


@admin.register(CourseDay)
class CourseDay_admin(admin.ModelAdmin):
    list_display = (
        'id',
        'name', 
    )
    list_display_links = ['name',]


@admin.register(CourseType)
class CourseType_admin(admin.ModelAdmin):
    list_display = (
        'id',
        'name', 
    )
    list_display_links = ['name',]


@admin.register(CourseTime)
class CourseTime_admin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'start',
        'end',
    )
    list_display_links = ['name',]


@admin.register(CourseTeacher)
class CourseTeacher_admin(admin.ModelAdmin):

    def personal_info_get_name(self, obj):
        if obj.personal_info:
            return u"" + obj.personal_info.name + " " + obj.personal_info.family 
        else:
            return ""

    personal_info_get_name.short_description="name"
    list_display = (
        'id',
        'personal_info_get_name',
    )
    list_display_links = ['personal_info_get_name',]
    raw_id_fields = ("personal_info",)


#TODO: get names instead of __str__ and make colloms shorter
@admin.register(Course)
class Course_admin(admin.ModelAdmin):

    def week_to_start_per(self, obj):
        if obj.week_to_start() == 0:
            return smart_unicode("کمتر از یک هفته", encoding="utf-8")
        elif obj.week_to_start() == 1:
            return smart_unicode("یک هفته", encoding="utf-8")
        elif obj.week_to_start() == 2:
            return smart_unicode("دو هفته", encoding="utf-8")
        elif obj.week_to_start() == 3:
            return smart_unicode("سه هفته", encoding="utf-8")
        elif obj.week_to_start() == 4:
            return smart_unicode("کمتر از یک ماه", encoding="utf-8")
        elif obj.week_to_start() > 4 :
            return smart_unicode("بیشتر از یک ماه", encoding="utf-8")
        else:
            return smart_unicode("نا‌مشخص", encoding="utf-8")

    week_to_start_per.short_description = "Start"
    list_display = (
        'id', 
        "name", 
        "price",
        "course_type", 
        "course_day", 
        "course_time",
        "teacher",
        "week_to_start_per",
        "location",
        "active",
    )
    list_display_links = ["name"]


@admin.register(Payment)
class Payment_admin(admin.ModelAdmin):

    def resend_receipt(self, request, queryset):
        rows_updated = 0
        for item in queryset:
            if item.status == True:
                item.send_receipt_course()
                rows_updated += 1
        if rows_updated == 1:
            message_bit = "1 receipt"
        elif rows_updated == 0:
            message_bit = "0 receipt"
        else:
            message_bit = "%s receipts" % rows_updated
        self.message_user(request, "%s sent." % message_bit)
    
    def personal_info_get_name(self, obj):
        if obj.personal_info:
            return u"" + obj.personal_info.name + " " + obj.personal_info.family 
        else:
            return ""

    def personal_info_get_phone(self, obj):
        if obj.personal_info:
            return u"" + obj.personal_info.phone_number
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
        if obj.cart and len(obj.cart.courses.all()) > 0:
            return u"" + obj.cart.courses.all().first().name
        elif obj.cart and len(obj.cart.discounts.all()) > 0:
            return u"" + obj.cart.discounts.all().first().name
        else:
            return ""

    def get_cart_discount_code(self, obj):
        if obj.cart and len(obj.cart.discounts.all()) == 1:
            return u"" + obj.cart.discounts.all().first().code
        else:
            return ""

    resend_receipt.short_description = "Resend receipt"
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