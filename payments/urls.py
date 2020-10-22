# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cartcoursecreate/?$', views.cart_course_create, name='cartcoursecreate'),
    url(r'^verify/?$', views.verify , name='verify'),
    url(r'^getcoursetotal/?$', views.get_course_total , name='getcoursetotal'),
    url(r'^checkcourse/?$', views.check_course , name='checkcourse'),
    url(r'^getcourses/?$', views.get_courses , name='getcourses'),
]
