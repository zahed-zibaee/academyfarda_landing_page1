# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Verify, Sent
from payments.models import Discount
from persiantools import digits
from datetime import datetime,timedelta
from random import randint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def lookup(request):
    """this is a view to send sms authenticator to phone
    this POST request need ip address and phone number
    status0: submited
    status1: bad request
    status2: wait for a minutes
    status3: you blocked for a day
    return: status code and an object id(Verify)
    """
    if request.method == 'POST' and 'ip' in request.POST.keys() and 'phone' in request.POST.keys():
        ip = request.POST['ip']
        phone_fa = digits.ar_to_fa(request.POST['phone'])
        phone_en = digits.fa_to_en(phone_fa)
        # last 24h same ip
        if Verify.objects.filter(ip = ip, sent__created_date__lt = datetime.now()\
            , sent__created_date__gt = datetime.now() + timedelta(days=-1)).exists():
            if len(Verify.objects.filter(ip = ip, sent__created_date__lt = datetime.now()\
            , sent__created_date__gt = datetime.now() + timedelta(days=-1))) > 9:
                return JsonResponse({'status':'3','id':'-1'})
            elif Verify.objects.filter(sent__receptor = phone_en, sent__created_date__lt = datetime.now()\
            , sent__created_date__gt = datetime.now() + timedelta(minutes=-1)).exists():
                return JsonResponse({'status':'2','id':'-1'})
            else:
                obj = Verify.objects.create(sent = Sent.objects.create( receptor = phone_en)\
                , ip = ip, token1=''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]),\
                    token2 = ''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]) )
                obj.expiration_time = datetime.now() + timedelta(minutes=5)
                obj.save()
                obj.send()
                return JsonResponse({'status':'0','id':obj.id})
        else:
            obj = Verify.objects.create(sent = Sent.objects.create( receptor = phone_en)\
            , ip = ip, token1=''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]),\
                token2 = ''.join(["{}".format(randint(0, 9)) for num in range(0, 3)]) )
            obj.expiration_time = datetime.now() + timedelta(minutes=5)
            obj.save()
            obj.send()
            return JsonResponse({'status':'0','id':obj.id})
    else:
        return JsonResponse({'status':'1','id':'-1'})

@csrf_exempt
def validate(request):
    """this view validate sms code
    this POST request need 2 tokens named token1 and token2, one id that related to Verify object and whatnext
    status0: OK
    status1: bad request
    status2: token is wrong
    status3: object is not found
    return: status and a href url for redirection"""
    if request.method == 'POST' and 'token1' in request.POST.keys() and 'token2' in request.POST.keys()\
        and 'id' in request.POST.keys() and 'whatnext' in 'post_key':
        token1_fa = digits.ar_to_fa(request.POST['token1'])
        token1_en = digits.fa_to_en(token1_fa)
        token2_fa = digits.ar_to_fa(request.POST['token2'])
        token2_en = digits.fa_to_en(token2_fa)
        try:
            obj = Verify.objects.get(id=int(request.POST["id"])).first()
        except:
            return JsonResponse({'status':'3','href':''})
        if obj.validate(token1_en,token2_en):
            what_next = request.POST['whatnext']
            if what_next == 'CART_COURSE' and 'discount_code' in request.POST.keys() and 'course_id' in request.POST.keys():
                

                return JsonResponse({'status':'0','href':''})
        else:
            return JsonResponse({'status':'2','href':''})
    else:
        return JsonResponse({'status':'1','href':''})