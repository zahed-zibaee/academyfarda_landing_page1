# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from .models import Sent, Verify
from persiantools import digits
from datetime import datetime,timedelta
from django.utils import timezone
from random import randint
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit

from .statuscode import STATUS_CODES


#TODO: add logging of admin to view
#TODO: add limitter
#TODO: add validation
def normalize(string):
    """this methode will check for arabic charecter and will convert them
    to persian and than change persian numerics to english one"""
    not_arabic = digits.ar_to_fa(string)
    res = digits.fa_to_en(not_arabic)
    return res

@ratelimit(key='ip', rate='30/d')
def lookup(request):
    """this is a view to send sms authenticator to phone
    this POST request need ip address and phone number and returns status and verify id
    """
    if request.method == 'POST' and 'phone' in request.POST.keys():
        phone = normalize(request.POST['phone'])
        #exist in last min
        if Verify.objects.filter(
            sent__receptor = phone, 
            sent__created_date__lt = datetime.now(), 
            sent__created_date__gt = datetime.now()
            ).exists():
            return HttpResponseServerError(
                "not allowed to make more than one message every minute"
            )
        #if in last 9 min we had a message we can resend it
        elif Verify.objects.filter(
            sent__receptor = phone, 
            sent__created_date__lt = datetime.now(), 
            sent__created_date__gt = datetime.now()
            ).exists():
                sms = Verify.objects.filter(
                sent__receptor = phone, 
                sent__created_date__lt = datetime.now(), 
                sent__created_date__gt = datetime.now()
                ).last()
                status = sms.send()
                return JsonResponse(
                    {
                        'status': status,
                        'id': sms.id,
                        'status_message': STATUS_CODES[str(status)]
                    }
                )
        else:
            sms = Verify.objects.create(
                sent = Sent.objects.create(receptor = phone),
            )
            sms.save()
            status = sms.send()
            return JsonResponse(
                {
                    'status':status,
                    'id':sms.id,
                    'status_message':STATUS_CODES[str(status)]
                 }
            )
    else:
        return HttpResponseBadRequest("bad request")
