# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime  
from django.contrib.auth.models import User  


# Create your models here.
class Lead(models.Model):
    name_and_family = models.CharField(max_length=500, null=False, default='No Name', blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)
    phone_number = models.CharField(max_length=15, null=False, default='09000000000', unique=True, blank=False)
    R_STAT = (
        ('K', 'OK'),
        ('C', 'Cancel'),
        ('D', 'Default'),
    )
    register_status = models.CharField(max_length=1, choices=R_STAT, default='D')
    led_time = models.DateTimeField(default=datetime.now, editable=False)
    discription = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "{} ----- {}".format(self.phone_number, self.name_and_family )
    
class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    def __unicode__(self):
        return str(self.user) + "_Token"