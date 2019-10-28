from django.conf.urls import url
from django.contrib.auth.views import login
from . import views


urlpatterns = [
    #TODO: 1-change submit/leads to leads/saubmit 2-acount/login 3-leads/dashboard or analysis
    url(r'^submit/leads/?$', views.submit_Leads, name='submit_Leads'),
    url(r'^analysis/?$', views.analysis, name='analysis'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),
    url(r'^landing2/?$', views.landing2, name='landing2'),
    url(r'^thanks/?$', views.thanks, name='thanks'),
    url(r'^export/?$', views.export, name='export'),
    url(r'^export_comment_save/?$', views.export_comment_save, name='export_comment_save'),
    url(r'^export_comment_approved/?$', views.export_comment_approved, name='export_comment_approved'),
]
