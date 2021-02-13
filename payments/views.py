# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from persiantools import digits
from re import compile as re_compile
from zeep import Client
from django.http import HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden,\
    HttpResponseServerError,HttpResponseNotAllowed, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit
from django.utils.encoding import smart_unicode

from .config import ZARINPAL_MERCHANT as MERCHANT_CODE
from .zarinpall_errors import ERROR_CODES

from SMS.models import Verify, Sent
from .models import *


User = get_user_model()
#TODO: add validation to view
#TODO: add limitter to view
#TODO: add logging of admin to view
def normalize(data):
    """this methode will check for arabic charecter and will convert them
    to persian and than change persian numerics to english one"""
    try:
        string = str(data)
    except:
        string = data
    not_arabic = digits.ar_to_fa(string)
    res = digits.fa_to_en(not_arabic)
    return res

#class based
def get_zarinpal_payment_url(self, MERCHANT, description, amount, mobile, CallbackURL):
        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        result = client.service.PaymentRequest(
            MERCHANT, 
            amount, 
            description, 
            mobile, 
            CallbackURL
        )
        if result.Status == 100:
            return True, str(result.Authority)
        else:
            return False, str(result.Status)

#chane to class based
@csrf_exempt
def verify_zarinpal_payment(request):
    """this view verify peyment with get mothod and return the answer by refrence id or an error
    this method needs Authority
    """
    if request.method == 'GET':
        if request.GET.get('Status') == 'OK':
            try:
                authority = request.GET['Authority']
                payment_id = Payment.objects.filter(authority = authority).order_by("-created_date").first().id
                payment = Payment.objects.get(id=payment_id)
            except:
                return HttpResponseNotFound("payment not found")
            client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
            try:
                result = client.service.PaymentVerification(
                    MERCHANT_CODE,
                    request.GET['Authority'],
                    payment.total
                    )
            except:
                return HttpResponseServerError("can not connect to zarinpal server")
            if result.Status == 100 or result.Status == 101:
                payment.status = True
                payment.ref_id = result.RefID
                payment.save()
                if payment.send_receipt == False:
                    payment.send_receipt_course()
                data = {'status':"OK",'payment':payment, 'error_code': None}
                if len(payment.cart.course_with_discount.all()) > 0:
                    data.update( {'discount' : True} )
                return render(request,'receipt/index.html', data)
            else:
                try:
                    error = "\"" + ERROR_CODES[result.Status] + "\""
                except:
                    error = "\"" + "نامشخص" + " " + str(result.Status) + "\""
                data = {'status':"ERROR",'payment':payment, 'error_code': error}
                if len(payment.cart.discount.all()) > 0:
                    data.update( {'discount' : True} )
                return render(request,'receipt/index.html', data)
        else:
            try:
                payment_id = Payment.objects.filter(authority = request.GET['Authority']).order_by("-created_date").first().id
                payment = Payment.objects.get(id=payment_id)
            except:
                return HttpResponseNotFound("payment not found")
            data = {'status':"NOK",'payment':payment, 'error_code': None}
            if len(payment.cart.discount.all()) > 0:
                    data.update( {'discount' : True} )
            return render(request,'receipt/index.html', data)
    else:
        return HttpResponseNotAllowed("bad request.")




