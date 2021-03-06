# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect,\
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import Origin, Lead, Comment, Label
from datetime import datetime, timedelta
from django.contrib import messages
from persiantools import digits
from persiantools.jdatetime import JalaliDateTime, JalaliDate
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from random import choice
from ratelimit.decorators import ratelimit

from .lead_search_choices import REGISTRATION_STATUS, GENDER_CHOICES,\
    ORIGIN_DESCRIPTION, USER_NAME_AND_FAMILY, LABELDEFINITION_TAG
from academyfarda_backend import LEAD_OPERATORS
from users.models import User

#TODO: add comment to all project
def normalize(data):
    """this methode will check for arabic charecter and will convert them
    to persian and than change persian numerics to english one"""
    string = str(data)
    not_arabic = digits.ar_to_fa(string)
    res = digits.fa_to_en(not_arabic)
    return res


@csrf_exempt
@ratelimit(key='ip', rate='10/d')
def api_submit(request):
    if request.method == "POST":
        post_keys = request.POST.keys() 
        if 'token' not in post_keys or Origin.objects.filter(token = request.POST['token'], token_activation = True).exists() is False:
            return HttpResponseForbidden("bad authentication")
        elif 'name' not in post_keys or not 2 < (request.POST['name']) < 100 :
            return HttpResponseBadRequest("bad name field")
        elif 'phone' not in post_keys or not 5 < len(request.POST['phone']) < 16 or request.POST['phone'].isdigit() is False:
            return HttpResponseBadRequest("bad phone number field")
        elif Lead.objects.filter(phone_number = request.POST['phone']).exists() is True:
            return HttpResponseNotAllowed("repetitive phone number")
        else:
            token = normalize(request.POST['token'])
            phone = normalize(request.POST['phone'])
            my_lead = Lead.objects.create(
                name_and_family = request.POST['name'],
                phone_number = phone,
                question = request.POST.get('question', default=''),
                origin = Origin.objects.filter(token = token).first()
            )
        try:
            my_operator = choice(LEAD_OPERATORS)
            my_lead.operator.add(User.objects.filter(username = my_operator).first())
        except:
            pass
        return JsonResponse({
        'status': 'submitted',
        }, encoder=JSONEncoder)
    else:
        return HttpResponseBadRequest("bad request")
    
