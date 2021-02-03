# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime, timedelta, date
from django.utils import encoding
from persiantools.jdatetime import JalaliDateTime
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode
from zeep import Client

from SMS.models import Verify, Sent
from .config import PREPAYMENT_COMMON_COURSE, PAYMENT_COMMON_COURSE,\
    PAYMENT_COMMON_COURSE_DISCOUNTED ,DISCOUNT_ON_CASH_PAYMENT,\
    OPERATOR_DISCOUNT
    
#TODO: relate name for all
#TODO: timezone awareness
class Product(models.Model):
    """what we want to sell
    its abstract so u need to make a class for every product type
    """
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    price = models.BigIntegerField(null=False, blank=False, default=PAYMENT_COMMON_COURSE_DISCOUNTED)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    class meta:
        abstract = True

    def have_stock(self):
        """stock check"""
        if self.stock > 0:
            return True
        elif self.stock == 0:
            return False
        else:
            raise Exception("stock can not be less than zero")
    
    def sell(self):
        """stock -1"""
        self.stock -= 1

    def is_active(self):
        """check for is it able to be sold"""
        if self.active == True:
            return True
        else:
            return False
    
    def get_total(self):
        if self.is_active():
            return self.price
        else:
            return False

    def __unicode__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name),
            encoding='utf-8',
        )

    def __str__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name),
            encoding='utf-8',
        )


class Discount(models.Model):
    """discount for bunch of products"""
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=50, null=False, blank=False, unique=True)
    product = models.ManyToManyField(Product, blank=False)
    amount = models.BigIntegerField(null=False, blank=False, default=OPERATOR_DISCOUNT)
    expiration_time = models.DateTimeField(
        null=False, 
        blank=False, 
        default=datetime.now() + timedelta(days=+36500)
    )
    active = models.BooleanField(default=False)
    
    def is_active(self ,product_id):
        """check if discount and produuct is active and not discount expired"""
        if self.expiration_time.replace(tzinfo=None) > datetime.now()\
            and self.active == True:
            try:
                if self.product.get(id=product_id).active == True:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def get_total(self, product_id):
        """get total amount for this product with this discount"""
        try:
            product = self.product.get(id=product_id)
        except:
            return False
        if self.is_active(product_id) and product in self.product.all():
            return product.price - self.amount
        else:
            return False

    def __unicode__(self):
        return smart_unicode(
            "ID: {} - name: {} - code: {}"\
            .format(self.id, self.name, self.code),
            encoding='utf-8',
        )

    def __str__(self):
        return smart_unicode(
            "ID: {} - name: {} - code: {}"\
            .format(self.id, self.name, self.code),
            encoding='utf-8',
        )


class PersonalInformation(models.Model):
    """this method will generate personal information for buyers and teachers"""
    name = models.CharField(max_length=50, blank=False, null=False)
    family= models.CharField(max_length=50, blank=False, null=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    father_name = models.CharField(max_length=50, blank=True)
    meli_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Meli code must be entered in the format: 'XXXXXXXXXX'. only 10 digits allowed."
    )
    code_meli = models.CharField(
        validators=[meli_regex],
        max_length=10, 
        blank=False,
        null=False,
    )
    shenasname_regex = RegexValidator(
        regex=r'^\d+$',
        message="Shenasname code must be entered in the format: 'XXXXXXXXXX'. 1 to 14 digits allowed."
    )
    code_shenasname = models.CharField(
        validators=[meli_regex], 
        max_length=14, 
        blank=True,
    )
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message="Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digit digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=11, 
        null=False, 
        blank=False
    )
    phone_number2 = models.CharField(max_length=15, blank=True)
    phone_number3 = models.CharField(max_length=15, blank=True)
    origin_town = models.CharField(max_length=200, blank=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.TextField(max_length=1000, blank=True)
    photo = models.URLField(max_length=200, blank=True)
    photo_shenasname = models.URLField(max_length=200, blank=True)
    photo_meli = models.URLField(max_length=200, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return smart_unicode(
            "ID: {} - name: {} - phone: {}"\
            .format(
            self.id, 
            self.name + " " + self.family, 
            self.phone_number
            ),
            encoding='utf-8',
        )

    def __str__(self):
        return smart_unicode(
            "ID: {} - name: {} - phone: {}"\
            .format(
            self.id, 
            self.name + " " + self.family, 
            self.phone_number
            ),
            encoding='utf-8',
        )
    

class CourseTeacher(models.Model):
    personal_info = models.ForeignKey(
        PersonalInformation,
        related_name='course_teacher_personal_information',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
            
    def __str__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(
            self.id,
            self.personal_info.name + " " + self.personal_info.family,
            ), 
            encoding='utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(
            self.id,
            self.personal_info.name + " " + self.personal_info.family,
            ), 
            encoding='utf-8',
        )


class CourseType(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    intensive = models.BooleanField(default=False)
    duration = models.CharField(max_length=20, blank=False, null=False)
    duration_hours = models.IntegerField(default=78)

    def __str__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name), 
            encoding='utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name), 
            encoding='utf-8',
        )


