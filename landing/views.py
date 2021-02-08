# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from persiantools import digits
from re import compile as re_compile
from django.http import HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import get_user_model

#change theese to app name ...
from SMS.models import Verify, Sent
from payments.models import Course, Payment, Cart, PersonalInformation, Student

User = get_user_model()

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
        courses = Course.objects.filter(active=True, site_show=True).order_by("site_order")
        # pass courses to show in landing and operator for tracking for registration
        data = {"courses": courses, "operator_username": operator}
        return render(request, 'landing/index.html', context = data)

    def post(self, request):
        """register by this"""
        #normalize data
        request.POST = request.POST.copy()
        request.POST["code_meli"] = normalize(request.POST["code_meli"])
        request.POST["phone"] = normalize(request.POST["phone"])
        pattern = re_compile("^\+989\d{9}$")
        if pattern.match(request.POST["phone"]) == True:
            request.POST["phone"] = "0" + request.POST["phone"][3:]
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
        if not pattern.match(request.POST["code_meli"]):
            return HttpResponseBadRequest("bad data code_meli")
        pattern = re_compile("^09\d{9}$|^\+989\d{9}$")
        if not pattern.match(request.POST["phone"]):
            return HttpResponseBadRequest("bad data phone")
        if not 10 <= len(request.POST["address"]) <= 1000:
            return HttpResponseBadRequest("bad data address")
        try:
            course = Course.objects.get(id = int(request.POST["course"]))
            if not course.is_active():
                HttpResponseBadRequest("course is not active")
        except:
            return HttpResponseNotFound("course not found")
        if not (request.POST["discount_cash"] == "0" or request.POST["discount_cash"] == "1"):
            return HttpResponseBadRequest("bad data payment_type")
        else:
            if request.POST["discount_cash"] == "1":
                discount_cash = True
            else:
                discount_cash = False
        # make payment object for tracking lead
        payment = Payment.objects.create(
            cart = Cart.objects.create(
                _type = "0",
                discount_cash = discount_cash,
            ), 
            # only make a verification object for later
            verification = Verify.objects.create(
                sent = Sent.objects.create(
                    receptor = request.POST["phone"],
                )
            ), 
            # save personal info for get lead if register not complete
            student = Student.objects.create(
                PersonalInformation.objects.create(
                name = request.POST["name"],
                family = request.POST["family"],
                gender = request.POST["gender"],
                father_name = request.POST["father_name"],
                code_meli = request.POST["code_meli"],
                phone_number = request.POST["phone"],
                address = request.POST["address"],
                    ), 
                ),
            # this total is for only course registration price not discount included
        )
        # add course to cart
        # if discount added we need to remove this from cart
        payment.cart.courses.add(course)
        try:
            # try to track operator
            operator = User.objects.get(username = request.POST["operator_username"])
            payment.operator = operator
        except:
            pass
        payment.save()
        # go to verify/id page to verify payment by user
        return HttpResponseRedirect("/landing/common/verify/" + str(payment.id))

class CommonVerify(TemplateView):
    #TODO: add methode to check for discounts
    #change template page to show properly
    #on post make verification happend and if its success redirect to bank
    #on post check for discount if we had a valid one we need to change payment.cart and payment.total accordingly
    #after payment we need to show and send receipt

    def get(self, request, verify_id):
        try:
            payment = Payment.objects.get(id = verify_id)
        except:
            return HttpResponseNotFound("payment not found")
        data = {'payment': payment,}
        return render(request, 'landing/verify.html', context = data)
    
    def post(self, request):
        pass