@staff_member_required
def export(request):
    data = {}
    #operators can not know each other leads
    if request.user.is_superuser:
        leads = Lead.objects.order_by('-id')
        if "operator" in request.GET and len(request.GET["operator"])>0:
            data.update( { "operator":int(request.GET["operator"]) } )
            operator = request.GET["operator"]
            if operator:
                leads = leads.filter(operator__id=operator)
    else:
        leads = Lead.objects.filter(operator__id=request.user.id).order_by('-id')

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
    # if there is no date show last month
    if "date_from" not in data:
        date = datetime.now()
        date -= timedelta(days=30)
        leads = leads.filter(led_time__gte=date)
        date = date.strftime("%Y-%m-%d")
        data.update( { "date_from":date} )
    if "date_to" not in data:
        date = datetime.now()
        date += timedelta(days=1)
        leads = leads.filter(led_time__lte=date)
        date = date.strftime("%Y-%m-%d")
        date = data.update( { "date_to":date} )


    #leads paginator
    paginator = Paginator(leads, 30)
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
        created_date_jalali = JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S"), \
            created_date_jalali_str = JalaliDateTime.now().strftime("%c"))
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
        #if label is uniqe for this lead
        if len(Label.objects.filter(label__id=int(request.POST["label"]), post__id=int(request.POST["lead_id"]))) == 0:
            post = Lead.objects.filter(id=int(request.POST["lead_id"])).first()
            label1 = LabelDefinition.objects.filter(id=int(request.POST["label"])).first()
            label = Label(post = post, label = label1, owner = request.user , created_date = datetime.now(), \
                created_date_jalali = JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S"), \
                    created_date_jalali_str = JalaliDateTime.now().strftime("%c"))
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
        name_and_family = request.POST['name_and_family']
        gender = request.POST['gender']
        phone_fa = digits.ar_to_fa(request.POST['phone_number'])
        phone_en = digits.fa_to_en(phone_fa)
        register_status = request.POST['register_status']
        operator = request.user
        origin = Origin.objects.filter(id=int(request.POST['origin'])).first()
        #fields should be validate
        if len(name_and_family) > 2 and len(phone_en) > 5 and len(phone_en) < 16 and\
                phone_en.isdigit() and len(Lead.objects.filter(phone_number=phone_en)) == 0:
            lead = Lead(origin = origin, name_and_family = name_and_family.encode("utf-8"), gender = gender,\
                phone_number = phone_en, register_status = register_status,\
                led_time = datetime.now(),led_time_jalali = JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S"),\
                led_time_jalali_str = JalaliDateTime.now().strftime("%c"))
            #if lead is registered save operator
            if register_status == "K":
                lead.registered_by = request.user
            else:
                lead.registered_by = None
            lead.save()
            lead.operator.add(operator)
            messages.success(request, "You'r new lead has been save")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        #if same phone number added by 1 or more operators
        elif len(Lead.objects.filter(phone_number=phone_en)) == 1:
            lead = Lead.objects.filter(phone_number=phone_en).first()
            if request.user in lead.operator.all():
                messages.warning(request, "Phone number is repetitive")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                if lead.register_status != "K":
                    lead.operator.add(request.user)
                    lead.save()
                    messages.info(request, "lead is repetitive but you added to this lead operators")
                    messages.success(request, "You'r new lead has been save")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.info(request, "lead is repetitive and registered by another operator")
                    messages.warning(request, "You'r new lead did not changed!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif len(name_and_family) <= 3:
            messages.warning(request, "Check name and family fileld")
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
            else:
                messages.warning(request, "You're not superuser") 
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif request.POST["submit"] == "edit":
            name_and_family = request.POST['name_and_family']
            gender = request.POST['gender']
            phone_fa = digits.ar_to_fa(request.POST['phone_number'])
            phone_en = digits.fa_to_en(phone_fa)
            register_status = request.POST['register_status']
            origin = Origin.objects.filter(id=int(request.POST['origin'])).first()
            lead = Lead.objects.filter(id=request.POST["id"]).first()
            #later we need for regester leads with 2 or more operators
            if name_and_family == lead.name_and_family and gender == lead.gender\
                and phone_en == lead.phone_number and register_status != lead.register_status\
                    and origin == lead.origin:
                status_changed = True
            else:
                status_changed = False
            #fields should be valid
            if len(name_and_family) > 2 and len(phone_en) > 5 and len(phone_en) < 16 and\
                    phone_en.isdigit():
                #edited phone should not be other lead phone number
                if (len(Lead.objects.filter(phone_number=phone_en)) == 1 \
                    and lead.id == Lead.objects.filter(phone_number=phone_en).first().id)\
                        or len(Lead.objects.filter(phone_number=phone_en)) == 0:
                    if request.user.is_superuser:
                        lead.orgin = origin
                        lead.name_and_family = name_and_family.encode("utf-8")
                        lead.gender = gender
                        lead.phone_number = phone_en
                        lead.register_status = register_status
                        #if lead is registered save operator
                        if register_status == "K":
                            lead.registered_by = request.user
                        else:
                            lead.registered_by = None
                        lead.save()
                        messages.success(request, "You'r lead has been changed")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    #only single owner operator can change this lead or superuser
                    elif request.user in lead.operator.all() and len(lead.operator.all()) < 2:
                        lead.orgin = origin
                        lead.name_and_family = name_and_family.encode("utf-8")
                        lead.gender = gender
                        lead.phone_number = phone_en
                        lead.register_status = register_status
                        #if lead is registered save operator
                        if register_status == "K":
                            lead.registered_by = request.user
                        else:
                            lead.registered_by = None
                        lead.save()
                        messages.success(request, "You'r lead has been changed")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    #want make operator register    
                    elif status_changed and request.user in lead.operator.all() and len(lead.operator.all()) > 1:
                        if (lead.register_status == "K" and lead.registered_by == request.user) or  lead.register_status != "K":
                            lead.register_status = register_status
                            #if lead is registered save operator
                            if register_status == "K":
                                lead.registered_by = request.user
                            else:
                                lead.registered_by = None
                            lead.save()
                            messages.success(request, "You'r lead has been registered")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                        else:
                            messages.warning(request, "You'r can not change lead status")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    else:
                        messages.warning(request, "This is not you'r lead") 
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))                  
                else:
                    messages.warning(request, "Phone number is repititive")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif len(phone_en) <= 6 and len(phone_en) >= 16 and phone_en.isdigit() is False:
                messages.warning(request, "Phone number is in wrong format")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif len(name_and_family) <= 3:
                messages.warning(request, "Check name and family fileld")
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
    if request.method == "POST" and request.user.is_authenticated\
        and request.user.is_staff:
        get_object_or_404(Lead, id=int(request.POST["id"]))
        lead = Lead.objects.filter(id=request.POST["id"]).first()
        question = request.POST["text"]
        if request.user.is_superuser:
            lead.question = question
            lead.save()
            messages.success(request, "Your lead question has been changed")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif request.user in lead.operator.all() and len(lead.operator.all()) < 2:
            lead.question = question
            lead.save()
            messages.success(request, "Your lead question has been changed")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "you are not only operator of this lead") 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You'r not authorized") 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))