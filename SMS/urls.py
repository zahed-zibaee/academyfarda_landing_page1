from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lookup/?$', views.lookup, name='lookup'),
]