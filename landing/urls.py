
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^common/?$', views.CommonLanding.as_view(), name='common_landing'),
    url(r'^common/register/(?P<slug>[0-9a-fA-F]+)/?$', views.CommonLandingRegister.as_view(), name='common_landing_course_registering'),
    url(r'^common/receipt/?$', views.CommonLandingPaymentVerification.as_view(), name='common_landing_course_payment_verification'),
]