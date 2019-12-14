# -*- coding: utf-8 -*-
from .models import Origin, LabelDefinition
from django.contrib.auth.models import User

REGISTRATION_STATUS = {
    'ثبت نام شده ':'K', 
    'کنسل شده':'C', 
    'نا مشخص':'D', 
}
    
GENDER_CHOICES = {
    'مرد ': 'M',
    'زن':'F',
}

ORIGIN_DESCRIPTION = {}
for item in Origin.objects.all():
    ORIGIN_DESCRIPTION.update( { item.description:item.id } )

USER_NAME_AND_FAMILY = {}
for item in User.objects.filter(is_staff=True):
    USER_NAME_AND_FAMILY.update( { item.first_name + " " + item.last_name:item.id } )

LABELDEFINITION_TAG = {}
for item in LabelDefinition.objects.all():
    LABELDEFINITION_TAG.update( { item.tag:item.color_code } )