from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^send/$', views.send, name='send'),
    url(r'^OTP/$', views.OTP, name='OTP'),
    url(r'^status/$', views.status, name='status'),
]