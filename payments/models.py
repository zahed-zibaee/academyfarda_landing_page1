# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime
from persiantools.jdatetime import JalaliDateTime

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    amount = models.BigIntegerField(null=False, blank=False)
    active = models.NullBooleanField(null=True, blank=False)
    class meta:
        abstract = True

class Discount(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    code = models.CharField(max_length=100, null=False, blank=False)
    product = models.ForeignKey(Product, null=False, blank=False)
    amount = models.BigIntegerField(null=False, blank=False)
    active = models.NullBooleanField(null=True, blank=False)

class Teacher(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    family= models.CharField(max_length=200, null=False, blank=False)
    meli_regex = RegexValidator(regex=r'^\d{10}$', \
        message="Meli code must be entered in the format: 'XXXXXXXXXX'. only 10 digits allowed.")
    meli = models.CharField(validators=[meli_regex], \
        max_length=10, null=False, blank=False, unique=True)

    def __unicode__(self):
        return "{} {}".format(self.name, self.family)

class Course(Product):
    CLASS_TYPE_CHOICES = (
        ('0', 'regular'),
        ('1', 'intensive'),
    )
    class_type = models.CharField(max_length=1, choices=CLASS_TYPE_CHOICES, null=False, blank=False)
    TIME_CHOICES = (
        ('0', '9-12'),
        ('1', '13-16'),
        ('2', '17-20'),
    )
    time = models.CharField(max_length=1, choices=TIME_CHOICES, null=False, blank=False)
    DAY_CHOICES = (
        ('0', 'SA-WE'),
        ('1', 'SA-TH'),
    )
    day = models.CharField(max_length=1, choices=DAY_CHOICES, null=False, blank=False)
    teacher = models.ForeignKey(Teacher, related_name='teacher', null=False, blank=False)

    def __unicode__(self):
        return "{} {} {} {}".format(self.get_class_type_display(), self.get_time_display(), self.get_day_display(), self.teacher)

class Cart(models.Model):
    course = models.ManyToManyField(Course)
    discount = models.ManyToManyField(Discount)


class PaymentInformation(models.Model):
    name = models.CharField(max_length=200, null=True, blank=False)
    family= models.CharField(max_length=200, null=True, blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    father_name= models.CharField(max_length=200, null=True, blank=False)
    meli_regex = RegexValidator(regex=r'^\d{10}$', \
        message="Meli code must be entered in the format: 'XXXXXXXXXX'. only 10 digits allowed.")
    meli = models.CharField(validators=[meli_regex], \
        max_length=10, null=True, blank=False, unique=True)
    phone_regex = RegexValidator(regex=r'^09\d{9}$', \
        message="Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digit digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], \
        max_length=11, null=False, blank=False)
    address = models.TextField(max_length=2000,blank=False, null=True)
    PAYMENT_TYPE_CHOICES = (
        ('0', 'نقدی'),
        ('1', 'اقساط'),
    )
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE_CHOICES, null=False, blank=False, default="0")
    cart = models.ForeignKey(Cart, related_name='cart', null=False, blank=False)
    
    
class Payment(models.Model):
    payment_info = models.ForeignKey(PaymentInformation, related_name='payment_info',unique=False, null=True, blank=False)
    authority = models.CharField(max_length=100, null=True, blank=False)
    created_date = models.DateTimeField(default=datetime.now(), editable=False)
    created_date_jalali = models.DateTimeField(default=datetime.strptime(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S")\
        ,"%Y-%m-%d %H:%M:%S"), editable=False, null=False, blank=False)
    created_date_jalali_str = models.CharField(max_length=50, default=JalaliDateTime.now().strftime("%c"),\
        editable=False, null=False, blank=False)
    status = models.NullBooleanField(null=True, blank=False)
    ref_id = models.CharField(max_length=50, null=True, blank=False)
    