class CourseTime(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name), 
            encoding='utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name), 
            encoding='utf-8',
        )


class CourseDay(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    shanbe = models.BooleanField(default=False)
    yek_shanbe = models.BooleanField(default=False)
    do_shanbe = models.BooleanField(default=False)
    se_shanbe = models.BooleanField(default=False)
    chahar_shanbe = models.BooleanField(default=False)
    panj_shanbe = models.BooleanField(default=False)
    jome = models.BooleanField(default=False)

    def __str__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name), 
            encoding='utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name), 
            encoding='utf-8',
        )


class Course(Product):
    """this method will manage courses witch can be bought from online shop"""
    alter_name = models.CharField(max_length=100, blank=True)
    course_type = models.ForeignKey(
        CourseType,
        related_name='course_type', 
        null=False, 
        blank=False,
    )
    course_time = models.ForeignKey(
        CourseTime, 
        related_name='course_time', 
        null=False, 
        blank=False,
    )
    course_day = models.ForeignKey(
        CourseDay, 
        related_name='course_day', 
        null=False, 
        blank=False
    )
    LOCATION_CHOICES = (
        ('V', 'Valiasr'),
        ('E', 'Enghelab'),
    )
    location = models.CharField(
        max_length=1, 
        choices=LOCATION_CHOICES, 
        null=False, 
        blank=False,
    )
    teacher = models.ForeignKey(
        CourseTeacher, 
        related_name='course_teacher', 
        null=True, 
        blank=True
    )
    prepayment = models.BigIntegerField(null=False, blank=False, default=PREPAYMENT_COMMON_COURSE)
    price_showoff = models.BigIntegerField(null=False, blank=False, default=PAYMENT_COMMON_COURSE)
    discount_cash_payment = models.BigIntegerField(null=False, blank=False, default=DISCOUNT_ON_CASH_PAYMENT)
    site_show_special_discount = models.BooleanField(default=False)
    site_show = models.BooleanField(default=True)
    
    def week_to_start(self):
        today = date.today()
        return (self.start - today).days // 7

    def __str__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name), 
            encoding='utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {} - name: {}".format(self.id, self.name), 
            encoding='utf-8',
        )


