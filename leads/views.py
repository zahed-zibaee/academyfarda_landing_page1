# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import Origin, User, Lead, Comment, Label, LabelDefinition
from datetime import datetime
from django.contrib import messages ,auth
from persiantools import digits
from persiantools.jdatetime import JalaliDateTime
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.admin.views.decorators import staff_member_required


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
    
@staff_member_required
def export(request):
    leads = Lead.objects.order_by('-id')
    #leads paginator
    paginator = Paginator(leads, 20)
    page = request.GET.get('page')
    if page:
        paged_leads = paginator.page(page)
    else:
        paged_leads = paginator.page(1)
    #page = paginator.get_page(page)

    comments = Comment.objects.all()
    labels = Label.objects.all()
    labels_def = LabelDefinition.objects.all()
    time = JalaliDateTime.now().strftime("%H:%M %Y-%m-%d")

    data = {'comments': comments, 'leads':paged_leads, 'labels': labels, 'time': time, 'labels_def': labels_def}
    return render(request,'leads/export/export.html', data)

@staff_member_required
def export_all(request):
    leads = Lead.objects.order_by('-id')
    comments = Comment.objects.all()
    labels = Label.objects.all()
    time = JalaliDateTime.now().strftime("%H:%M %Y-%m-%d")


    data = {'comments': comments, 'leads':leads, 'labels': labels, 'time': time}
    return render(request,'leads/export/export_all.html', data)


@staff_member_required
def comment_add(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_staff and len(request.POST['text']) > 0:
        get_object_or_404(Lead, id=int(request.POST["id"]))
        post = Lead.objects.filter(id=int(request.POST["id"])).first()
        author = request.user
        text = request.POST['text']
        comment = Comment(post = post, author = author, text = text, created_date = datetime.now(), \
        created_date_jalali = datetime.strptime(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S"), \
            "%Y-%m-%d %H:%M:%S"), created_date_jalali_str = JalaliDateTime.now().strftime("%c"))
        comment.save()
        messages.success(request, "You'r comment has been save")
        return redirect('export')
    elif len(request.POST['text']) == 0:
        messages.warning(request, "You'r comment text field is empty")
        return redirect('export')
    else:
        messages.warning(request, "You'r not authorized")
        return redirect('export')
    

@staff_member_required
def comment_approve(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_staff:
        get_object_or_404(Comment, id=int(request.POST["id"]))
        comment_id = int(request.POST["id"])
        author = Comment.objects.filter(id=comment_id).first().author
        if Comment.objects.filter(id=comment_id).first().approved_comment:
            approved = False
        else:
            approved = True
    else:
        messages.warning(request, "You'r not authorized")
        return redirect('export')
    if request.user == author:
        obj = Comment.objects.filter(id=comment_id).first()
        obj.approved_comment = approved
        obj.save()
        messages.success(request, "You'r comment state has been changed")
        return redirect('export')
    else:
        messages.warning(request, "You'r not authorized")
        return redirect('export')   

@staff_member_required
def comment_edit(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_superuser:
        get_object_or_404(Comment, id=int(request.POST["id"]))
        comment = Comment.objects.filter(id=int(request.POST["id"])).first()
        text = request.POST["text"]
        comment.text = text
        comment.save()
        messages.success(request, "You'r comment has been changed!!!")
        return redirect('export')
    else:
        messages.warning(request, "You'r not authorized")
        return redirect('export')

@staff_member_required
def comment_del(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_superuser:
        get_object_or_404(Lead, id=int(request.POST["id"]))
    else:
        messages.warning(request, "You'r not authorized")
        return redirect('export')
    comment = Comment.objects.filter(id=int(request.POST["id"])).first()
    comment.delete()
    messages.success(request, "You'r comment has been delete")
    return redirect('export')

@staff_member_required
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

        if len(name_and_family) > 2 and len(phone_en) > 5 and len(phone_en) < 16 and\
                phone_en.isdigit() and len(Lead.objects.filter(phone_number=phone_en)) == 0:
            lead = Lead(origin = origin, name_and_family = name_and_family.encode("utf-8"), gender = gender,\
                 phone_number = phone_en, register_status = register_status, operator = operator)
            lead.save()
            messages.success(request, "You'r new lead has been save")
            return redirect('export')
        elif len(name_and_family) <= 3:
            messages.warning(request, "Check name and family fileld")
            return redirect('export')
        elif len(Lead.objects.filter(phone_number=phone_en)) == 1:
            messages.warning(request, "Phone number is repetitive")
            return redirect('export')
        elif len(phone_en) <= 6 and len(phone_en) >= 16 and phone_en.isdigit() is False:
            messages.warning(request, "Phone number is in wrong format")
            return redirect('export')
        else:
            messages.warning(request, "something went wrong")
            return redirect('export')
    else:
        messages.warning(request, "You'r not authorized")
        return redirect('export')

@staff_member_required       
def lead_del_and_edit(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_staff:
        get_object_or_404(Lead, id=int(request.POST["id"]))
        lead = Lead.objects.filter(id=request.POST["id"]).first()
        if request.POST["submit"] == "delete" :
            if request.user.is_superuser or request.user == lead.operator and lead.origin.description == "دیوار":
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
            origin = Origin.objects.filter(description = 'دیوار').first()
            name_and_family = request.POST['name_and_family']
            gender = request.POST['gender']
            phone_fa = digits.ar_to_fa(request.POST['phone_number'])
            phone_en = digits.fa_to_en(phone_fa)
            register_status = request.POST['register_status']
            operator = request.user
            lead = Lead.objects.filter(id=request.POST["id"]).first()
            if len(name_and_family) > 2 and len(phone_en) > 5 and len(phone_en) < 16 and\
                phone_en.isdigit() and len(Lead.objects.filter(phone_number=phone_en)) == 0:
                lead.orgin = origin
                lead.name_and_family = name_and_family.encode("utf-8")
                lead.gender = gender
                lead.phone_number = phone_en
                lead.register_status = register_status 
                lead.operator = operator
                lead.save()
                messages.success(request, "You'r lead has been save")
                return redirect('export')
            elif len(name_and_family) <= 3:
                messages.warning(request, "Check name and family fileld")
                return redirect('export')
            elif len(Lead.objects.filter(phone_number=phone_en)) == 1:
                messages.warning(request, "Phone number is repetitive")
                return redirect('export')
            elif len(phone_en) <= 6 and len(phone_en) >= 16 and phone_en.isdigit() is False:
                messages.warning(request, "Phone number is in wrong format")
                return redirect('export')
            else:
                messages.warning(request, "something went wrong")
                return redirect('export')

    else:
        messages.warning(request, "You'r not authorized") 
        return redirect('export')

@staff_member_required       
def question_edit(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_superuser:
        get_object_or_404(Lead, id=int(request.POST["id"]))
        lead = Lead.objects.filter(id=request.POST["id"]).first()
        question = request.POST["text"]
        if len(question) > 1:
            lead.question = question
            lead.save()
            messages.success(request, "Your lead question has been changed")
            return redirect('export')
        else:
            messages.warning(request, "your question is too short!!!") 
            return redirect('export')
    else:
        messages.warning(request, "You'r not authorized") 
        return redirect('export')