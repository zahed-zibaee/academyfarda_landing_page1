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

from .statuscode import status_choices as STATUS_CHOICES
from .config import API_key as apikey 

# Create your models here.
class TextSave(models.Model):
    name = models.CharField(max_length=500, null=True, blank=False)
    text = models.TextField(max_length=2000,blank=True, null=False)

    def __unicode__(self):
        return u"{}-{}".format(self.id, self.name).encode('utf8')
    
    def __str__(self):
        return u"{}-{}".format(self.id, self.name).encode('utf8')

class Sent(models.Model):
    phone_regex = RegexValidator(regex=r'^09\d{9}$', \
        message="Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digits allowed.")
    sender = models.CharField(max_length=20, null=False, blank=False, default='10004000770077')
    receptor = models.CharField(validators=[phone_regex], \
        max_length=11, null=False, blank=False)
    created_date = models.DateTimeField(default=datetime.now(), editable=False)
    sent_time = models.DateTimeField(null=True, blank=True, editable=False)
    text = models.TextField(max_length=2000,blank=True, null=False)
    messageid = models.BigIntegerField(null=True, blank=True)
    gone = models.BooleanField(default=False)
    status = models.CharField(max_length=3, null=True, blank=True, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return u"{}-{}| user:{} gone:{} status:{}".format(self.id ,self.receptor,\
            self.user ,self.gone, self.status).encode('utf8')

    def __str__(self):
        return u"{}-{}| user:{} gone:{} status:{}".format(self.id ,self.receptor,\
            self.user ,self.gone, self.status).encode('utf8')

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
            self.text = response.json()['entries'][0]['message'].encode('utf-8')
            self.sent_time = datetime.now().fromtimestamp(int(response.json()['entries'][0]['date']))
            self.gone = True
            self.save()
            self.check_status()
            return True
        else:
            print("error" + str(response.json()['return']['status']))
            return False

    def check_status(self):
        api = "https://api.kavenegar.com/v1/" + apikey + "/sms/status.json"
        data = {
        'messageid': self.messageid,
        }
        response = get(api, params=data)
        if (response.json()['return']['status'] == 200):
           self.status =  int(response.json()['entries'][0]['status'])
           self.save()
           return True
        else:
            print("error" + str(response.json()['return']['status']))
            return False

    def send_receipt_course(self, ref_id):
        api = "https://api.kavenegar.com/v1/" + apikey + "/verify/lookup.json"
        data = {
            'receptor': self.receptor,
            'token': ref_id,
            'template':'coursereceipt',
        }
        response = get(api, params=data)
        if (response.json()['return']['status'] == 200):
            self.messageid = int(response.json()['entries'][0]['messageid']) 
            self.text = response.json()['entries'][0]['message'].encode('utf-8').strip()
            self.sent_time = datetime.now().fromtimestamp(int(response.json()['entries'][0]['date']))
            self.gone = True
            self.save()
            self.check_status()
            return 200
        else:
            return response.json()['return']['status']

class Verify(models.Model):
    sent = models.ForeignKey(Sent, null=False, blank=False)
    ip = models.GenericIPAddressField(null=True, blank=True)
    token1 = models.CharField(max_length=3, null=False, blank=False, \
        default=''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]))
    token2 = models.CharField(max_length=3, null=False, blank=False, \
        default=''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]))
    expiration_time = models.DateTimeField(default=(datetime.now() + \
        timedelta(minutes=5)), editable=False)
    STATUS_CHOICES = (
            ('K', 'ok'),
            ('N', 'not ok'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="N", null=False, blank=False)

    def __unicode__(self):
        string = u"{}-".format(self.id)
        try:
            u"{} | ".format(self.sent.receptor)
        except:
            u"None | "
        string += u"token1:{} token2:{} status:{}".format(self.token1, self.token2, self.status)
        return string.encode('utf8')

    def __str__(self):
        string = u"{}-".format(self.id)
        try:
            u"{} | ".format(self.sent.receptor)
        except:
            u"None | "
        string += u"token1:{} token2:{} status:{}".format(self.token1, self.token2, self.status)
        return string.encode('utf8')

    def send(self):
        api = "https://api.kavenegar.com/v1/" + apikey + "/verify/lookup.json"
        data = {
            'receptor': self.sent.receptor,
            'token': self.token1,
            'token2': self.token2,
            'template':'auth',
        }
        response = get(api, params=data)
        if (response.json()['return']['status'] == 200):
            self.sent.messageid = int(response.json()['entries'][0]['messageid']) 
            self.sent.text = response.json()['entries'][0]['message'].encode('utf-8').strip()
            self.sent.sent_time = datetime.now().fromtimestamp(int(response.json()['entries'][0]['date']))
            self.sent.gone = True
            self.sent.save()
            self.save()
            self.check_status()
            return 200
        else:
            return response.json()['return']['status']
            
    def check_status(self):
        self.sent.check_status()

    def validate(self, token1, token2):
        if (self.token1 == token1) and (self.token2 == token2) and (self.sent.created_date < self.expiration_time):
            self.status = "K"
            self.save()
            return True
        else:
            return False
