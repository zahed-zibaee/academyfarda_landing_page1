# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Teacher)
admin.site.register(PaymentInformation)
admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(Discount)
admin.site.register(Course)