

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

def error_404(request):
    #TODO: add other errors 
    data = {}
    return render(request,'404/error_404.html', data)

@csrf_exempt
def hi(request):
    if request.method == "POST" or request.method == "GET":
        return JsonResponse({'ans':'hi'})
    else:
        return HttpResponseBadRequest("bad request")