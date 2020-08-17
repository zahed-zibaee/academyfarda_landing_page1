# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import datetime,timedelta
from persiantools.jdatetime import JalaliDateTime
from random import randint
from requests import get
from urllib import quote

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
    massageid = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
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
            self.messageid = int(response.json()['entries']['messageid']) 
            self.created_date = datetime.now().fromtimestamp(int(response.json()['entries']['date'])) 
        else:
            print("error" + response.json()['return']['status'])

    def verify(self):
        api = "https://api.kavenegar.com/v1/" + apikey + "/sms/status.json"
        data = {
        'messageid': massageid,
        }
        response = get(api, params=data)
        if (response.json()['return']['status'] == 200):
           self.status =  int(response.json()['entries'][0]['status'])

class Verify(models.Model):
    sent = models.ForeignKey(Sent, null=False, blank=False)
    ip = models.GenericIPAddressField(null=False, blank=False)
    token1 = models.CharField(max_length=3, null=False, blank=False, default=''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]))
    token2 = models.CharField(max_length=3, null=False, blank=False, default=''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]))
    exception_time = models.DateTimeField(default=(datetime.now() + timedelta(minutes=1)), editable=False)
    STATUS_CHOICES = (
            ('K', 'ok'),
            ('N', 'not ok'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="U", null=False, blank=False)

