# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import Origin, Lead, Comment, Label, LabelDefinition
from datetime import datetime, timedelta
from django.contrib import messages ,auth
from persiantools import digits
from persiantools.jdatetime import JalaliDateTime, JalaliDate
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.admin.views.decorators import staff_member_required
from .lead_search_choices import REGISTRATION_STATUS, GENDER_CHOICES, ORIGIN_DESCRIPTION, USER_NAME_AND_FAMILY,\
        LABELDEFINITION_TAG
import pytz

#TODO: add comment to all project
@csrf_exempt
def api_submit(request):
    #TODO: frontend make lead page input pup red when error, calasify this if
    post_keys = request.POST.keys() 
    #check if there is a token and token is valid and phone is not exist and not repetitive than is phone digits and name exits and not too short
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
    data = {}
    #search
    if "phrase" in request.GET and len(request.GET["phrase"])>0:
        data.update( { "phrase":request.GET["phrase"] } )
        phrase = request.GET["phrase"]
        if phrase:
            p_name = leads.filter(name_and_family__icontains=phrase)
            p_phone = leads.filter(phone_number__icontains=phrase)
            p_comment = leads.filter(comments__text__icontains=phrase)
            p_question = leads.filter(question__icontains=phrase)
            
            leads = p_name | p_phone | p_comment | p_question
            leads = leads.distinct()

    if "operator" in request.GET and len(request.GET["operator"])>0:
        data.update( { "operator":int(request.GET["operator"]) } )
        operator = request.GET["operator"]
        if operator:
            leads = leads.filter(operator__id=operator)
    if "origin" in request.GET and len(request.GET["origin"])>0:
        data.update( { "origin":int(request.GET["origin"]) } )
        origin = request.GET["origin"]
        if origin:
            leads = leads.filter(origin__id=origin)
    if "gender" in request.GET and len(request.GET["gender"])>0:
        data.update( { "gender":request.GET["gender"] } )
        gender = request.GET["gender"]
        if gender:
            leads = leads.filter(gender=gender)
    if "status" in request.GET and len(request.GET["status"])>0:
        data.update( { "status":request.GET["status"] } )
        status = request.GET["status"]
        if status:
            leads = leads.filter(register_status=status)
    if "label1" in request.GET and len(request.GET["label1"])>0:
        data.update( { "label1":request.GET["label1"] } )
        label1 = request.GET["label1"]
        if label1:
            leads = leads.filter(label__label__color_code=label1)
    if "label2" in request.GET and len(request.GET["label2"])>0:
        data.update( { "label2":request.GET["label2"] } )
        label2 = request.GET["label2"]
        if label2:
            leads = leads.filter(label__label__color_code=label2)
    if "date_from" in request.GET and len(request.GET["date_from"])>0:
        date_from = request.GET["date_from"]
        if date_from:
            date_from_s =date_from.split("/")
            date_from = JalaliDate(int(date_from_s[0]), int(date_from_s[1]), int(date_from_s[2])).to_gregorian()
            data.update( { "date_from":date_from.strftime("%Y-%m-%d")} )
            leads = leads.filter(led_time__gte=date_from)
    if "date_to" in request.GET and len(request.GET["date_to"])>0:
        date_to = request.GET["date_to"]
        if date_to:
            date_to_s =date_to.split("/")
            date_to = JalaliDate(int(date_to_s[0]), int(date_to_s[1]), int(date_to_s[2])).to_gregorian()
            data.update( { "date_to":date_to.strftime("%Y-%m-%d")} )
            date_to += timedelta(days=1)
            leads = leads.filter(led_time__lte=date_to)
    if "date_from" not in data:
        date = datetime.now()
        date += timedelta(days=-30)
        leads = leads.filter(led_time__gte=date)
        date = date.strftime("%Y-%m-%d")
        data.update( { "date_from":date} )
    if "date_to" not in data:
        date = datetime.now()
        leads = leads.filter(led_time__lte=date)
        date = date.strftime("%Y-%m-%d")
        date = data.update( { "date_to":date} )
    if "operator" not in data:
        data.update( { "operator":request.user.id } )
        leads = leads.filter(operator__id=request.user.id)


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
    
    origins = Origin.objects.all()
    time = JalaliDateTime.now().strftime("%H:%M %Y-%m-%d")

    data.update( {'comments': comments, 'leads':paged_leads, 'labels': labels, 'time': time, 'labels_def': labels_def, \
        origins:'origins','REGISTRATION_STATUS':REGISTRATION_STATUS, 'GENDER_CHOICES':GENDER_CHOICES,\
            'ORIGIN_DESCRIPTION':ORIGIN_DESCRIPTION, 'USER_NAME_AND_FAMILY':USER_NAME_AND_FAMILY,\
                'LABELDEFINITION_TAG':LABELDEFINITION_TAG,} )
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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    elif len(request.POST['text']) == 0:
        messages.warning(request, "You'r comment text field is empty")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You'r not authorized")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

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
        messages.error(request, "You'r not authorized")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if request.user == author:
        obj = Comment.objects.filter(id=comment_id).first()
        obj.approved_comment = approved
        obj.save()
        messages.success(request, "You'r comment state has been changed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You'r not authorized")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   

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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You'r not authorized")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required
def comment_del(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_superuser:
        get_object_or_404(Comment, id=int(request.POST["id"]))
    else:
        messages.error(request, "You'r not authorized")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    comment = Comment.objects.filter(id=int(request.POST["id"])).first()
    comment.delete()
    messages.success(request, "You'r comment has been delete")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required
def label_edit_and_del(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_staff :
        get_object_or_404(Lead, id=int(request.POST["lead_id"]))
        get_object_or_404(Label, id=int(request.POST["label_id"]))
        if request.POST["submit"] == "delete" and request.user == Label.objects.filter(id=int(request.POST["label_id"])).first().owner:
            label = Label.objects.filter(id=int(request.POST["label_id"])).first()
            label.delete()
            messages.success(request, "You'r label has been delete")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif request.POST["submit"] == "edit" and request.user == Label.objects.filter(id=int(request.POST["label_id"])).first().owner:
            get_object_or_404(LabelDefinition, id=int(request.POST["label"]))
            if len(Label.objects.filter(label__id=int(request.POST["label"]), post__id=int(request.POST["lead_id"]))) == 0:
                label = Label.objects.filter(id=int(request.POST["label_id"])).first()
                label.label = LabelDefinition.objects.filter(id=int(request.POST["label"])).first()
                label.save()
                messages.success(request, "You'r label has been changed")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.warning(request, "This label exist")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif request.user != Label.objects.filter(id=int(request.POST["label_id"])).first().owner:
            messages.warning(request, "This is not you'r label")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "You'r request is not valid")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You'r not authorized")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required
def label_add(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_staff:
        get_object_or_404(Lead, id=int(request.POST["lead_id"]))
        get_object_or_404(LabelDefinition, id=int(request.POST["label"]))
        if len(Label.objects.filter(label__id=int(request.POST["label"]), post__id=int(request.POST["lead_id"]))) == 0:
            post = Lead.objects.filter(id=int(request.POST["lead_id"])).first()
            label1 = LabelDefinition.objects.filter(id=int(request.POST["label"])).first()
            label = Label(post = post, label = label1, owner = request.user)
            label.save()
            messages.success(request, "You'r label has been changed")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "This label exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You'r not authorized")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
        origin = Origin.objects.filter(id=int(request.POST['origin'])).first()

        if len(name_and_family) > 2 and len(phone_en) > 5 and len(phone_en) < 16 and\
                phone_en.isdigit() and len(Lead.objects.filter(phone_number=phone_en)) == 0:
            lead = Lead(origin = origin, name_and_family = name_and_family.encode("utf-8"), gender = gender,\
                 phone_number = phone_en, register_status = register_status, operator = operator)
            lead.save()
            messages.success(request, "You'r new lead has been save")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif len(name_and_family) <= 3:
            messages.warning(request, "Check name and family fileld")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif len(Lead.objects.filter(phone_number=phone_en)) == 1:
            messages.warning(request, "Phone number is repetitive")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif len(phone_en) <= 6 and len(phone_en) >= 16 and phone_en.isdigit() is False:
            messages.warning(request, "Phone number is in wrong format")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "something went wrong")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You'r not authorized")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required       
