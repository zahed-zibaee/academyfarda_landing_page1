"""academyfarda_backend URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from heartbeat.urls import urlpatterns as heartbeat_urls

from . import views


#TODO change from leads import views as leads_views to something dynamic
urlpatterns = [
    url(r'^adminlogin/', admin.site.urls),
    url(r'^heartbeat/?', include(heartbeat_urls)),

    url(r'^/?$', views.landing_redirect , name="landing_redirect"),   
]

urlpatterns += [
    url(r'^leads/', include('leads.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^payments/', include('payments.urls')),
    url(r'^SMS/', include('SMS.urls')),
    url(r'^landing/', include('landing.urls')),
]

handler404 = views.error_404
