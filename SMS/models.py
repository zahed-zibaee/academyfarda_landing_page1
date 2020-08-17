# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import datetime,timedelta
from persiantools.jdatetime import JalaliDateTime
from random import randint
from requests import get
from django.utils.six.moves.urllib.parse import quote

from .config import API_key as apikey 

# Create your models here.
class TextSave(models.Model):
    name = models.CharField(max_length=500, null=True, blank=False)
    text = models.TextField(max_length=2000,blank=True, null=False)

class Sent(models.Model):
    phone_regex = RegexValidator(regex=r'^09\d{9}$', \
        message="Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digits allowed.")
    sender = models.CharField(max_length=20, null=False, blank=False, default='10004000770077')
    receptor = models.CharField(validators=[phone_regex], \
        max_length=11, null=False, blank=False)
    created_date = models.DateTimeField(default=datetime.now(), editable=False)
    created_date_jalali = models.DateTimeField(default=datetime.strptime(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S")\
        ,"%Y-%m-%d %H:%M:%S"), editable=False, null=False, blank=False)
    created_date_jalali_str = models.CharField(max_length=50, default=JalaliDateTime.now().strftime("%c"),\
        editable=False, null=False, blank=False)
    text = models.TextField(max_length=2000,blank=True, null=False)
    messageid = models.BigIntegerField(null=True, blank=True)
    STATUS_CHOICES = (
        ('0', 'بررسی نشده'),
        ('1', 'در صف ارسال قرار دارد'),
        ('2', 'زمان بندی شده (ارسال در تاریخ معین)'),
        ('4', 'ارسال شده به مخابرات'),
        ('5', 'ارسال شده به مخابرات'),
        ('6', 'خطا در ارسال پیام که توسط سر شماره پیش می آید و به معنی عدم رسیدن پیامک می‌باشد'),
        ('10', 'رسیده به گیرنده'),
        ('11', 'نرسیده به گیرنده ، این وضعیت به دلایلی از جمله خاموش یا خارج از دسترس بودن گیرنده اتفاق می افتد'),
        ('13', 'ارسال پیام از سمت کاربر لغو شده یا در ارسال آن مشکلی پیش آمده که هزینه آن به حساب برگشت داده می‌شود'),
        ('14', 'بلاک شده است، عدم تمایل گیرنده به دریافت پیامک از خطوط تبلیغاتی که هزینه آن به حساب برگشت داده می‌شود'),
        ('100', 'شناسه پیامک نامعتبر است'),
    )
    status = models.IntegerField(null=True, blank=True, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, null=True, blank=True)

    def send(self):
        api = "https://api.kavenegar.com/v1/" + apikey + "/sms/send.json"
        coded_message = quote(self.text.encode('utf8'))
        data = {
            'receptor': self.receptor,
            'message': coded_message,
            'sender': self.sender,
        }
        response = get(api, params=data)
        if (response.json()['return']['status'] == 200):
            self.messageid = int(response.json()['entries'][0]['messageid']) 
            self.created_date = datetime.now().fromtimestamp(int(response.json()['entries'][0]['date']))
            self.save()
        else:
            print("error" + str(response.json()['return']['status']))

    def check_status(self):
        api = "https://api.kavenegar.com/v1/" + apikey + "/sms/status.json"
        data = {
        'messageid': self.messageid,
        }
        response = get(api, params=data)
        if (response.json()['return']['status'] == 200):
           self.status =  int(response.json()['entries'][0]['status'])
           self.save()
        else:
            print("error" + str(response.json()['return']['status']))


class Verify(models.Model):
    sent = models.ForeignKey(Sent, null=False, blank=False)
    ip = models.GenericIPAddressField(null=True, blank=True)
    token1 = models.CharField(max_length=3, null=False, blank=False, default=''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]))
    token2 = models.CharField(max_length=3, null=False, blank=False, default=''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]))
    expiration_time = models.DateTimeField(default=(datetime.now() + timedelta(minutes=1)), editable=False)
    STATUS_CHOICES = (
            ('K', 'ok'),
            ('N', 'not ok'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="N", null=False, blank=False)

    def send(self):
        api = "https://api.kavenegar.com/v1/" + apikey + "/verify/lookup.json"
        data = {
            'receptor': self.sent.receptor,
            'token': self.token1,
            'token2': self.token2,
            'template':'default',
        }
        response = get(api, params=data)
        if (response.json()['return']['status'] == 200):
            self.sent.messageid = int(response.json()['entries'][0]['messageid']) 
            self.sent.text = str(response.json()['entries'][0]['message']) 
            self.sent.created_date = datetime.now().fromtimestamp(int(response.json()['entries'][0]['date']))
            self.sent.save()
            self.save()
        else:
            print("error" + str(response.json()['return']['status']))

    def check_status(self):
        self.sent.check_status()

    def validate(self, token1, token2):
        if self.token1 == token1 and self.token2 == token2:
            return True
        else:
            return False