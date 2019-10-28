# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from persiantools.jdatetime import JalaliDateTime
from django.utils.html import format_html

class Token(models.Model):
    description = models.CharField(max_length=100, null=False, default='No Name', blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, null=True, blank=True)
    token_activation = models.BooleanField(default=False)
    def __unicode__(self):
        return "{}".format(self.description)

class Lead(models.Model):
    #TODO 
    origin = models.ForeignKey(Token, on_delete=models.SET_NULL, unique=False, null=True, editable=False,)
    name_and_family = models.CharField(max_length=500, null=False, default='No Name', blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)
    phone_regex = RegexValidator(regex=r'^[0-9].{6,15}$', \
        message="Phone number must be entered in the format: '09999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], \
        max_length=15, null=False, default='09000000000', unique=True, blank=False)
    R_STAT = (
        ('K', 'OK'),
        ('C', 'Cancel'),
        ('D', 'Default'),
    )
    register_status = models.CharField(max_length=1, choices=R_STAT, default='D')
    led_time = models.DateTimeField(default=datetime.now(), editable=False)
    led_time_jalali = models.DateTimeField(default=datetime.strptime(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S")\
        ,"%Y-%m-%d %H:%M:%S"), editable=False, null=False, blank=False)
    led_time_jalali_str = models.CharField(max_length=50, default=JalaliDateTime.now().strftime("%c"),\
        editable=False, null=False, blank=False)
    question = models.TextField(blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator', unique=False, null=True, editable=False,)

    def __unicode__(self):
        return "{} ----- {}".format(self.phone_number, self.name_and_family)


class Comment(models.Model):
    post = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    text = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.now(), editable=False)
    created_date_jalali = models.DateTimeField(default=datetime.strptime(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S")\
        ,"%Y-%m-%d %H:%M:%S"), editable=False, null=False, blank=False)
    created_date_jalali_str = models.CharField(max_length=50, default=JalaliDateTime.now().strftime("%c"),\
        editable=False, null=False, blank=False)
    approved_comment = models.BooleanField(default=True)
    def __unicode__(self):
        return str(self.id) + " :" + str(self.author)

 
class LabelDefinition(models.Model):
    tag = models.CharField(max_length=500, null=True, blank=True)
    COLOR_CHOICES = (
    ('800000', 'Maroon'),
    ('FF0000', 'Red'),
    ('FFA500', 'Orange'),
    ('FFFF00', 'Yellow'),
    ('808000', 'Olive'),
    ('00800', 'Green'),
    ('800080', 'Purple'),
    ('FF00FF', 'Fuchsia'),
    ('00FF00', 'Lime'),
    ('008080', 'Teal'),
    ('00FFFF', 'Aqua'),
    ('0000FF', 'Blue'),
    ('000080', 'Navy'),
    ('000000', 'Black'),
    ('808080', 'Gray'),
    )
    color_code = models.CharField(max_length=10, choices=COLOR_CHOICES, default="000000", unique=True)
    def colored_name(self):
        return format_html(
            '<span style="color: white; background-color: #{};">{}</span>',
            self.color_code,
            self.tag,
        )
    def __unicode__(self):
        return "{}".format(self.tag)

class Label(models.Model):
    post = models.ForeignKey(Lead, on_delete=models.CASCADE)
    label = models.ForeignKey(LabelDefinition, on_delete=models.CASCADE)
    def colored_name(self):
        return format_html(
            '<span style="color: white; background-color: #{};">{}</span>',
            self.label.color_code,
            self.label.tag,
        )
    def export_show(self):
        return format_html(
            '<button type="button" class="btn btn-light btn-sm" style="color: white; background-color: #{};">{}</button>',
            self.label.color_code,
            self.label.tag, 
        )
    def __unicode__(self):
        return format_html(
            '<span style="color: white; background-color: #{};">{}</span>',
            self.label.color_code,
            self.label.tag,
        )