# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import Origin, User, Lead, Comment, Label
from datetime import datetime
from django.contrib import messages ,auth
from persiantools import digits
from persiantools.jdatetime import JalaliDateTime

#TODO: add comment to all project
@csrf_exempt
def api_submit(request):
    #TODO: frontend make lead page input pup red when error, calasify this if
    post_keys = request.POST.keys() 
    #check if there is a token and token is valid and phone is exist and not repetitive than is phone digits and name exits and not too short
    if 'token' in post_keys and Origin.objects.filter(token = request.POST['token']).exists() and Origin.objects.filter(token_activation = True) \
            and 'phone' in post_keys and Lead.objects.filter(phone_number = request.POST['phone']).exists() is False \
                and request.POST['phone'].isdigit() and 'name' in post_keys and len(request.POST['phone']) > 5 \
                    and len(request.POST['name']) > 2 :
        #change arabic numbers to persian and than to english
        phone_fa = digits.ar_to_fa(request.POST['phone'])
        phone_en = digits.fa_to_en(phone_fa)
        Lead.objects.create(name_and_family = request.POST['name'], phone_number = phone_en, \
            question = request.POST.get('question', default=''), \
                origin = Origin.objects.filter(token = request.POST['token']).first())
        return JsonResponse({
        'status': 'submited',
        }, encoder=JSONEncoder)
    elif 'token' not in post_keys or Origin.objects.filter(token = request.POST['token']).exists() is False\
         or Origin.objects.filter(token_activation = False):
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
    time = JalaliDateTime.now().strftime("%H:%M %Y-%m-%d")


    data = {'comments': comments, 'leads':leads, 'labels': labels, 'time': time}
    return render(request,'leads/export/export.html', data)

def comment_add(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_staff and len(request.POST['text']) > 0:
        post = Lead.objects.get(id=int(request.POST['post']))
        author = request.user
        text = request.POST['text']
    else:
        messages.warning(request, "You'r comment can not be saved")
        return redirect('export')
    comment = Comment(post = post, author = author, text = text)
    comment.save()
    messages.success(request, "You'r comment has been save")
    return redirect('export')


def lead_add(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_staff:
        origin = Origin.objects.filter(description = 'دیوار').first()
        name_and_family = request.POST['name_and_family']
        gender = request.POST['gender']
        phone_fa = digits.ar_to_fa(request.POST['phone_number'])
        phone_en = digits.fa_to_en(phone_fa)
        register_status = request.POST['register_status']
        operator = request.user

        if len(name_and_family) > 2 and len(phone_en) > 5 and len(phone_en) < 16 and phone_en.isdigit():
            lead = Lead(origin = origin, name_and_family = name_and_family.encode("utf-8"), gender = gender,\
                 phone_number = phone_en, register_status = register_status, operator = operator)
            lead.save()
            messages.success(request, "You'r new lead has been save")
            return redirect('export')
        else:
            messages.warning(request, "Check name and family fileld or phone number")
            return redirect('export')
    else:
        messages.warning(request, "You'r lead can not be saved")
        return redirect('export')
        
def lead_del(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_staff:
        lead = Lead.objects.filter(id=request.POST["lead_id"]).first()
        if request.user.is_superuser:
            lead.delete()
            messages.success(request, "That lead is now gone!!!") 
            return redirect('export')
        elif request.user == lead.operator and lead.origin.description == "دیوار":
            lead.delete()
            messages.success(request, "That lead is now gone!!!") 
            return redirect('export')
        else:
            messages.warning(request, "You're not operator or lead origin is undeleteable") 
            return redirect('export')
    else:
        messages.warning(request, "You're can not remove this lead") 
        return redirect('export')


def x(request):
    if request.user.is_superuser or request.method == "PUT" and request.user.is_authenticated \
            and request.user.is_staff \
                and Comment.objects.filter(id=request.POST['comment']).first().author == request.user:
        approved_comment = request.POST['approved_comment']
        if approved_comment == "True":
            Comment.objects.filter(id=request.POST['comment']).update(approved_comment=True)
        else:
            Comment.objects.filter(id=request.POST['comment']).update(approved_comment=False)
        if approved_comment == "True":
            messages.success(request, "You'r comment has been approved")
        else:
            messages.success(request, "You'r comment has been revoked") 
        return redirect('export')
    else:
        messages.success(request, "You'r comment has been save")
        return redirect('export')