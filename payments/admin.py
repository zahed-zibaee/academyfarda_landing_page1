# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Teacher)
class Teacher_admin(admin.ModelAdmin):
    list_display = ('id','name',"family")
    list_display_links = ['name',"family"]
@admin.register(PaymentInformation)
class PaymentInformation_admin(admin.ModelAdmin):
    list_display = ('id','name',"family","gender","father_name","code_meli","phone_number","cart_id")
    list_display_links = ['name',"family"]
@admin.register(Payment)
class Payment_admin(admin.ModelAdmin):
    list_display = ('id','payment_info_id',"total","created_date","status","ref_id","send_receipt")
    list_display_links = ["payment_info_id"]
@admin.register(Cart)
class Cart_admin(admin.ModelAdmin):
    list_display = ('id',"verification_id","get_courses","get_discounts")
    list_display_links = ["verification_id"]
@admin.register(Discount)
class Discount_admin(admin.ModelAdmin):
    list_display = ('id',"name","product_id","code","amount","expiration_time","active")
    list_display_links = ["name"]
@admin.register(Course)
class Course_admin(admin.ModelAdmin):
    list_display = ('id',"get_name","show","price","active")
    list_display_links = ["get_name"]