# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import *


# Register your models here.
@admin.register(Teacher)
class Teacher_admin(admin.ModelAdmin):
    list_display = ('id', "family", 'name')
    list_display_links = ['family',]
@admin.register(PaymentInformation)
class PaymentInformation_admin(admin.ModelAdmin):
    list_display = ('id', 'name', "family", "gender", "father_name", "code_meli", "phone_number")
    list_display_links = ['name',"family"]
@admin.register(Payment)
class Payment_admin(admin.ModelAdmin):
    list_display = ('id', "verification_id", "cart_id", "total", "created_date", "status", "ref_id", "send_receipt")
    list_display_links = ["id"]
    raw_id_fields = ("verification","cart")
    list_filter = (
        ('created_date', DateFieldListFilter,),
        'status',
        "send_receipt",
    )
    search_fields = ("id",'ref_id')
@admin.register(Cart)
class Cart_admin(admin.ModelAdmin):
    list_display = ('id', 'payment_info_id', "get_courses", "get_discounts")
    list_display_links = ["id"]
    raw_id_fields = ("payment_info",)
@admin.register(Discount)
class Discount_admin(admin.ModelAdmin):
    list_display = ('id', "name", "product_id", "code", "amount", "expiration_time", "active")
    list_display_links = ["name"]
@admin.register(Course)
class Course_admin(admin.ModelAdmin):
    list_display = ('id',"get_name","show","price","active")
    list_display_links = ["get_name"]