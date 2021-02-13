# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from datetime import timedelta, datetime
from django.utils import timezone
from persiantools.jdatetime import JalaliDateTime
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_unicode

from SMS.models import Verify, Sent
from .prices import PREPAYMENT_COMMON_COURSE_PRICE, COMMON_COURSE_PRICE,\
    COMMON_COURSE_DISCOUNTED_PRICE ,DISCOUNT_ON_CASH_PAYMENT_AMOUNT,\
    DISCOUNT_OPERATORS_AMOUNT
    
User = get_user_model()
#TODO: relate name for all
#TODO: timezone awareness
class Product(models.Model):
    """what we want to sell
    its abstract so u need to make a class for every product type
    """
    name = models.CharField(max_length = 100, blank = False)
    description = models.TextField(blank = True)
    prepayment = models.BigIntegerField(null = False, blank = False, default = 0)
    price = models.BigIntegerField(null = False, blank = False, default = 0)
    stock = models.IntegerField(default = 0)
    active = models.BooleanField(default = True)
    order = models.IntegerField(default = 100)
    created_date = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User)

    class meta:
        abstract = True

    def have_stock(self):
        """stock check"""
        if self.stock > 0:
            return True
        elif self.stock == 0:
            return False
        elif self.stock == -1:
            return True
        else:
            raise Exception("stock can not be less than zero")
    
    def sell(self):
        """stock -1"""
        if self.have_stock() and self.stock != -1:
            self.stock -= 1
            self.save()

    def is_active(self):
        """check for is it able to be sold"""
        if self.active is True and self.have_stock():
            return True
        else:
            return False
    
    def get_prepayment_total(self):
        if self.is_active() and self.have_stock():
            return self.prepayment
        else:
            return 0

    def get_total(self):
        if self.is_active() and self.have_stock():
            return self.price
        else:
            return 0

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name),
            encoding = 'utf-8',
        )

    def __str__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name),
            encoding = 'utf-8',
        )


class Discount(models.Model):
    """discount for bunch of products"""
    name = models.CharField(max_length =100, null = False, blank = False)
    code = models.CharField(max_length =50, null = False, blank = False, unique= True)
    product = models.ManyToManyField(Product, blank = False)
    amount = models.BigIntegerField(null = False, blank = False, default =DISCOUNT_OPERATORS_AMOUNT)
    expiration_date = models.DateTimeField(
        null = False, 
        blank = False, 
        default = (timezone.make_aware(datetime.now(), timezone.get_default_timezone()) + timedelta(days=+3650)).date()
    )
    active = models.BooleanField(default = False)
    
    def product_is_active(self ,product_id):
        """check if discount and produuct is active and not discount expired"""
        if self.expiration_date.replace(tzinfo = None) > \
            timezone.make_aware(
                datetime.now(), 
                timezone.get_default_timezone()
                ).date().replace(tzinfo = None) and \
            self.active is True:
            try:
                if self.product.get(id =product_id).active is True:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def get_prepayment_total(self, product_id):
        """get total amount for this product with this discount"""
        try:
            product = self.product.get(id = product_id)
        except ValueError:
            raise ValueError("product by id " + product_id + "can not find")
        if self.is_active(product_id) and product in self.product.all():
            return product.prepayment - self.amount
        else:
            return 0

    def get_total(self, product_id):
        """get total amount for this product with this discount"""
        try:
            product = self.product.get(id = product_id)
        except ValueError:
            raise ValueError("product by id " + product_id + "can not find")
        if self.is_active(product_id) and product in self.product.all():
            return product.price - self.amount
        else:
            return 0

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, name: {}, code: {}"\
            .format(self.id, self.name, self.code),
            encoding = 'utf-8',
        )

    def __str__(self):
        return smart_unicode(
            "ID: {}, name: {}, code: {}"\
            .format(self.id, self.name, self.code),
            encoding = 'utf-8',
        )


