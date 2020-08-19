# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Verify, Sent
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
    """
    post_keys = request.POST.keys() 
    if request.method == 'POST' and 'ip' in post_keys and 'phone' in post_keys:
        
        ip = request.POST['ip']
        phone_fa = digits.ar_to_fa(request.POST['phone'])
        phone_en = digits.fa_to_en(phone_fa)
        # last 24h same ip
        if Verify.objects.filter(ip = ip, sent__created_date__lt = datetime.now()\
            , sent__created_date__gt = datetime.now() + timedelta(days=-1)).exists():
            if len(Verify.objects.filter(ip = ip, sent__created_date__lt = datetime.now()\
            , sent__created_date__gt = datetime.now() + timedelta(days=-1))) > 9:
                return JsonResponse({'status':'3'})
            elif Verify.objects.filter(sent__receptor = phone_en, sent__created_date__lt = datetime.now()\
            , sent__created_date__gt = datetime.now() + timedelta(minutes=-1)).exists():
                return JsonResponse({'status':'2'})
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
        return JsonResponse({'status':'1'})

@csrf_exempt
def validate(request):
    post_keys = request.POST.keys()
    print(post_keys)
    if request.method == 'POST' and 'token1' in post_keys and 'token2' in post_keys\
        and 'id' in post_keys:
        token1_fa = digits.ar_to_fa(request.POST['token1'])
        token1_en = digits.fa_to_en(token1_fa)
        token2_fa = digits.ar_to_fa(request.POST['token2'])
        token2_en = digits.fa_to_en(token2_fa)
        try:
            obj = Verify.objects.get(id=int(request.POST["id"])).first()
        except:
            return JsonResponse({'status':'3'})
        if obj.validate(token1_en,token2_en):
            return JsonResponse({'status':'0'})
        else:
            return JsonResponse({'status':'2'})
    else:
        return JsonResponse({'status':'1'})