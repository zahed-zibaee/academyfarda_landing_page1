# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import Token, User, Lead, Comment, Label
from django.db.models import Count
from datetime import datetime ,timedelta
from django.contrib import messages ,auth
from persiantools import characters, digits

#TODO: add comment to all project
@csrf_exempt
def submit_Leads(request):
    #TODO: frontend make lead page input pup red when error
    post_keys = request.POST.keys() 
    #check if there is a token and token is valid and phone is exist and not repetitive than is phone digits and name exits and not too short
    if 'token' in post_keys and User.objects.filter(token__token = request.POST['token']).exists() is True \
            and 'phone' in post_keys and Lead.objects.filter(phone_number = request.POST['phone']).exists() is False \
                and request.POST['phone'].isdigit() and 'name' in post_keys and len(request.POST['phone']) > 5 \
                    and len(request.POST['name']) > 2 :
        #change arabic numbers to persian and than to english
        phone_fa = digits.ar_to_fa(request.POST['phone'])
        phone_en = digits.fa_to_en(phone_fa)
        Lead.objects.create(name_and_family = request.POST['name'], phone_number = phone_en, \
            question = request.POST.get('question', default=''), \
                origin = Token.objects.filter(token = request.POST['token'])[0])
        return JsonResponse({
        'status': 'submited',
        }, encoder=JSONEncoder)
    elif 'token' not in post_keys or User.objects.filter(token__token = request.POST['token']).exists() is False:
        return JsonResponse({
        'status': 'registeration_error',
        }, encoder=JSONEncoder)
    elif 'name' not in post_keys or len(request.POST['name']) < 3 :
        return JsonResponse({
        'status': 'name_needed',
        }, encoder=JSONEncoder)
    elif 'phone' not in post_keys or len(request.POST['phone']) < 6 or request.POST['phone'].isdigit() is False:
        return JsonResponse({
        'status': 'phone_number_needed',
        }, encoder=JSONEncoder)
    elif Lead.objects.filter(phone_number = request.POST['phone']).exists() is True:
        return JsonResponse({
        'status': 'repetitive_ phone_number',
        }, encoder=JSONEncoder)

    else:
        return JsonResponse({
        'status': 'unknown_error',
        }, encoder=JSONEncoder)
    
def error_404(request):
    #TODO: add other errors 
    data = {}
    return render(request,'404/error_404.html', data)

def analysis(request):
    #TODO do the frontend and graphs
    leads_all = Lead.objects.all().aggregate(Count('id'))
    leads_registered = Lead.objects.filter(register_status = 'K').aggregate(Count('id'))
    leads_registered_value = leads_registered.values()
    leads_all_value = leads_all.values()
    leads_not_reg = leads_all_value[0] - leads_registered_value[0]
 
    data = {'leads_all': leads_all_value[0], \
        'leads_reg': leads_registered_value[0], 'leads_not_reg': leads_not_reg
    }
    return render(request,'leads/analysis/analysis.html', data)

def login(request):
    #TODO add user login or logout
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username ,password=password )

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now loged in')
            return redirect("dashboard")
        else:
            messages.error(request, "You'r username or passwerd is wrong")
            return redirect("login")
    else:
        return render(request,'leads/login/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now loged out')
        return redirect('login')
    else:
        messages.error(request, "Something went wrong!!!")
        return redirect('login')

def dashboard(request):
    #TODO add search and filters, make user only see commend they need 2 see, sort commends,padging
    leads = Lead.objects.all()
    comments = Comment.objects.all()
    data = {'comments': comments, 'leads':leads, }
    return render(request,'leads/dashboard/dashboard.html', data)


def landing2(request):
    data = {}
    return render(request,'landing/2/index.html', data)

def thanks(request):
    data = {}
    return render(request,'landing/thanks/thanks.html', data)

def export(request):
    leads = Lead.objects.all()
    comments = Comment.objects.all()
    labels = Label.objects.all()


    data = {'comments': comments, 'leads':leads, 'labels': labels}
    return render(request,'leads/export/export.html', data)