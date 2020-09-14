"""academyfarda_landing_page1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404
from django.views.generic import TemplateView
from django.contrib import admin
from . import views


#TODO change from leads import views as leads_views to something dynamic
urlpatterns = [
    url(r'^adminlogin/', admin.site.urls),
    url(r'^leads/', include('leads.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^crm/', include('CRM.urls')),
    url(r'^payments/', include('payments.urls')),
    url(r'^SMS/', include('SMS.urls')),
    url(r'^hi/?$', views.hi, name="hi"),
    url(r'^/?$', views.landing_redirect , name="landing"),
]

handler404 = views.error_404
