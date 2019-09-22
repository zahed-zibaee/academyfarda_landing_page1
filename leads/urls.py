from django.conf.urls import url
from django.contrib.auth.views import login
import views


urlpatterns = [
    url(r'^submit/leads/?$', views.submit_Leads, name='submit_Leads'),
    url(r'^query/?$', views.query_Leads, name='query_Leads'),
    url(r'^analysis/?$', views.analysis, name='analysis'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),

]
