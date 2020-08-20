# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render
from zeep import Client
from .config import zarinpal_MERCHANT
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

MERCHANT = zarinpal_MERCHANT
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "ثبت نام دوره تعمیرات موبایل متخصصان فردا"  # Required
mobile = '09376868321'  # Optional
CallbackURL = "https://www.academyfarda.com/payment/verify/" # Important: need to edit for realy server.

def send_request(request):
    result = client.service.PaymentRequest(MERCHANT, amount, description, mobile, CallbackURL=CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')


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
             Product.objects.get(id = course.product_ptr_id)).exists() and\
             Discount.objects.filter(code = request.POST['discount_code'],
             product = course.product_ptr_id).first().is_active():
            discount = Discount.objects.filter(code = request.POST['discount_code']).first()
            amount = discount.last_amount()
            return JsonResponse({'status':'0','amount':amount})
        else:
            return JsonResponse({'status':'3','amount':'0'})
    else:
        return JsonResponse({'status':'1','amount':'0'})

def cart_course(request):
    """this method will make or get cart id of a course
    this method needs course id and you can have discount_code fir discount
    """
    if request.method == 'POST' and 'course_id' in request.POST.keys() :
        if Course.objects.filter(id = request.POST['course_id']).exists():
            course = Course.objects.get(id = request.POST['course_id'])
            if 'discount_code' in request.POST.keys():
                #check for validating discount code
                if Discount.objects.filter(code = request.POST['discount_code'], product = \
                    Product.objects.get(id = course.product_ptr_id)).exists() \
                    and Discount.objects.filter(code = request.POST['discount_code'], \
                    product = course.product_ptr_id).first().is_active():
                    discount = Discount.objects.filter(code = request.POST['discount_code']).first()
            if course and discount:
                cart = Cart.objcets.create(discount = discount, course = course)
                return cart.id
            else:
                if Discount.objects.filter(product = Product.objects.get(id = \
                    course.product_ptr_id), amount = 0).exists():
                    discount = Discount.objects.filter(product = Product.objects.get(id = \
                    course.product_ptr_id), amount = 0).first()
                else:
                    discount = Discount.objects.create(product = Product.objects.get(id = \
                    course.product_ptr_id), amount = 0)
                cart = Cart.objcets.create(discount = discount, course = course)
                return cart.id
        else:
            print("no course exist")
    else:
        pass