def lead_del_and_edit(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_staff:
        get_object_or_404(Lead, id=int(request.POST["id"]))
        lead = Lead.objects.filter(id=request.POST["id"]).first()
        if request.POST["submit"] == "delete" :
            if request.user.is_superuser:
                lead.delete()
                messages.success(request, "That lead is now gone!!!") 
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif request.user == lead.operator and lead.origin.description == "دیوار":
                lead.delete()
                messages.success(request, "That lead is now gone!!!") 
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.warning(request, "You're not operator or lead origin is undeleteable") 
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif request.POST["submit"] == "edit" and request.user == lead.operator\
                and (lead.origin.description == "دیوار" or lead.origin.description == "سایت"):
            origin = Origin.objects.filter(description = 'دیوار').first()
            name_and_family = request.POST['name_and_family']
            gender = request.POST['gender']
            phone_fa = digits.ar_to_fa(request.POST['phone_number'])
            phone_en = digits.fa_to_en(phone_fa)
            register_status = request.POST['register_status']
            operator = request.user
            origin = Origin.objects.filter(id=int(request.POST['origin'])).first()
            lead = Lead.objects.filter(id=request.POST["id"]).first()
            if len(name_and_family) > 2 and len(phone_en) > 5 and len(phone_en) < 16 and\
                phone_en.isdigit() and len(Lead.objects.filter(phone_number=phone_en)) == 0:
                lead.orgin = origin
                lead.name_and_family = name_and_family.encode("utf-8")
                lead.gender = gender
                lead.phone_number = phone_en
                lead.register_status = register_status 
                lead.operator = operator
                lead.origin = origin
                lead.save()
                messages.success(request, "You'r lead has been changed")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif len(name_and_family) > 2 and len(phone_en) > 5 and len(phone_en) < 16 and\
                phone_en.isdigit() and len(Lead.objects.filter(phone_number=phone_en, id=request.POST["id"])) == 1:
                lead.orgin = origin
                lead.name_and_family = name_and_family.encode("utf-8")
                lead.gender = gender
                lead.phone_number = phone_en
                lead.register_status = register_status 
                lead.operator = operator
                lead.origin = origin
                lead.save()
                messages.success(request, "You'r lead has been changed")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif len(name_and_family) <= 3:
                messages.warning(request, "Check name and family fileld")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif len(Lead.objects.filter(phone_number=phone_en)) == 1:
                messages.warning(request, "Phone number is repetitive")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif len(phone_en) <= 6 and len(phone_en) >= 16 and phone_en.isdigit() is False:
                messages.warning(request, "Phone number is in wrong format")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.warning(request, "something went wrong")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "You'r request is not valid")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You'r not authorized") 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required       
def question_edit(request):
    if request.method == "POST" and request.user.is_authenticated \
            and request.user.is_superuser:
        get_object_or_404(Lead, id=int(request.POST["id"]))
        lead = Lead.objects.filter(id=request.POST["id"]).first()
        question = request.POST["text"]
        lead.question = question
        lead.save()
        messages.success(request, "Your lead question has been changed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        messages.error(request, "You'r not authorized") 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))