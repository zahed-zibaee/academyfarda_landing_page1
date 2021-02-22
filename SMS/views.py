# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from re import compile as re_compile
from persiantools import digits
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit
from django.shortcuts import get_object_or_404

from .models import Sent, Verify
from .statuscode import STATUS_CODES

def normalize(string):
    """this methode will check for arabic charecter and will convert them
    to persian and than change persian numerics to english one"""
    not_arabic = digits.ar_to_fa(string)
    res = digits.fa_to_en(not_arabic)
    return res

@ratelimit(key='header:x-cluster-client-ip', rate='15/d', block=True, method=['POST'])
def lookup(request):
    """this is a view to send sms authenticator to phone
    this POST request need ip address and phone number and returns status and verify id
    """
    if request.method == 'POST' and 'verification_id' in request.POST.keys():
        verification_id = normalize(request.POST['verification_id'])
        verification = get_object_or_404(Verify, id = verification_id)
        now = timezone.make_aware(
                datetime.now(), 
                timezone.get_default_timezone()
                )
        last_min = now + timedelta(minutes=-1)
        last_ten_min = now + timedelta(minutes=-10)
        if last_min < verification.sent.send_date < now:
            return HttpResponseForbidden(
                "not allowed to make more than one message every minute"
            )
        #if in last 10 min we had a message we can resend it
        elif last_ten_min < verification.sent.send_date < now:
                status = verification.send()
                if status != 200:
                    return HttpResponseServerError("Kavehnegar api does not woek properly with error code: " + status)
                else:
                    return JsonResponse({})
        else:
            verification.save()
            verification.start()
            status = verification.send()
            if status != 200:
                return HttpResponseServerError("Kavehnegar api does not woek properly with error code: " + status)
            else:
                return JsonResponse({})
    else:
        return HttpResponseBadRequest("bad request")