class PersonalInformation(models.Model):
    """this method will generate personal information for buyers and teachers"""
    name = models.CharField(max_length = 50, blank = False, null = False)
    family= models.CharField(max_length = 50, blank = False, null = False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length =1, choices =GENDER_CHOICES, default ="M")
    father_name = models.CharField(max_length =50, blank = True)
    meli_regex = RegexValidator(
        regex = r'^\d{10}$',
        message="Meli code must be entered in the format: 'XXXXXXXXXX'. only 10 digits allowed."
    )
    code_meli = models.CharField(
        validators=[meli_regex],
        max_length = 10, 
        blank = False,
        null = False,
    )
    shenasname_regex = RegexValidator(
        regex = r'^\d+$',
        message = "Shenasname code must be entered in the format: 'XXXXXXXXXX'. 1 to 14 digits allowed."
    )
    code_shenasname = models.CharField(
        validators=[meli_regex], 
        max_length = 14, 
        blank = True,
    )
    phone_regex = RegexValidator(
        regex = r'^09\d{9}$',
        message = "Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digit digits allowed."
    )
    phone_number = models.CharField(
        validators = [phone_regex],
        max_length = 11, 
        null = False, 
        blank = False
    )
    phone_number2 = models.CharField(max_length = 15, blank = True)
    phone_number3 = models.CharField(max_length = 15, blank = True)
    origin_town = models.CharField(max_length = 200, blank = True)
    birthday = models.DateField(blank = True)
    address = models.TextField(max_length = 1000, blank = True)
    avetar = models.URLField(max_length = 200, blank = True)
    photo = models.URLField(max_length = 200, blank = True)
    photo_shenasname = models.URLField(max_length = 200, blank = True)
    photo_meli = models.URLField(max_length = 200, blank = True)
    created_date = models.DateTimeField(auto_now_add = True) 

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, name: {}, phone: {}"\
            .format(
            self.id, 
            self.name + " " + self.family, 
            self.phone_number
            ),
            encoding = 'utf-8',
        )

    def __str__(self):
        return smart_unicode(
            "ID: {}, name: {}, phone: {}"\
            .format(
            self.id, 
            self.name + " " + self.family, 
            self.phone_number
            ),
            encoding = 'utf-8',
        )
    

class Teacher(models.Model):
    personal_info = models.ForeignKey(
        PersonalInformation,
        related_name = 'teacher_personal_information',
        blank = False,
        null = False,
        on_delete = models.PROTECT,
    )
            
    def __str__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(
            self.id,
            self.personal_info.name + " " + self.personal_info.family,
            ), 
            encoding = 'utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(
            self.id,
            self.personal_info.name + " " + self.personal_info.family,
            ), 
            encoding = 'utf-8',
        )


class Student(models.Model):
    personal_info = models.ForeignKey(
        PersonalInformation,
        related_name = 'student_personal_information',
        blank = False,
        null = False,
        on_delete = models.PROTECT,
    )
    phone_number_validate = models.BooleanField(default = False)
            
    def __str__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(
            self.id,
            self.personal_info.name + " " + self.personal_info.family,
            ), 
            encoding = 'utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(
            self.id,
            self.personal_info.name + " " + self.personal_info.family,
            ), 
            encoding = 'utf-8',
        )

class CourseType(models.Model):
    name = models.CharField(max_length = 20, blank = False, null = False)
    intensive = models.BooleanField(default = False)
    duration = models.IntegerField(default = 78)
    duration_text = models.CharField(max_length = 20, blank = False, null = False)

    def __str__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name), 
            encoding = 'utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name), 
            encoding = 'utf-8',
        )


class CourseTime(models.Model):
    name = models.CharField(max_length = 20, blank = False, null = False)
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name), 
            encoding = 'utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name), 
            encoding = 'utf-8',
        )


class CourseDay(models.Model):
    name = models.CharField(max_length = 20, blank = False, null = False)
    shanbe = models.BooleanField(default = False)
    yek_shanbe = models.BooleanField(default = False)
    do_shanbe = models.BooleanField(default = False)
    se_shanbe = models.BooleanField(default = False)
    chahar_shanbe = models.BooleanField(default = False)
    panj_shanbe = models.BooleanField(default = False)
    jome = models.BooleanField(default = False)

    def __str__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name), 
            encoding = 'utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name), 
            encoding = 'utf-8',
        )


