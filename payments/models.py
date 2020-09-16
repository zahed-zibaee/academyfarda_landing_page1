# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime,timedelta
from persiantools.jdatetime import JalaliDateTime
from SMS.models import Verify, Sent
from zeep import Client
import pytz

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    price = models.BigIntegerField(null=False, blank=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"{}-{} {} | active:{}".format(self.id ,self.name, self.price, self.active).encode('utf-8')

    def __str__(self):
        return u"{}-{} {} | active:{}".format(self.id ,self.name, self.price, self.active).encode('utf-8')
    
    def is_active(self):
        if self.expiration_time.replace(tzinfo=None) > datetime.now() and self.active == True\
             and self.product.active == True:
            return True
        else:
            return False

    class meta:
        abstract = True

class Discount(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    code = models.CharField(max_length=100, null=False, blank=False, unique=True)
    product = models.ForeignKey(Product, null=False, blank=False)
    amount = models.BigIntegerField(null=False, blank=False)
    expiration_time = models.DateTimeField(null=False, blank=False, default=datetime.now() + timedelta(days=+36500))
    active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"{}-{} | code:{} amount:{} active:{}".format(self.id ,self.name, \
            self.code, self.amount, self.active).encode('utf-8')

    def __str__(self):
        return u"{}-{} | code:{} amount:{} active:{}".format(self.id ,self.name, \
            self.code, self.amount, self.active).encode('utf-8')

    def is_active(self):
        if self.expiration_time.replace(tzinfo=None) > datetime.now() and self.active == True\
             and self.product.active == True:
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
    code_meli = models.CharField(validators=[meli_regex], \
        max_length=10, null=False, blank=False, unique=True)

    def __unicode__(self):
        return u"{}-{}".format(self.name, self.family).encode('utf-8')

    def __str__(self):
        return u"{} {}".format(self.name ,self.family).encode('utf-8')
        

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
        return u"{}-{} | price:{} active:{}".format(self.id ,self.name, self.price, self.active).encode('utf-8')

    def __str__(self):
        return u"{}-{} | price:{} active:{}".format(self.id ,self.name, self.price, self.active).encode('utf-8')
        
    def get_name(self):
        string = "کلاس "
        if self.class_type == "R":
            string += "عادی "
            string += "- "
        elif self.class_type == "I":
            string += "فشرده "
            string += "- "
        if self.time == "912":
            string += "۹ تا ۱۲ "
            string += "- "
        elif self.time == "1316":
            string += "۱۳ تا ۱۶ "
            string += "- "
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

class PaymentInformation(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    family= models.CharField(max_length=200, null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    father_name = models.CharField(max_length=200, null=True, blank=True)
    meli_regex = RegexValidator(regex=r'^\d{10}$', \
        message="Meli code must be entered in the format: 'XXXXXXXXXX'. only 10 digits allowed.")
    code_meli = models.CharField(validators=[meli_regex], \
        max_length=10, null=True, blank=True)
    code_shenasname = models.CharField(max_length=10, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^09\d{9}$', \
        message="Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digit digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], \
        max_length=11, null=False, blank=False)
    phone_number2 = models.CharField(max_length=15, null=True, blank=True)
    origin_town = models.CharField(max_length=200, null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.TextField(max_length=2000,blank=True, null=True)
    PAYMENT_TYPE_CHOICES = (
        ('0', 'نقدی'),
        ('1', 'اقساط'),
    )
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE_CHOICES,\
         null=False, blank=False, default="0")
    
    def __unicode__(self):
        return u"{}| meli code:{} phone:{}".format(self.id, self.code_meli, self.phone_number).encode('utf-8')

    def __str__(self):
        return u"{}| meli code:{} phone:{}".format(self.id, self.code_meli, self.phone_number).encode('utf-8')
    

class Cart(models.Model):
    course = models.ManyToManyField(Course, blank=True)
    discount = models.ManyToManyField(Discount, blank=True)
    payment_info = models.ForeignKey(PaymentInformation, related_name='payment_info',\
        null=True, blank=False, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"{}- payment information id:{} course:{} discount:{}".format(self.id \
            ,self.payment_info.id , self.course.all(), self.discount.all()).encode('utf-8')

    def __str__(self):
        return u"{}- payment information id:{} course:{} discount:{}".format(self.id \
            ,self.payment_info.id , self.course.all(), self.discount.all()).encode('utf-8')

    def get_courses(self):
        try:
            return ", ".join([str(obj.id) for obj in self.course.all()])
        except:
            return None

    def get_discounts(self):
        try:
            return ", ".join([str(obj.id) for obj in self.discount.all()])
        except:
            None

    def get_href(self, MERCHANT, description, amount, mobile, callbackurl):
        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        result = client.service.PaymentRequest(MERCHANT, amount, description, mobile, CallbackURL = callbackurl)
        if result.Status == 100:
            return [True, str(result.Authority)]
        else:
            return [False, str(result.Status)]

class Payment(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart', null=True, blank=False,\
         on_delete=models.SET_NULL)
    verification = models.ForeignKey(Verify, on_delete=models.SET_NULL, null=True)
    total = models.BigIntegerField(null=True, blank=True)
    authority = models.CharField(max_length=100, null=True, blank=False)
    created_date = models.DateTimeField(default=datetime.now(), editable=False)
    status = models.BooleanField(default=False)
    ref_id = models.CharField(max_length=50, null=True, blank=False)
    send_receipt = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{}| cart id:{} verification id:{} total:{} created date:{} status:{} refrence code:{} "\
            .format(self.id, self.cart.id, self.verification.id, self.total, \
            JalaliDateTime(self.created_date).strftime("%Y/%m/%d %H:%M:%S"), self.status, self.ref_id).encode('utf-8')
        
    def __str__(self):
        return u"{}| cart id:{} verification id:{} total:{} created date:{} status:{} refrence code:{} "\
            .format(self.id, self.cart.id, self.verification.id, self.total, \
            JalaliDateTime(self.created_date).strftime("%Y/%m/%d %H:%M:%S"), self.status, self.ref_id).encode('utf-8')

    def get_jalali_date(self):
        return JalaliDateTime(self.created_date).strftime("%Y/%m/%d")
        #return JalaliDateTime(self.created_date.replace(tzinfo=pytz.utc)\
        #    .astimezone(pytz.timezone("Asia/Tehran"))).strftime("%Y/%m/%d")
    def get_tehran_time(self):
        return self.created_date.strftime("%H:%M:%S")
        #return JalaliDateTime(self.created_date.replace(tzinfo=pytz.utc)\
        #    .astimezone(pytz.timezone("Asia/Tehran"))).strftime("%H:%M:%S")

    def send_receipt_course(self):
        sms = Sent.objects.create(receptor = self.cart.payment_info.phone_number,\
             created_date = datetime.now())
        res_code = sms.send_receipt_course(self.ref_id)
        if res_code == 200:
            self.send_receipt = True
            self.save()
            return res_code
        else:
            return res_code