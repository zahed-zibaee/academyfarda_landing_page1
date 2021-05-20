# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from persiantools import digits
from json import loads
from re import compile as re_compile
from ratelimit.decorators import ratelimit
from django.http import HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseRedirect, \
    JsonResponse, HttpResponseForbidden, \
    HttpResponseServerError, HttpResponse
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse
from random import choice

from .phone_numbers import PHONE_NUMBER_CHOICES

#change theese to app name ...
from SMS.models import Verify, Sent
from payments.models import Course, Payment, Cart, \
    PersonalInformation, Student, DiscountCode


User = get_user_model()

def en_ar_to_persian(data):
    """this methode will check for arabic charecter and will convert them
    to persian and than change persian numerics to english one"""
    try:
        string = str(data)
    except:
        string = data
    not_arabic = digits.ar_to_fa(string)
    res = digits.fa_to_en(not_arabic)
    return res

#TODO: need a limmiter
class CommonLanding(TemplateView):
    """for render and register in common courses"""

    def get(self, request):
        """loads common landing and courses"""
        # try to find if link is for an operator
        try:
            operator = User.objects.get(pk=request.GET["op"]).username
        except:
            operator = None
        # show all courses by site_order
        courses = Course.objects.filter(active=True, site_show=True).order_by("order")
        # pass courses to show in landing and operator for tracking for registration
        data = {"courses": courses, "operator_username": operator, 'phone': choice(PHONE_NUMBER_CHOICES)}
        return render(request, 'landing/index.html', context = data)

    @method_decorator(ratelimit(key='header:x-cluster-client-ip', rate='20/d', block=True, method='POST'))
    def post(self, request):
        """register by this"""
        #normalize data
        request.POST = request.POST.copy()
        code_meli = en_ar_to_persian(request.POST["code_meli"])
        phone = en_ar_to_persian(request.POST["phone"])
        pattern = re_compile("^\+98\d{10}$")
        pattern2 = re_compile("^98\d{10}$")
        if pattern.match(phone):
            phone = "0" + phone[3:]
        elif pattern2.match(phone):
            phone = "0" + phone[2:]
        #check data validation
        if not 3 <= len(request.POST["name"]) <= 50:
            return HttpResponseBadRequest("bad data name")
        if not 3 <= len(request.POST["family"]) <= 50:
            return HttpResponseBadRequest("bad data family")
        if not 3 <= len(request.POST["father_name"]) <= 50:
            return HttpResponseBadRequest("bad data father_name")
        if not (request.POST["gender"] == "M" or request.POST["gender"] == "F"):
            return HttpResponseBadRequest("bad data gender")
        pattern = re_compile("^\d{10}$")
        if not pattern.match(code_meli):
            return HttpResponseBadRequest("bad data code_meli")
        pattern = re_compile("^09\d{9}$")
        if not pattern.match(phone):
            return HttpResponseBadRequest("bad data phone")
        if not 10 <= len(request.POST["address"]) <= 1000:
            return HttpResponseBadRequest("bad data address")
        course = get_object_or_404(Course, id = int(request.POST["course"]))
        if not course.is_active():
                HttpResponseBadRequest("course is not active")
        if not (request.POST["installment"] == "0" or request.POST["installment"] == "1"):
            return HttpResponseBadRequest("bad data payment_type")
        else:
            if request.POST["installment"] == "1":
                installment = True
            else:
                installment = False
        # make payment object for tracking lead
        payment = Payment.objects.create(
            cart = Cart.objects.create(
                cart_type = "0",
                installment = installment,
            ), 
            # only make a verification object for later
            verification = Verify.objects.create(
                sent = Sent.objects.create(
                    receptor = phone,
                )
            ), 
            # save personal info for get lead if register not complete
            customer = PersonalInformation.objects.create(
                    name = request.POST["name"],
                    family = request.POST["family"],
                    gender = request.POST["gender"],
                    father_name = request.POST["father_name"],
                    code_meli = code_meli,
                    phone_number = phone,
                    address = request.POST["address"],
                    birthday = datetime(1621, 3, 21)
                ),
                total = 0,
            # this total is for only course registration price not discount included
        )
        # add course to cart
        # if discount added we need to remove this from cart
        payment.cart.products.add(course)
        try:
            # try to track operator
            operator = User.objects.get(username = request.POST["operator_username"])
            payment.operator = operator
        except:
            pass
        # save payment to generate slug
        payment.save()
        payment.set_absolute_url()
        # go to verify/id page to verify payment by user
        return HttpResponseRedirect("/landing/common/register/" + payment.slug)