class Course(Product):
    """this method will manage courses witch can be bought from online shop"""
    alter_name = models.CharField(max_length = 100, blank = False)
    course_type = models.ForeignKey(
        CourseType,
        related_name = 'course_type', 
        null = False, 
        blank = False,
        on_delete = models.PROTECT,
        )
    time = models.ForeignKey(
        CourseTime, 
        related_name = 'course_time', 
        null = False, 
        blank = False,
        on_delete = models.PROTECT,
        )
    days = models.ForeignKey(
        CourseDay, 
        related_name = 'course_day', 
        null = False, 
        blank = False,
        on_delete = models.PROTECT,
        )
    LOCATION_CHOICES = (
        ('V', 'Valiasr'),
        ('E', 'Enghelab'),
        )
    location = models.CharField(
        max_length = 1, 
        choices = LOCATION_CHOICES, 
        null = False, 
        blank = False,
        )
    teacher = models.ForeignKey(
        Teacher, 
        related_name = 'course_teacher', 
        null = True, 
        blank = True,
        on_delete = models.PROTECT,
        )
    students = models.ManyToManyField(Student, blank = True)
    price_showoff = models.BigIntegerField(null = False, blank = False, default = COMMON_COURSE_PRICE)
    discount_cash_payment_amount = models.BigIntegerField(
        null = False, 
        blank = False, 
        default = DISCOUNT_ON_CASH_PAYMENT_AMOUNT
        )
    site_show = models.BooleanField(default = True)
    site_show_special_discount = models.BooleanField(default = False)
    start_date = models.DateField(blank = True)
    finished = models.BooleanField(default = False)
    
    def start(self):
        self.active = False
        self.save()

    def unstart(self):
        self.active = True
        self.save()

    def finish(self):
        self.finished = True
        self.active = False
        self.save()
    
    def unfinish(self):
        self.finished = False
        self.active = True
        self.save()

    def week_to_start(self):
        today = timezone.make_aware(datetime.now(), timezone.get_default_timezone()).date()
        return (self.start_date - today).days // 7

    def __str__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name), 
            encoding = 'utf-8',
        )

    def __unicode__(self):
        return smart_unicode(
            "ID: {}, name: {}".format(self.id, self.name), 
            encoding = 'utf-8',
        )


Course._meta.get_field("price").default = COMMON_COURSE_DISCOUNTED_PRICE
Course._meta.get_field("stock").default = -1
Course._meta.get_field("prepayment").default = PREPAYMENT_COMMON_COURSE_PRICE


