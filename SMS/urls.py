from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^send/?$', views.send, name='send'),
    url(r'^lookup/?$', views.lookup, name='lookup'),
    url(r'^status/?$', views.status, name='status'),
]