class CommonLandingRegister(TemplateView):
    #on post make verification happend and if its success redirect to bank
    #after payment we need to show and send receipt
    ##### add student to class after payment
    #    course = payment.cart.products.get()
    #    course.student.add(payment.student)
    #    course.save()

    @method_decorator(ratelimit(key='header:x-cluster-client-ip', rate='20/d', block=True, method='GET'))
    def get(self, request, slug):
        payment = get_object_or_404(Payment, slug = slug)
        if payment.payment_type != "O":
            return HttpResponseBadRequest("this payment is not online")
        total = payment.cart.get_total()
        prepayment = payment.cart.get_prepayment_course()
        pay = payment.cart.get_installments_course()[0]
        installment1 = payment.cart.get_installments_course()[1]
        installment2 = payment.cart.get_installments_course()[2]
        data = {
            'payment': payment, 
            'total': total, 
            'prepayment': prepayment, 
            'pay': pay, 
            'installment1': installment1, 
            'installment2': installment2,
            }
        if 'state' in request.GET.keys():
            data['state'] = request.GET['state']
        return render(request, 'landing/register.html', context = data)
    
    @method_decorator(ratelimit(key='header:x-cluster-client-ip', rate='20/d', block=True, method='POST'))
    def post(self, request, slug):
        payment = get_object_or_404(Payment, slug = slug)
        # validate token
        if 'token' not in request.POST.keys():
            return HttpResponseBadRequest("tokens needed to verify")
        token = en_ar_to_persian(request.POST['token'])
        if not payment.verification.validate(token):
            return HttpResponseForbidden("tokens are not valid or they expired")
        # change total payment
        payment.total = payment.cart.get_prepayment_course()
        payment.save()
        # check total
        if payment.check_total() == False:
            return HttpResponseServerError("less than mimimum payment amount")
        # make url comeback
        CallbackURL = "https://" + request.META['HTTP_HOST'] + reverse('common_landing_course_payment_verification')
        # make authority code for redirecting to API
        try:
            zarinpal_authority = payment.get_zarinpal_authority(CallbackURL) 
        except:
            return HttpResponseServerError("zarinpall api error")
        if zarinpal_authority[0]:
            url = 'https://www.zarinpal.com/pg/StartPay/' + zarinpal_authority[1]
            return HttpResponse({url: url})
        else:
            return HttpResponseServerError("zarinpall api error: " + zarinpal_authority[1])

    @method_decorator(ratelimit(key='header:x-cluster-client-ip', rate='20/d', block=True, method='PATCH'))
    def patch(self, request, slug):
        payment = get_object_or_404(Payment, slug = slug)
        json_req = loads(request.body.decode("utf-8"))
        if len(json_req['discount_code']) > 0:
            discount_code = en_ar_to_persian(json_req['discount_code'])
            discount = get_object_or_404(DiscountCode, code = discount_code)
            payment.cart.discount_code = discount
            payment.save()
            return JsonResponse(
                {}, status=201)
        else:
            payment.cart.discount_code = None
            payment.save()
            return JsonResponse({}, status=200)
        
    @method_decorator(ratelimit(key='header:x-cluster-client-ip', rate='15/d', block=True, method='PUT'))
    def put(self, request, slug):
        """this is a view to send sms authenticator to phone
        this patch request need verification id"""
        payment = get_object_or_404(Payment, slug = slug)
        verification = get_object_or_404(Verify, id = payment.verification.id)
        if verification.sent.send_date == None and verification.sent.gone == False:
            verification.start()
            status = verification.send()
            if status != 200:
                return HttpResponseServerError("Kavehnegar api does not work properly with error code: " + status)
            else:
                return JsonResponse({}, status = 201)
        else:
            now = timezone.make_aware(
                    datetime.now(), 
                    timezone.get_default_timezone()
                    )
            last_min = now + timedelta(minutes=-1)
            last_ten_min = now + timedelta(minutes=-10)
            if last_min < verification.sent.send_date < now:
                return HttpResponseForbidden(
                    "not allowed to make more than one message every minute"
                )
            #if in last 10 min we had a message we can resend it
            elif last_ten_min < verification.sent.send_date < now:
                    status = verification.send()
                    if status != 200:
                        return HttpResponseServerError("Kavehnegar api does not work properly with error code: " + status)
                    else:
                        return JsonResponse({}, status = 200)
            else:
                verification.start()
                status = verification.send()
                if status != 200:
                    return HttpResponseServerError("Kavehnegar api does not work properly with error code: " + status)
                else:
                    return JsonResponse({}, status = 201)
            
class CommonLandingPaymentVerification(TemplateView):

    def get(self, request):
        if request.GET.get('Status') == 'OK':
            authority = request.GET['Authority']
            payment = get_object_or_404(Payment, authority = authority)
            try:
                res = payment.verification_zarinpal() 
            except:
                return HttpResponseServerError("Zarinpal api does not work properly")
            if res[0] == True :
                data = {'status': "OK", 'payment': payment, 'error_code': None}
                return render(request, 'landing/receipt.html', data)
            else:
                data = {'status': "ERROR", 'payment': payment, 'error_code': res[1]}
                return render(request, 'landing/receipt.html', data)
        else:
            authority = request.GET['Authority']
            payment = get_object_or_404(Payment, authority = authority)
            data = {'status': "NOK", 'payment': payment, 'error_code': None}
            return render(request, 'landing/receipt.html', data)
