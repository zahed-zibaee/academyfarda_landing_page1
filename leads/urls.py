from django.conf.urls import url
from . import views


urlpatterns = [
    #TODO: 1-change submit/leads to leads/saubmit 2-acount/login 3-leads/dashboard or analysis
    url(r'^api/submitnew/?$', views.api_submit, name='api_submit'),
    url(r'^landing/second?$', views.landing2, name='landing2'),
    url(r'^landing/thanks/?$', views.thanks, name='thanks'),
    url(r'^export/?$', views.export, name='export'),
<<<<<<< HEAD
    url(r'^comment_save/?$', views.comment_save, name='comment_save'),
=======
    url(r'^comment_add/?$', views.comment_add, name='comment_add'),
>>>>>>> a622e076fb3bce85104cbed4d4d980f9a60adfbf
    url(r'^lead_add/?$', views.lead_add, name='lead_add'),
    url(r'^lead_del/?$', views.lead_del, name='lead_del'),
]
