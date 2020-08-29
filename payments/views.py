# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseBadRequest\
     , HttpResponseNotFound, HttpResponseForbidden,\
     HttpResponseServerError, HttpResponseRedirect,\
     HttpResponseNotAllowed
from django.shortcuts import redirect, render
from zeep import Client
from .config import zarinpal_MERCHANT as MERCHANT
from .zarinpall_errors import error_code as ERRORCODE
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from persiantools import digits
from random import randint
from re import compile as re_compile

@csrf_exempt
def verify(request):
    """this view verify peyment with get mothod and return the answer by refrence id or an error
    this method needs Authority
    """
    if request.method == 'GET':
        if request.GET.get('Status') == 'OK':
            try:
                payment = Payment.objects.filter(authority = request.GET['Authority']).first()
            except:
                return HttpResponseNotFound("payment not found")
            client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
            result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], payment.total)
            if result.Status == 100:
                payment.status = True
                payment.ref_id = result.RefID
                payment.save()
                data = {'status':"OK",'payment':payment}
                return render(request,'receipt/index.html', data)
            elif result.Status == 101:
                payment.status = True
                payment.ref_id = result.RefID
                payment.save()
                data = {'status':"OK",'payment':payment}
                return render(request,'receipt/index.html', data)
            else:
                try:
                    error = "\"" + ERRORCODE[result.Status] + "\""
                except:
                    error = "\"" + "نامشخص" + " " + str(result.Status) + "\""
                data = {'status':"ERROR",'error':error,'payment':payment}
                return render(request,'receipt/index.html', data)
        else:
            try:
                payment = Payment.objects.filter(authority = request.GET['Authority']).first()
            except:
                return HttpResponseNotFound("payment not found")
            data = {'status':"NOK",'payment':payment}
            return render(request,'receipt/index.html', data)
    else:
        return HttpResponseNotAllowed("bad request. request must be GET")

    


@csrf_exempt
def check_discount_course(request):
    """this method will check if discount exist and valid
    it return status code and amount
    """
    if request.method == 'POST' and 'course_id' in request.POST.keys()\
        and 'discount_code' in request.POST.keys() :
        discount_code_fa = digits.ar_to_fa(request.POST['discount_code'])
        discount_code_fa_en = digits.fa_to_en(discount_code_fa)
        if Course.objects.filter(id = request.POST['course_id']).exists():
            course = Course.objects.get(id = request.POST['course_id'])
        else:
            return HttpResponseNotFound("course not found")
        if Discount.objects.filter(code = discount_code_fa_en, product =\
             Product.objects.get(id = course.id)).exists() and\
             Discount.objects.filter(code = discount_code_fa_en,
             product = course.id).first().is_active():
            discount = Discount.objects.filter(code = discount_code_fa_en).first()
            total = discount.get_total()
            return JsonResponse({'total':total})
        else:
            return HttpResponseNotFound("code not found")
    else:
        return HttpResponseBadRequest("bad request")

@csrf_exempt
def check_course(request):
    """this method will check if course exist and active
    it return active true or false
    """
    if request.method == 'POST' and 'course_id' in request.POST.keys():
        if Course.objects.filter(id = request.POST['course_id']).exists():
            course = Course.objects.get(id = request.POST['course_id'])
        else:
            return HttpResponseNotFound("course not found")
        if course.active == True:
            return JsonResponse({'avtive':'true'})
        else:
            return JsonResponse({'active':'false'})
    else:
        return HttpResponseBadRequest("bad request")

