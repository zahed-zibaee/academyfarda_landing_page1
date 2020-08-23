# Github.com/Rasooll
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cartcoursecreate/?$', views.cart_course_create, name='cartcoursecreate'),
    url(r'^verify/?$', views.verify , name='verify'),
    url(r'^checkdiscountcourse/?$', views.check_discount_course , name='checkdiscountcourse'),
    url(r'^checkcourse/?$', views.check_course , name='checkcourse'),
]
