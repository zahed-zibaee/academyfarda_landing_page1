# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import datetime, timedelta, tzinfo
from django.utils import timezone
from django.utils.encoding import smart_unicode
from random import randint
from requests import get
from django.utils.six.moves.urllib.parse import quote

from .statuscode import STATUS_CHOICES, STATUS_CODES
from .config import API_KEY

class APIError(Exception):
    """An API Error Exception"""
    def __init__(self, api_name, status):
        self.status = status
        self.api_name = api_name

    def __str__(self):
        return "API={} status={}".format(self.api_name, self.status)

class Sent(models.Model):
    """list of SMSs
    it only get one receptor"""
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message="Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digits allowed."
    )
    sender = models.CharField(
        max_length=20, 
        null=False, blank=False, 
        default='10004000770077',
    )
    receptor = models.CharField(
        validators=[phone_regex],
        max_length=11, 
        null=False, 
        blank=False,
    )
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    send_date = models.DateTimeField(null = True, blank = True)
    message = models.TextField(max_length=2000, blank=True, null=False)
    message_id = models.BigIntegerField(null=True, blank=True)
    gone = models.BooleanField(default=False)
    status_code = models.CharField(
        max_length=3, 
        null=False, 
        blank=False, 
        default="0", 
        choices=STATUS_CHOICES,
    )
    user = models.ForeignKey(User, null=True, blank=True)

    def send(self):
        api = "https://api.kavenegar.com/v1/" + API_KEY + "/sms/send.json"
        coded_message = quote(self.message.encode('utf8'))
        data = {
            'receptor': self.receptor,
            'message': coded_message,
            'sender': self.sender,
        }
        try:
            response = get(api, params=data)
        except:
            raise APIError("Kavenegar", "can not connect")
        if (response.json()['return']['status'] == 200):
            self.message_id = int(response.json()['entries'][0]['messageid']) 
            self.message = response.json()['entries'][0]['message'].encode('utf-8')
            self.send_date = timezone.make_aware(
                datetime.now(), 
                timezone.get_default_timezone()
                )
            self.gone = True
            self.save()
            self.check_status()
            return response.json()['return']['status']
        else:
            try:
                status = STATUS_CODES[str(response.json()['return']['status'])]
            except:
                status = str(response.json()['return']['status'])
            return status
                

    def check_status(self):
        api = "https://api.kavenegar.com/v1/" + API_KEY + "/sms/status.json"
        data = {
            'messageid': self.message_id,
            }
        response = get(api, params=data)
        if (response.json()['return']['status'] == 200):
            self.status_code =  int(response.json()['entries'][0]['status'])
            self.save()
            return True
        else:
            return False

    def send_receipt_course(self, ref_id):
        api = "https://api.kavenegar.com/v1/" + API_KEY + "/verify/lookup.json"
        data = {
            'receptor': self.receptor,
            'token': ref_id,
            'template': 'coursereceipt',
            }
        try:
            response = get(api, params=data)
        except:
            raise APIError("Kavenegar", "can not connect")
        if response.json()['return']['status'] == 200:
            self.message_id = int(response.json()['entries'][0]['messageid']) 
            self.message = response.json()['entries'][0]['message'].encode('utf-8').strip()
            self.send_date = timezone.make_aware(
                datetime.now(), 
                timezone.get_default_timezone()
                )
            self.gone = True
            self.save()
            self.check_status()
            return 200
        else:
            try:
                status = STATUS_CODES[str(response.json()['return']['status'])]
            except:
                status = str(response.json()['return']['status'])
            return status

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, receptor: {}, message: {}, gone: {}, status: {}".format(
                self.id, 
                self.receptor,
                self.message[:10],
                self.gone, 
                self.status_code,
            ),
            encoding='utf-8',
        )

    def __str__(self):
        return smart_unicode(
            "ID: {}, receptor: {}, message: {}, gone: {}, status: {}".format(
                self.id, 
                self.receptor,
                self.message[:10],
                self.gone, 
                self.status_code,
            ),
            encoding='utf-8',
        )


class Verify(models.Model):
    sent = models.ForeignKey(Sent, null=False, blank=False)
    token = models.CharField(max_length=6, null=False, blank=False, default="000000")
    expiration_time = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def start(self):
        self.token = ''.join(["{}".format(randint(0, 9)) for _ in range(0, 6)])
        self.expiration_time = timezone.make_aware(
            datetime.now() + timedelta(minutes=11), 
            timezone.get_default_timezone()
        )
        self.save()

    def send(self):
        api = "https://api.kavenegar.com/v1/" + API_KEY + "/verify/lookup.json"
        data = {
            'receptor': self.sent.receptor,
            'token': self.token,
            'template':'auth',
        }
        try:
            response = get(api, params=data)
        except:
            raise APIError("Kavenegar", "can not connect")
        if (response.json()['return']['status'] == 200):
            self.sent.message_id = int(
                response.json()['entries'][0]['messageid']
            ) 
            self.sent.message = response.json()['entries'][0]['message']\
                .encode('utf-8').strip()
            self.sent.send_date = timezone.make_aware(
                datetime.now(), 
                timezone.get_default_timezone()
                )
            self.sent.gone = True
            self.sent.save()
            self.check_status()
            return response.json()['return']['status']
        else:
            try:
                status = STATUS_CODES[str(response.json()['return']['status'])]
            except:
                status = str(response.json()['return']['status'])
            return status
            
    def check_status(self):
        self.sent.check_status()

    def validate(self, token):
        if self.token == token and timezone.make_aware(
                datetime.now(),
                timezone.get_default_timezone()
                ) < self.expiration_time:
            self.status = True
            self.save()
            return True
        else:
            return False

    def __unicode__(self):
        string = u"ID: {},".format(self.id)
        if self.sent:
            string += u" receptor: {}, message: {},".format(
                self.sent.receptor,
                self.sent.message[:10],
            )
        string += u" token: {}, status: {}".format(
            self.token,
            self.status,
        )
        return smart_unicode(string, encoding='utf-8')

    def __str__(self):
        string = u"ID: {},".format(self.id)
        if self.sent:
            string += u" receptor: {}, message: {},".format(
                self.sent.receptor,
                self.sent.message[:10],
            )
        string += u" token: {}, status: {}".format(
            self.token,
            self.status,
        )
        return smart_unicode(string, encoding='utf-8')