class Cart(models.Model):
    """this class will manage carts so every product and its discount need to add to this 
    model and than need to add to total so total can be calculated"""
    courses = models.ManyToManyField(Course, blank=True)
    discounts = models.ManyToManyField(Discount, blank=True)
    
    def get_total_course(self):
        """calculate total amount for one course with or without of discount in cart"""
        try:
            course = self.courses.get()
        except ValueError:
            raise ValueError("more than one course is in the cart")
        if len(self.discounts.all()) > 1:
            raise ValueError("more than one discount is in the cart")
        elif len(self.discounts.all()) < 1:
            return course.get_total(course.id)
        else:
            discount = self.discounts.get()
            return discount.get_total(course.id)

    def get_courses(self):
        try:
            return smart_unicode(
                ", ".join([str(obj.id) for obj in self.courses.all()]),
                encoding='utf-8',
                )
        except:
            return None

    def get_discounts(self):
        try:
            return smart_unicode(
                ", ".join([str(obj.id) for obj in self.discounts.all()]),
                encoding='utf-8',
                )
        except:
            return None
    
    def __unicode__(self):
       return smart_unicode(
            "ID: {} - course ids: {} - course with discount ids: {}".format(
                self.id, 
                self.get_courses(), 
                self.get_discounts()
            ), 
            encoding='utf-8',
        )

    def __str__(self):
        return smart_unicode(
            "ID: {} - course ids: {} - course with discount ids: {}".format(
                self.id, 
                self.get_courses(), 
                self.get_discounts()
            ), 
            encoding='utf-8',
        )

class Payment(models.Model):
    cart = models.ForeignKey(
        Cart, 
        related_name='cart', 
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    verification = models.ForeignKey(
        Verify, 
        on_delete=models.SET_NULL, 
        null=True,
    )
    personal_info = models.ForeignKey(
        PersonalInformation, 
        related_name='buyer_personal_info',
        null=False, 
        blank=False, 
        on_delete=models.PROTECT,
    )
    operator = models.ForeignKey(
        User, 
        related_name='register_operator',
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    total = models.BigIntegerField(null=False, blank=False)
    authority = models.CharField(max_length=100, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    ref_id = models.CharField(max_length=20, blank=True)
    send_receipt = models.BooleanField(default=False) 
    PAYMENT_TYPE_CHOICES = (
        ('0', 'نقدی'),
        ('1', 'اقساط'),
    )
    payment_type = models.CharField(
        max_length=1, 
        choices=PAYMENT_TYPE_CHOICES,
        null=False, 
        blank=False,
        default="0"
    )

    def check_total(self):
        """check if total if not less than payment api low limit"""
        if total <= 5000:
            return True
        else:
            return False

    def get_jalali_date(self):
        return JalaliDateTime(self.created_date).strftime("%Y/%m/%d")

    def get_tehran_time(self):
        return self.created_date.strftime("%H:%M:%S")

    def send_receipt_course(self):
        sms = Sent.objects.create(
            receptor = self.personal_info.phone_number,
            created_date = datetime.now()
        )
        res_code = sms.send_receipt_course(self.ref_id)
        if res_code == 200:
            self.send_receipt = True
            self.save()
            return res_code
        else:
            return res_code

    def __unicode__(self):
        res = "ID: {}".format(self.id)
        if self.personal_info:
            res +=  "- name: {}".format(
            self.personal_info.name + " " + self.personal_info.family
            )
        if self.cart:
            if len(self.cart.get_discounts()) > 0:
                res +=  "- cart: {}".format(self.cart.get_discounts())
            elif len(self.cart.get_courses()) > 0:
                res +=  "- cart: {}".format(self.cart.get_courses())
            else:
                res +=  "- cart id: {}".format(self.cart.id)
        res += "- status: {}".format(self.status)
        return smart_unicode(res)
        
    def __str__(self):
        res = "ID: {}".format(self.id)
        if self.personal_info:
            res +=  "- name: {}".format(
            self.personal_info.name + " " + self.personal_info.family
            )
        if self.cart:
            if len(self.cart.get_discounts()) > 0:
                res +=  "- cart: {}".format(self.cart.get_discounts())
            elif len(self.cart.get_courses()) > 0:
                res +=  "- cart: {}".format(self.cart.get_courses())
            else:
                res +=  "- cart id: {}".format(self.cart.id)
        res += "- status: {}".format(self.status)
        return smart_unicode(res)