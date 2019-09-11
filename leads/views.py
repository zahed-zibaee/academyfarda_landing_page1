# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import Token, User, Lead
from django.db.models import Count
from datetime import datetime ,timedelta

# Create your views here.
@csrf_exempt
def submit_Leads(request):
    # User submit a lead
    #TODO: validate phone, date Shamsi,
    post_keys = request.POST.keys() 
    if 'token' in post_keys and User.objects.filter(token__token = request.POST['token']).exists() is True \
            and 'phone' in post_keys and Lead.objects.filter(phone_number = request.POST['phone']).exists() is False \
                and 'name' in post_keys and len(request.POST['phone']) > 5:
        Lead.objects.create(name_and_family = request.POST['name'], phone_number = request.POST['phone'], \
            description = request.POST.get('description', default=''), token = Token.objects.filter(token = request.POST['token'])[0])
        return JsonResponse({
        'status': 'submited',
        }, encoder=JSONEncoder)
    elif 'token' not in post_keys or User.objects.filter(token__token = request.POST['token']).exists() is False:
        return JsonResponse({
        'status': 'registeration_error',
        }, encoder=JSONEncoder)
    elif 'phone' not in post_keys or len(request.POST['phone']) < 6:
        return JsonResponse({
        'status': 'phone_number_needed',
        }, encoder=JSONEncoder)
    elif Lead.objects.filter(phone_number = request.POST['phone']).exists() is True:
        return JsonResponse({
        'status': 'repetitive_ phone_number',
        }, encoder=JSONEncoder)
    elif 'name' not in post_keys:
        return JsonResponse({
        'status': 'name_needed',
        }, encoder=JSONEncoder)
    else:
        return JsonResponse({
        'status': 'unknown_error',
        }, encoder=JSONEncoder)
    
def error_404(request):
    data = {}
    return render(request,'academyfarda_crm/error_404.html', data)

@csrf_exempt
def query_Leads(request):
    #TODO: date shamsi,
    post_keys = request.POST.keys() 
    if 'token' in post_keys and User.objects.filter(token__token = request.POST['token']).exists() is True:
        if 'days' not in post_keys:
            days = '30'
            last_month = datetime.today() - timedelta(days=int(days))
        else:
            days = request.POST['days']
            last_month = datetime.today() - timedelta(days=int(days))
        Leads_counts = Lead.objects.filter(led_time__gte = last_month,led_time__lte = datetime.now() \
            , register_status='K').aggregate(Count('register_status'))
        Leads_counts_value = Leads_counts.values()
        context={}
        context['registered_in_' + str(days) + '_days'] = last_month
        return JsonResponse(context, encoder=JSONEncoder)
    else:
        return JsonResponse({
            'status': 'registeration_error',
        }, encoder=JSONEncoder)

def analysis(request):
    leads_all = Lead.objects.all().aggregate(Count('id'))
    leads_registered = Lead.objects.filter(register_status = 'K').aggregate(Count('id'))
    leads_registered_value = leads_registered.values()
    leads_all_value = leads_all.values()
    leads_not_reg = leads_all_value[0] - leads_registered_value[0]

    data = { 'leads_all': leads_all_value[0], \
        'leads_reg': leads_registered_value[0], 'leads_not_reg': leads_not_reg
    }
    return render(request,'academyfarda_crm/analysis.html', data)
