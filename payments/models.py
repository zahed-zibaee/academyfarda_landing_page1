# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime,timedelta
from persiantools.jdatetime import JalaliDateTime
from SMS.models import Verify
from zeep import Client
import pytz

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    price = models.BigIntegerField(null=False, blank=False)
    active = models.NullBooleanField(null=True, blank=False)

    def __unicode__(self):
        return "{}-{}".format(self.name, self.amount, self.active)

    class meta:
        abstract = True

class Discount(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    code = models.CharField(max_length=100, null=False, blank=False, unique=True)
    product = models.ForeignKey(Product, null=False, blank=False)
    amount = models.BigIntegerField(null=False, blank=False)
    expiration_time = models.DateTimeField(null=False, blank=False, default=datetime.now() + timedelta(days=+36500))
    active = models.NullBooleanField(null=True, blank=False)
    
    def __unicode__(self):
        return "{}-{}-{}-{}-{}".format(self.name, self.product, self.code, self.amount, self.active)

    def is_active(self):
        if self.expiration_time.replace(tzinfo=None) > datetime.now() and self.active == True and self.product.active == True:
            return True
        else:
            return False

    def get_total(self):
        if self.is_active():
            return (self.product.price - self.amount)
        else:
            return False


class Teacher(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    family= models.CharField(max_length=200, null=False, blank=False)
    meli_regex = RegexValidator(regex=r'^\d{10}$', \
        message="Meli code must be entered in the format: 'XXXXXXXXXX'. only 10 digits allowed.")
    meli = models.CharField(validators=[meli_regex], \
        max_length=10, null=False, blank=False, unique=True)

    def __unicode__(self):
        return "{}-{}".format(self.name, self.family)

class Course(Product):
    CLASS_TYPE_CHOICES = (
        ('R', 'regular'),
        ('I', 'intensive'),
    )
    class_type = models.CharField(max_length=1, choices=CLASS_TYPE_CHOICES, null=False, blank=False)
    TIME_CHOICES = (
        ('912', '9-12'),
        ('1316', '13-16'),
        ('1720', '17-20'),
    )
    time = models.CharField(max_length=4, choices=TIME_CHOICES, null=False, blank=False)
    DAY_CHOICES = (
        ('STW', 'SA-WE'),
        ('STT', 'SA-TH'),
        ('E', 'even'),
        ('O', 'odd'),
    )
    day = models.CharField(max_length=4, choices=DAY_CHOICES, null=False, blank=False)
    teacher = models.ForeignKey(Teacher, related_name='teacher', null=True, blank=True)
    show = models.BooleanField(default=True)

    def __unicode__(self):
        return "{}-{}-{}-{}".format(self.get_class_type_display(), self.get_time_display(), self.get_day_display(), self.teacher)

    def get_name(self):
        string = "کلاس "
        if self.class_type == "I":
            string += "عادی "
        elif self.class_type == "R":
            string += "فشرده "
        string += "- "
        if self.time == "912":
            string += "۹ تا ۱۲ "
        elif self.time == "1316":
            string += "۱۳ تا ۱۶ "
        elif self.time == "1720":
            string += "۱۷ تا ۲۰ "
        string += "- "
        if self.day=="STW":
            string += "شنبه تا چهار‌شنبه "
        elif self.day=="STT":
            string += "شنبه تا پنج‌شنبه "
        elif self.day=="O":
            string += "فرد "
        elif self.day=="E":
            string += "زوج "
        if self.teacher != None:
            string += "- "
            string += "استاد " + self.teacher.name + " " + self.teacher.family + " "
        return string


class Cart(models.Model):
    course = models.ManyToManyField(Course)
    discount = models.ManyToManyField(Discount)
    verification = models.ForeignKey(Verify, on_delete=models.SET_NULL, null=True )

    def __unicode__(self):
        return "{}-{}-{}-{}".format(self.id, self.course, self.discount, self.verification)

    def get_href(self, MERCHANT, description, amount, mobile, callbackurl):
        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        print(MERCHANT)
        print(amount)
        print(description)
        print(mobile)
        print(callbackurl)
        result = client.service.PaymentRequest(MERCHANT, amount, description, mobile, CallbackURL = callbackurl)
        if result.Status == 100:
            return [True, str(result.Authority)]
        else:
            return [False, str(result.Status)]

class PaymentInformation(models.Model):
    name = models.CharField(max_length=200, null=True, blank=False)
    family= models.CharField(max_length=200, null=True, blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    father_name = models.CharField(max_length=200, null=True, blank=False)
    meli_regex = RegexValidator(regex=r'^\d{10}$', \
        message="Meli code must be entered in the format: 'XXXXXXXXXX'. only 10 digits allowed.")
    code_meli = models.CharField(validators=[meli_regex], \
        max_length=10, null=True, blank=False)
    code_shenasname = models.CharField(max_length=10, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^09\d{9}$', \
        message="Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digit digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], \
        max_length=11, null=False, blank=False)
    phone_number2 = models.CharField(validators=[phone_regex], \
        max_length=11, null=True, blank=False)
    origin_town = models.CharField(max_length=200, null=True, blank=False)
    birthday = models.DateField(blank=False, null=True)
    address = models.TextField(max_length=2000,blank=False, null=True)
    PAYMENT_TYPE_CHOICES = (
        ('0', 'نقدی'),
        ('1', 'اقساط'),
    )
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE_CHOICES, null=False, blank=False, default="0")
    cart = models.ForeignKey(Cart, related_name='cart', null=True, blank=False, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return "{}-{}-{}-{}".format(self.id, self.name, self.family, self.cart)

    
class Payment(models.Model):
    payment_info = models.ForeignKey(PaymentInformation, related_name='payment_info',unique=False, null=True, blank=False, on_delete=models.SET_NULL)
    total = models.BigIntegerField(null=True, blank=True)
    authority = models.CharField(max_length=100, null=True, blank=False)
    created_date = models.DateTimeField(default=datetime.now(), editable=False)
    status = models.NullBooleanField(null=True, blank=False)
    ref_id = models.CharField(max_length=50, null=True, blank=False)
    
    def __unicode__(self):
        return "{}-{}-{}".format(self.id, self.ref_id, self.status)
