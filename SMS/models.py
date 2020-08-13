# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


# Create your models here.
class Save(models.Model):
    name = models.CharField(max_length=500, null=True, blank=False)
    text = models.TextField(max_length=2000,blank=True, null=False)

class Sent(models.Model):
    phone_regex = RegexValidator(regex=r'^09\d{9}$', \
        message="Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digit digits allowed.")
    sender = models.CharField(validators=[phone_regex], \
        max_length=11, null=False, blank=False)
    reciver = models.CharField(validators=[phone_regex], \
        max_length=11, null=False, blank=False)
    created_date = models.DateTimeField(default=datetime.now(), editable=False)
    created_date_jalali = models.DateTimeField(default=datetime.strptime(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S")\
        ,"%Y-%m-%d %H:%M:%S"), editable=False, null=False, blank=False)
    created_date_jalali_str = models.CharField(max_length=50, default=JalaliDateTime.now().strftime("%c"),\
        editable=False, null=False, blank=False)
    text = models.TextField(max_length=2000,blank=True, null=False)
    status = models.NullBooleanField()
    user = models.ForeignKey(User, null=True, blank=False)

class validate(models.Model):
    phone_regex = RegexValidator(regex=r'^09\d{9}$', \
        message="Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digit digits allowed.")
    phone = models.CharField(validators=[phone_regex], \
        max_length=11, null=False, blank=False)
    created_date = models.DateTimeField(default=datetime.now(), editable=False)
    created_date_jalali = models.DateTimeField(default=datetime.strptime(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S")\
        ,"%Y-%m-%d %H:%M:%S"), editable=False, null=False, blank=False)
    created_date_jalali_str = models.CharField(max_length=50, default=JalaliDateTime.now().strftime("%c"),\
        editable=False, null=False, blank=False)
    code = models.BigIntegerField(default=get_random_string(6, allowed_chars='1234567890'), null=False, blank=False)