@csrf_exempt
def cart_course_create(request):
    """this method will create a course cart that has a href for payments
    this method needs course id and you can have discount_code for discount 
    and sms validation id and token1 and token2
    and course sumbit form data: name, family, gender,
    father_name,code_meli, address, payment_type, operator
    """
    if request.method == 'POST':
        # data validation check
        if 'course_id' in request.POST.keys() and\
        'token1' in request.POST.keys() and\
        'token2' in request.POST.keys() and\
        'verify_id' in request.POST.keys() and\
        'name' in request.POST.keys() and\
        'family' in request.POST.keys() and\
        'gender' in request.POST.keys() and\
        'father_name' in request.POST.keys() and\
        'code_meli' in request.POST.keys() and\
        'address' in request.POST.keys() and\
        'payment_type' in request.POST.keys():
            ## verification
            try:
                # check fir existence of the verification
                verify = Verify.objects.get(id = int(request.POST["verify_id"]))
            except :
                return HttpResponseNotFound("verification not found")
            # check if the sms verification
            token1 = normalize(request.POST['token1'])
            token2 = normalize(request.POST['token2'])
            if verify.validate(token1,token2) == False:
                return HttpResponseForbidden("sms code is not validated")
            ## product check
            # TODO: add stock check
            # check if course and verify id are there
            try:
                # check for existence of the course
                course = Verify.objects.get(id = int(request.POST["course_id"]))
            except:
                return HttpResponseNotFound("course not found")       
            # discount code check 
            if 'discount_code' in request.POST.keys():
                discount_code = normalize(request.POST['discount_code'])
                # check for validating discount code
                if Discount.objects.filter(code = discount_code).exists() and\
                    Discount.objects.filter(code = discount_code).first().is_active(course.id):
                    discount = Discount.objects.filter(code = discount_code).first()
                else:
                    return HttpResponseForbidden("discount code is not valid")
            else:
                discount = None
            # check for discount and course activation
            if discount is None:
                if not course.is_active():
                    return HttpResponseNotFound("product is inactive") 
            else:
                if not discount.is_active():
                    return HttpResponseNotFound("product is inactive") 
            ## personal information
            code_meli = normalize(request.POST['code_meli'])
            pattern = re_compile("^\d{10}$")
            if pattern.match(code_meli) == False:
                return HttpResponseBadRequest("meli code is not 10 digits")
            pattern = re_compile("^.{3,200}$")
            if pattern.match(request.POST['name']) == False or pattern.match(request.POST['family']) ==\
                False or pattern.match(request.POST['father_name']) == False:
                return HttpResponseBadRequest("'name'', 'family' or 'father name' is too short or too long")
            pattern = re_compile("^[M,F]$")
            if pattern.match(request.POST['gender']) == False:
                return HttpResponseBadRequest("gender must be M(male) or F(female)")
            pattern = re_compile("^.{10,2000}$")
            if pattern.match(request.POST['address']) == False:
                return HttpResponseBadRequest("address is too short or too long")
            pattern = re_compile("^option[1-2]$")
            if pattern.match(request.POST['payment_type']) == False:
                return HttpResponseBadRequest("payment type is only has two options")
            personalinfo = PersonalInformation.objects.create(
                name = request.POST['name'],
                family = request.POST['family'],
                gender = request.POST['gender'],
                father_name = request.POST['father_name'],
                code_meli = code_meli,
                phone_number = verify.sent.receptor,
                address = request.POST['address'],
            )        
            ## cart
            cart = Cart.objects.create()
            if 'discount' is not None:
                cart.courses.add(course)
            else:
                cart.courses_with_discount.add(discount)
            cart.save()
            ## cart get_href
            description = "ثبت نام دوره تعمیرات موبایل متخصصان فردا"
            amount = cart.total()
            mobile = verify.sent.receptor
            callbackurl = "https://academyfarda.com/payments/verify"
            authority = cart.get_href(MERCHANT_CODE, description, amount, mobile, callbackurl)
            if authority[0] == False:
                return HttpResponseServerError("payment can not be done with status code:" + authority[1])
            ## payment
            payment = Payment.objects.create(
                verification = verify,
                total = amount,
                authority = authority[1].encode('utf-8'),
                created_date = datetime.now(),
                cart = cart,
                personal_info = personalinfo,
            )
            # check if total is not less than low limit
            if not payment.check_total():
                return HttpResponseForbidden("total amount is less thant low limit")
            ## add operator if it exist
            if "operator" in request.POST.keys():
                op = User.objects.get(id=int(request.POST["operator"]))
                payment.operator = op
                payment.save()
            ## return status 0 as OK and redirect url
            url = 'https://www.zarinpal.com/pg/StartPay/' + authority[1]
            return JsonResponse({'url':url})
        else:
            return HttpResponseBadRequest("bad data")

    else:
        return HttpResponseBadRequest("bad request")

