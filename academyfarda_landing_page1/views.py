

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def error_404(request):
    #TODO: add other errors 
    data = {}
    return render(request,'404/error_404.html', data)