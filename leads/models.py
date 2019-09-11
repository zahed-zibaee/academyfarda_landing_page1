# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime  
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
<<<<<<< HEAD
=======

>>>>>>> e7744f5b5355c20b57de7c2c75fb9928af1c91b3
   
class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    def __unicode__(self):
        return str(self.user) + "_Token"

class Lead(models.Model):
    token = models.ForeignKey(Token, on_delete=models.SET_NULL, unique=False, null=True, editable=False,)
    name_and_family = models.CharField(max_length=500, null=False, default='No Name', blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)
    phone_regex = RegexValidator(regex=r'^[0-9].{6,15}$', message="Phone number must be entered in the format: '09999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, null=False, default='09000000000', unique=True, blank=False)
    R_STAT = (
        ('K', 'OK'),
        ('C', 'Cancel'),
        ('D', 'Default'),
    )
    register_status = models.CharField(max_length=1, choices=R_STAT, default='D')
    led_time = models.DateTimeField(default=datetime.now, editable=False)
    description = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return "{} ==> {} ----- {}".format(self.id, self.phone_number, self.name_and_family)

class Comment(models.Model):
    post = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    text = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.now, editable=False)
    approved_comment = models.BooleanField(default=True)
    def __unicode__(self):
        return str(self.id) + " :" + str(self.author)