class Cart(models.Model):
    """this class will manage carts so every product and its discount need to add to this 
    model and than need to add to total so total can be calculated"""
    Cart_TYPE_CHOICES = (
        ('-1', 'Unknown'),
        ('0', 'Common Course Prepayment'),
        ('1' ,'Common Course Cash'),
        ('2' ,'Common Course Installment 1st'),
        ('3' ,'Common Course Installment 2nd'),
        ('4', 'Book'),
        ('5', 'Exam'),
        ('6', 'Certificate'),
        ('7', 'Exam + Certificate'),
        ('8', 'Exam + Certificate + Book'),
        )
    cart_type = models.CharField(
        max_length = 2, 
        choices = Cart_TYPE_CHOICES, 
        null = False, 
        blank = False,
        default ="0"
        )
    courses = models.ManyToManyField(Course, blank = True)
    discount_codes = models.ManyToManyField(Discount, blank = True)
    installment = models.BooleanField(default = False)
    total = models.BigIntegerField(null = False, blank = False, default = 0)
    prepayment = models.BigIntegerField(null = False, blank = False, default = 0)
    payment = models.BigIntegerField(null = False, blank = False, default = 0)
    first_installment = models.BigIntegerField(null = False, blank = False, default = 0)
    second_installment = models.BigIntegerField(null = False, blank = False, default = 0)

    def set_prepayment_course(self):
        """calculate total amount of prepayment for one course with or without of discount_code in cart"""
        if int(self._type) != 0:
            raise ValueError("this method is only for buy one course")
        course = self.courses.get()
        if len(self.discount_codes.all()) > 1:
            raise ValueError("more than one discount is in the cart")
        elif len(self.discount_codes.all()) == 0:
            if course.get_prepayment_total(course.id) > 10000:
                self.prepayment = course.get_prepayment_total(course.id)
                self.save()
            else:
                raise ValueError("can not calculate total")
        else:
            discount = self.discount_codes.get()
            if discount.get_prepayment_total(course.id) > 10000:
                self.prepayment = discount.get_prepayment_total(course.id)
                self.save()
            else:
                raise ValueError("can not calculate total")

    def set_total_course(self):
        """calculate total amount for one course with or without of discount_code in cart"""
        if 0 < int(self._type) <= 3:
            raise ValueError("this method is only for buy one course")
        res = 0
        course = self.courses.get()
        # add course and discount amount to total
        if len(self.discount_codes.all()) > 1:
            raise ValueError("more than one discount is in the cart")
        elif len(self.discount_codes.all()) == 0:
            if course.get_prepayment_total(course.id) > 10000:
                res += course.get_total(course.id)
            else:
                res += 0
        else:
            discount = self.discount_codes.get()
            if discount.get_total(course.id) > 10000:
                res += discount.get_total(course.id)
            else:
                res += 0
        # check for discount cash
        if res != 0 and self.installment is True:
            res -= course.discount_cash_payment_amount
        # check if amount not 0 retrun total amount or make an error
        if res == 0:
            raise ValueError("can not calculate total")
        else:
            self.total = res
            self.save()

    def set_installments_course(self):
        """calculate installments amount for one course with or without of discount_code in cart
        its first installment and second installment"""
        pass

    def set_payments(self):
        """automagically set total, prepayment, first_installment, second_installment"""
        pass

    def get_payment_amount(self):
        """after calculate the amount of payment this method retrun """
        if int(self._type) == -1:
            raise ValueError("Unknown cart type")
        elif int(self._type) == 0:
            if self.prepayment == 0:
                raise ValueError("payment amount not calculated prepayment")
            return self.prepayment
        elif int(self._type) == 1:
            if self.first_installment == 0:
                raise ValueError("payment amount not calculated installment")
            return self.first_installment
        elif int(self._type) == 2:
            if self.first_installment == 0:
                raise ValueError("payment amount not calculated first installment")
            return self.first_installment
        elif int(self._type) == 3:
            if self.second_installment == 0:
                raise ValueError("payment amount not calculated second installment")
            return self.second_installment
        elif int(self._type) > 3:
            if self.total == 0:
                raise ValueError("payment amount not calculated payment total")
            return self.total

    def get_courses(self):
        try:
            return smart_unicode(
                ", ".join([str(obj.id) for obj in self.courses.all()]),
                encoding = 'utf-8',
                )
        except:
            return None

    def get_discount_codes(self):
        try:
            return smart_unicode(
                ", ".join([str(obj.id) for obj in self.discount_codes.all()]),
                encoding = 'utf-8',
                )
        except:
            return None
    
    def __unicode__(self):
       return smart_unicode(
            "ID: {}, course ids: {}, course with discount ids: {}".format(
                self.id, 
                self.get_courses(), 
                self.get_discount_codes()
            ), 
            encoding = 'utf-8',
        )

    def __str__(self):
        return smart_unicode(
            "ID: {}, course ids: {}, course with discount ids: {}".format(
                self.id, 
                self.get_courses(), 
                self.get_discount_codes()
            ), 
            encoding = 'utf-8',
        )

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('O', 'Online'),
        ('P', 'POS'),
        ('C', 'Cash'),
        ('T', 'Transfer'),
        )
    payment_type = models.CharField(
        max_length = 1, 
        choices = PAYMENT_TYPE_CHOICES, 
        null = False, 
        blank = False,
        default = "O"
        )
    cart = models.ForeignKey(
        Cart, 
        related_name = 'cart', 
        null = False,
        blank = False,
        on_delete = models.PROTECT,
    )
    verification = models.ForeignKey(
        Verify, 
        on_delete = models.SET_NULL, 
        null = True,
    )
    student = models.ForeignKey(
        Student, 
        related_name = 'payment_student_personal_info',
        null = False, 
        blank = False, 
        on_delete = models.PROTECT,
    )
    operator = models.ForeignKey(
        User, 
        related_name = 'payment_operator',
        null = True, 
        blank = True, 
        on_delete = models.SET_NULL
    )
    total = models.BigIntegerField(null = False, blank = False)
    authority = models.CharField(max_length =100, null = False, blank = False)
    created_date = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(
        User, 
        related_name = 'payment_created_by', 
        null = True, 
        blank = True
        )
    status = models.BooleanField(default = False)
    ref_id = models.CharField(max_length =20, blank = True)
    send_receipt = models.BooleanField(default = False) 

    def check_total(self):
        """check if total if not less than payment api low limit"""
        if self.total <= 10000:
            return True
        else:
            return False

    def send_receipt_course(self):
        sms = Sent.objects.create(
            receptor = self.student.personal_info.phone_number,
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
        try:
            res +=  ", name: {}".format(
            self.student.personal_info.name + " " + self.student.personal_info.family
            )
        except:
            pass
        if self.cart:
            if len(self.cart.get_discount_codes()) > 0:
                res +=  ", cart: {}".format(self.cart.get_discount_codes())
            elif len(self.cart.get_courses()) > 0:
                res +=  ", cart: {}".format(self.cart.get_courses())
            else:
                res +=  ", cart id: {}".format(self.cart.id)
        res += ", status: {}".format(self.status)
        return smart_unicode(res)
        
    def __str__(self):
        res = "ID: {}".format(self.id)
        try:
            res +=  ", name: {}".format(
            self.student.personal_info.name + " " + self.student.personal_info.family
            )
        except:
            pass
        if self.cart:
            if len(self.cart.get_discount_codes()) > 0:
                res +=  ", cart: {}".format(self.cart.get_discount_codes())
            elif len(self.cart.get_courses()) > 0:
                res +=  ", cart: {}".format(self.cart.get_courses())
            else:
                res +=  ", cart id: {}".format(self.cart.id)
        res += ", status: {}".format(self.status)
        return smart_unicode(res)