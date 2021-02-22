

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse


def error_404(request):
    #TODO: add other errors 
    data = {}
    return render(request,'404/error_404.html', data)

@csrf_exempt
def hi(request):
    return JsonResponse({'ans':'hi'})

def landing_redirect(request):
    url = reverse('common_landing')
    if 'op' in request.GET.keys():
        url += "?op=" + request.GET["op"]    
    return redirect(url)