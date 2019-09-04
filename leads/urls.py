from django.conf.urls import url
import views

urlpatterns = [
    url(r'^submit/leads/?$', views.submit_Leads, name='submit_Leads'),
    url(r'^query/?$', views.query_Leads, name='query_Leads'),
    url(r'^analysis/?$', views.analysis, name='analysis'),
]
