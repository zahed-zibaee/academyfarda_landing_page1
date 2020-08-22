# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render
from zeep import Client
from .config import zarinpal_MERCHANT as MERCHANT
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from persiantools import digits
from random import randint
import re

@csrf_exempt
def verify(request):
    if request.GET.get('Status') == 'OK':
        payment = Payment.objects.filter(authority = request.GET['Authority']).first()
        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], Payment.amount)
        if result.Status == 100:
            payment.status = True
            payment.ref_id = result.RefID
            payment.save()
            return JsonResponse({'status':'0','refid':result.RefID})
        elif result.Status == 101:
            payment.status = True
            payment.ref_id = result.RefID
            payment.save()
            return JsonResponse({'status':'0','refid':result.RefID})
        else:
            return JsonResponse({'status':'2','refid':result.Status})
    else:
        return JsonResponse({'status':'1','refid':'Transaction failed or canceled by user'})


@csrf_exempt
def check_discount(request):
    """this method will check if discount exist and valid
    it return status code and amount
    status0: OK
    status1: bad request
    status2: bad course id
    status3: bad discount code
    """
    if request.method == 'POST' and 'course_id' in request.POST.keys()\
        and 'discount_code' in request.POST.keys() :
        if Course.objects.filter(id = request.POST['course_id']).exists():
            course = Course.objects.get(id = request.POST['course_id'])
        else:
            return JsonResponse({'status':'2','amount':'0'})
        if Discount.objects.filter(code = request.POST['discount_code'], product =\
             Product.objects.get(id = course.id)).exists() and\
             Discount.objects.filter(code = request.POST['discount_code'],
             product = course.id).first().is_active():
            discount = Discount.objects.filter(code = request.POST['discount_code']).first()
            amount = discount.last_amount()
            return JsonResponse({'status':'0','amount':amount})
        else:
            return JsonResponse({'status':'3','amount':'0'})
    else:
        return JsonResponse({'status':'1','amount':'0'})

@csrf_exempt
def check_course(request):
    """this method will check if course exist and active
    it return status code
    status0: OK
    status1: bad request
    status2: bad course id
    status3: course is not active
    """
    if request.method == 'POST' and 'course_id' in request.POST.keys():
        if Course.objects.filter(id = request.POST['course_id']).exists():
            course = Course.objects.get(id = request.POST['course_id'])
        else:
            return JsonResponse({'status':'2'})
        if course.active == True:
            return JsonResponse({'status':'0'})
        else:
            return JsonResponse({'status':'3'})
    else:
        return JsonResponse({'status':'1'})

@csrf_exempt
def cart_course_create(request):
    """this method will create a course cart that has a href for payments
    this method needs course id and you can have discount_code for discount 
    and sms validation id and token1 and token2
    and course sumbit form data: name, family, gender, father_name, code_meli, address, payment_type
    status0: OK
    status1: bad request
    status2: bad data
    status3: sms validation code is wrong
    status4: payment error
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
            return JsonResponse({'status':'2','href':''})
        pattern = re.compile("^\d{10}$")
        if pattern.match(code_meli_en) == False:
            return JsonResponse({'status':'2','href':''})
        pattern = re.compile("^.{3,200}$")
        if pattern.match(request.POST['name']) == False or pattern.match(request.POST['family']) ==\
            False or pattern.match(request.POST['father_name']) == False:
            return JsonResponse({'status':'2','href':''})
        pattern = re.compile("^[M,F]$")
        if pattern.match(request.POST['gender']) == False:
            return JsonResponse({'status':'2','href':''})
        pattern = re.compile("^.{10,2000}$")
        if pattern.match(request.POST['address']) == False:
            return JsonResponse({'status':'2','href':''})
        pattern = re.compile("^.{^option[1-2]}$")
        if pattern.match(request.POST['payment_type']) == False:
            return JsonResponse({'status':'2','href':''})
        ########### sms code validation
        if verify.validate(token1_en,token2_en) == False:
            return JsonResponse({'status':'3','href':''})
        ########### if discount code is posted 
        if 'discount_code' in request.POST.keys():
            #check for validating discount code
            if Discount.objects.filter(code = request.POST['discount_code'], product = \
                Product.objects.get(id = course.id)).exists() \
                and Discount.objects.filter(code = request.POST['discount_code'], \
                product = course.id).first().is_active():
                discount = Discount.objects.filter(code = request.POST['discount_code']).first()
            else:
                return JsonResponse({'status':'3','href':''})
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
        amount = int(discount.last_amount())
        mobile = verify.sent.receptor
        callbackurl = "https://academyfarda.com/payments/verify"
        authority = cart.get_href(MERCHANT, description, amount, mobile, callbackurl)
        if authority[0] == False:
            return JsonResponse({'status':'4','href':authority[1]})
        ########## make a payment 
        payment = Payment.objects.create(payment_info = paymentinfo,amount = discount.last_amount()\
            , authority = authority[1], created_date = datetime.now())
        ########## return status 0 as OK and href
        url = 'https://www.zarinpal.com/pg/StartPay/' + authority[1]
        return JsonResponse({'status':'0','href':url})
        