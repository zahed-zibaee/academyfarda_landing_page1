
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^common/?$', views.CommonLanding.as_view(), name='common_landing'),
    url(r'^common/verify/(?P<verify_id>\d+)/?$', views.CommonVerify.as_view(), name='common_landing_course_buy_verification'),
]