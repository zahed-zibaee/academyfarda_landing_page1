# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Verify, Sent
from persiantools import digits
from datetime import datetime




def lookup(request):
    #TODO add user login or logout
    if request.method == 'POST':
        ip = request.POST['ip']
        phone_fa = digits.ar_to_fa(request.POST['phone'])
        phone_en = digits.fa_to_en(phone_fa)

        if Verify.objects.filter(ip = ip, expiration_time__gte = datetime.now()).exists():
            messages.error(request, "Too many request")
            return redirect("#")
        else:
            obj = Verify.objects.create(sent = Sent.objects.create(phone_en), ip = ip)
            obj.send()
            return redirect("#")
    else:
        messages.error(request, "Bad method")
        return render(request,'leads/login/login.html')

def validate(request):
    if request.method == 'POST':
        token1_fa = digits.ar_to_fa(request.POST['token1'])
        token1_en = digits.fa_to_en(token1_fa)
        token2_fa = digits.ar_to_fa(request.POST['token2'])
        token2_en = digits.fa_to_en(token2_fa)
        phone_fa = digits.ar_to_fa(request.POST['phone'])
        phone_en = digits.fa_to_en(phone_fa)

    else:
        messages.error(request, "Bad method")
        return render(request,'leads/login/login.html')