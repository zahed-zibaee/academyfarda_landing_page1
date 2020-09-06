# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect, render
from .models import Sent, Verify
from persiantools import digits
from datetime import datetime,timedelta
from random import randint
from django.views.decorators.csrf import csrf_exempt
import json

from .statuscode import status_codes


@csrf_exempt
def lookup(request):
    """this is a view to send sms authenticator to phone
    this POST request need ip address and phone number and returns status and verify id
    status0: submited
    status1: bad request
    status2: wait for a minutes
    status3: you blocked for a day
    return: status code and an object id(Verify)
    """
    if request.method == 'POST' and 'phone' in request.POST.keys():
        try:
            ip = request.META['REMOTE_ADDR']
        except:
            ip = request.META['X_FORWARDED_FOR']
        phone_fa = digits.ar_to_fa(request.POST['phone'])
        phone_en = digits.fa_to_en(phone_fa)
        #esist in last 24h same ip
        if len(Verify.objects.filter(ip = ip, sent__created_date__lt = datetime.now()\
             , sent__created_date__gt = datetime.now() + timedelta(days=-1))) > 10:
                return HttpResponseForbidden("not allowed to make more than 10 messages every day")
        #exist in last min
        elif Verify.objects.filter(sent__receptor = phone_en, sent__created_date__lt = datetime.now()\
            , sent__created_date__gt = datetime.now() + timedelta(minutes=-1)).exists():
                return HttpResponseForbidden("not allowed to make more than one message every minute")
        else:
            obj = Verify.objects.create(sent = Sent.objects.create( receptor = phone_en,\
                 created_date = datetime.now()), ip = ip, \
                 token1=''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]),\
                 token2 = ''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]))
            obj.expiration_time = datetime.now() + timedelta(minutes=1)
            obj.save()
            status = obj.send()
            return JsonResponse({'status':status,'id':obj.id,'status_message':status_codes[str(status)]})
    else:
        return HttpResponseBadRequest("bad request")