@csrf_exempt
def cart_course_create(request):
    """this method will create a course cart that has a href for payments
    this method needs course id and you can have discount_code for discount 
    and sms validation id and token1 and token2
    and course sumbit form data: name, family, gender, father_name, code_meli, address, payment_type
    """
    if request.method == 'POST' and 'course_id' in request.POST.keys() and \
        'token1' in request.POST.keys() and 'token2' in request.POST.keys()\
        and 'verify_id' in request.POST.keys() and 'name' in request.POST.keys()\
        and 'family' in request.POST.keys() and 'gender' in request.POST.keys()\
        and 'father_name' in request.POST.keys() and 'code_meli' in request.POST.keys()\
        and 'address' in request.POST.keys() and 'payment_type' in request.POST.keys():
        token1_fa = digits.ar_to_fa(request.POST['token1'])
        token1_en = digits.fa_to_en(token1_fa)
        token2_fa = digits.ar_to_fa(request.POST['token2'])
        token2_en = digits.fa_to_en(token2_fa)
        code_meli_fa = digits.ar_to_fa(request.POST['code_meli'])
        code_meli_en = digits.fa_to_en(code_meli_fa)
        ########### data validation check
        try:
            # both ids are true
            verify = Verify.objects.get(id=int(request.POST["verify_id"]))
            course = Course.objects.get(id = request.POST['course_id'])
        except:
            return HttpResponseNotFound("verify or course not found")
        pattern = re_compile("^\d{10}$")
        if pattern.match(code_meli_en) == False:
            return HttpResponseBadRequest("meli code is not 10 digits")
        pattern = re_compile("^.{3,200}$")
        if pattern.match(request.POST['name']) == False or pattern.match(request.POST['family']) ==\
            False or pattern.match(request.POST['father_name']) == False:
            return HttpResponseBadRequest("name or family or father name is too short or too long")
        pattern = re_compile("^[M,F]$")
        if pattern.match(request.POST['gender']) == False:
            return HttpResponseBadRequest("gender must be M(male) or F(female)")
        pattern = re_compile("^.{10,2000}$")
        if pattern.match(request.POST['address']) == False:
            return HttpResponseBadRequest("address is too short or too long")
        pattern = re_compile("^option[1-2]$")
        if pattern.match(request.POST['payment_type']) == False:
            return HttpResponseBadRequest("payment type is only has two options")
        ########### sms code validation
        if verify.validate(token1_en,token2_en) == False:
            return HttpResponseForbidden("sms code is not valid")
        ########### if discount code is posted 
        if 'discount_code' in request.POST.keys():
            #check for validating discount code
            if Discount.objects.filter(code = request.POST['discount_code'], product = \
                Product.objects.get(id = course.id)).exists() \
                and Discount.objects.filter(code = request.POST['discount_code'], \
                product = course.id).first().is_active():
                discount = Discount.objects.filter(code = request.POST['discount_code']).first()
            else:
                return HttpResponseForbidden("discount code is not valid")
        ########### if discount code is not posted 
        else:
            #put discount code as one with 0 discount
            if Discount.objects.filter(product = Product.objects.get(id = \
                course.id), amount = 0, active = True).exists():
                discount = Discount.objects.filter(product = Product.objects.get(id =\
                course.id), amount = 0, active = True).first()
            else:
                discount = Discount.objects.create(product = Product.objects.get(id =\
                course.id), amount = 0, active = True, code = ''.join(["{}".format(randint(0, 9))\
                 for num in range(0, 20)]))
        ########## make a cart
        cart = Cart.objects.create(verification = verify)
        cart.course.add(course)
        cart.discount.add(discount)
        cart.save()
        ########## make a payment_info
        paymentinfo = PaymentInformation.objects.create(name = request.POST['name'],\
            family = request.POST['family'], gender = request.POST['gender'], \
            father_name = request.POST['father_name'], code_meli = code_meli_en\
            , phone_number = verify.sent.receptor, address = request.POST['address'], cart = cart)
        ########## cart get_href
        description = "ثبت نام دوره تعمیرات موبایل متخصصان فردا"
        amount = int(discount.get_total())
        mobile = verify.sent.receptor
        callbackurl = "https://academyfarda.com/payments/verify"
        authority = cart.get_href(MERCHANT, description, amount, mobile, callbackurl)
        if authority[0] == False:
            return HttpResponseServerError("payment can not be done with status code:" + authority[1])
        ########## make a payment 
        payment = Payment.objects.create(payment_info = paymentinfo,total = discount.get_total()\
            , authority = authority[1], created_date = datetime.now())
        ########## return status 0 as OK and href
        url = 'https://www.zarinpal.com/pg/StartPay/' + authority[1]
        return JsonResponse({'url':url})
    else:
        return HttpResponseBadRequest("bad request")


@csrf_exempt
def get_courses(request):
    if request.method == 'POST':
        dic = {}
        dic["course"] = []
        for course in Course.objects.filter(show=True):
            dic["course"].append({"id":course.id,"name":course.get_name(),"active":course.active,"day":course.day,"time":course.time,"type":course.class_type})
        return JsonResponse(dic)
    else:
        return HttpResponseBadRequest("bad request")