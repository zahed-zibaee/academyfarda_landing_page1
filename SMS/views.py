# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render
from kavenegar import *
import json


def send(request):
    api = KavenegarAPI('')
    params = {
        'sender': '',
        'receptor': "",
        'message': ""
    }   
    response = api.sms_send(params)
    if response.Status == 200:
        return HttpResponse('code: ' + str(response.Status))
    else:
        return HttpResponse('Error code: ' + str(response.Status))

def OTP(request):
    api = KavenegarAPI('')
    params = {
        'receptor': '',
        'template': '',
        'token': '',
        'type': 'sms',#sms vs call
    }   
    response = api.verify_lookup(params)
    if response.Status == 200:
        return HttpResponse('code: ' + str(response.Status))
    else:
        return HttpResponse('Error code: ' + str(response.Status))
             
def status(request):
    api = KavenegarAPI('')
    params = {
        'messageid': '',
    }   
    response = api.sms_status(params)
    if response.Status == 200:
        return HttpResponse('code: ' + str(response.Status))
    else:
        return HttpResponse('Error code: ' + str(response.Status))
        