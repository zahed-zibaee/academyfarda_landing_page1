# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render
import json
from urllib import quote
from random import randint
from requests import get

from .config import API_key as apikey


def send(request):
    api = "https://api.kavenegar.com/v1/" + apikey + "/sms/send.json"
    coded_message = quote("test")
    data = {
        'receptor':'09376868321,',
        'message':message,
        'sender':'10004000770077',
    }
    response = requests.get(api, params=data)
    api_status = response.json()['return']['status'] 
    messageid = response.json()['entries']['messageid'] 
    unixdate = response.json()['entries']['date'] 
    message = response.json()['entries']['message'] 
    receptor = response.json()['entries']['receptor'] 
    return HttpResponse(str(status))

def status(request):
    messageid = "1447131035"
    api = "https://api.kavenegar.com/v1/" + apikey + "/sms/status.json"
    data = {
        'messageid':'1447131035,',
    }
    response = requests.get(api, params=data)
    api_status = response.json()['return']['status'] 
    message_status = response.json()['entries'][0]['status']
    return HttpResponse(str(status))

def lookup(request):
    random1 = ''.join(["{}".format(randint(0, 9)) for num in range(0, 3)])
    random2 = ''.join(["{}".format(randint(0, 9)) for num in range(0, 3)])
    messageid = "1447131035"
    api = "https://api.kavenegar.com/v1/" + apikey + "/verify/lookup.json"
    data = {
        'receptor':'09376868321',
        'token':random1,
        'token2':random2,
        'template':'this is test for %token and %token2',
    }
    response = requests.get(api, params=data)
    api_status = response.json()['return']['status'] 
    message_status = response.json()['entries'][0]['status']
    return HttpResponse(str(status))