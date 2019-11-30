# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from leads.models import Origin, User, Lead, Comment, Label




def dashboard(request):
    #TODO add search and filters, make user only see commend they need 2 see, sort commends,padging
    leads = Lead.objects.all()
    comments = Comment.objects.all()
    data = {'comments': comments, 'leads':leads, }
    return render(request,'leads/dashboard/dashboard.html', data)
