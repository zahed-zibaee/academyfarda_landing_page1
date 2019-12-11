from django.conf.urls import url
from . import views


urlpatterns = [
    #TODO: 1-change submit/leads to leads/saubmit 2-acount/login 3-leads/dashboard or analysis
    url(r'^api/submitnew/?$', views.api_submit, name='api_submit'),
    url(r'^export/?$', views.export, name='export'),
    url(r'^export/all/?$', views.export_all, name='export_all'),
    url(r'^comment_add/?$', views.comment_add, name='comment_add'),
    url(r'^comment_edit/?$', views.comment_edit, name='comment_edit'),
    url(r'^comment_del/?$', views.comment_del, name='comment_del'),
    url(r'^comment_approve/?$', views.comment_approve, name='comment_approve'),
    url(r'^lead_add/?$', views.lead_add, name='lead_add'),
    url(r'^lead_del_and_edit/?$', views.lead_del_and_edit, name='lead_del_and_edit'),
    url(r'^question_edit/?$', views.question_edit, name='question_edit'),
    url(r'^label_add_and_del/?$', views.question_edit, name='label_add_and_del'),
]
