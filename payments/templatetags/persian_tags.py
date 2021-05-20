# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.encoding import smart_unicode
from datetime import date, datetime
from django import template
from persiantools import digits
from persiantools.jdatetime import JalaliDateTime
from django.utils import timezone


register = template.Library()

@register.filter
def weeks_date_to_string(string):
    try:
        datetime_value = datetime.strptime(string, '%Y-%m-%d')
    except:
        return ""
    date_value = datetime_value.date()
    today = date.today()
    weeks = (date_value - today).days // 7
    if weeks <= 0:
        return smart_unicode("کمتر از یک هفته",encoding="utf-8")
    elif  weeks == 1:
        return smart_unicode("یک هفته",encoding="utf-8")
    elif  weeks == 2:
        return smart_unicode("دو هفته",encoding="utf-8")
    elif  weeks == 3:
        return smart_unicode("سه هفته",encoding="utf-8")
    elif  weeks == 4:
        return smart_unicode("یک ماه",encoding="utf-8")
    elif  weeks >= 5:
        return smart_unicode("بیشتر از یک ماه",encoding="utf-8")
    else:
        return smart_unicode("نا‌مشخص",encoding="utf-8")

@register.filter
def persian_numbers(string):  
    res = digits.en_to_fa(str(string))
    try:
        return smart_unicode(res, encoding="utf-8")
    except:
        return ""

@register.filter
def toman_to_hezartoman(integer):
    try:
        return integer//1000
    except:
        return 0

@register.filter
def money_comma(data):
    try:
        integer = int(data)
        return ('{:,}'.format(integer))
    except:
        return ""

@register.filter
def four_digit_id(id_string):
    id_string = str(id_string)
    zero_needed = 4 - len(id_string)
    zeros = ""
    for _ in range(zero_needed):
        zeros += "0"
    res = zeros + id_string
    return res

@register.filter
def eight_digit_id(id_string):
    id_string = str(id_string)
    zero_needed = 8 - len(id_string)
    zeros = ""
    for _ in range(zero_needed):
        zeros += "0"
    res = zeros + id_string
    return res

@register.filter
def jalali_date(date):
    if not isinstance(date, datetime):
        return ""
    return JalaliDateTime(
        date.astimezone(timezone.get_default_timezone())
        ).strftime("%Y/%m/%d")

@register.filter
def jalali_time(date):
    if not isinstance(date, datetime):
        return ""
    return JalaliDateTime(
        date.astimezone(timezone.get_default_timezone())
        ).strftime("%H:%M:%S")