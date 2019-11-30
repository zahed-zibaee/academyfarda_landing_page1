from django.conf.urls import url
from . import views


urlpatterns = [
    #TODO: 1-change submit/leads to leads/saubmit 2-acount/login 3-leads/dashboard or analysis
    url(r'^api/submitnew/?$', views.api_submit, name='api_submit'),
    url(r'^export/?$', views.export, name='export'),
    url(r'^comment_add/?$', views.comment_add, name='comment_add'),
    url(r'^lead_add/?$', views.lead_add, name='lead_add'),
    url(r'^lead_del/?$', views.lead_del, name='lead_del'),
]
