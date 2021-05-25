# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from contacts.models import Contact

from django.db import models
from django.core.validators import RegexValidator
from django.db.models.fields.related import ForeignKey
from persiantools.jdatetime import JalaliDateTime
from django.utils.html import format_html

from users.models import User
from common.models import Label, TimeStampMixin, Comment
from contacts.models import Contact

class Origin(TimeStampMixin):
    title = models.CharField(max_length=100, null=False, blank=False)
    token = models.CharField(max_length=64, null=True, blank=True)
    token_activation = models.BooleanField(default=False)

    def __unicode__(self):
        return "{}".format(self.title)


class Lead(TimeStampMixin):
    #TODO: chane to a better lead by django CRM 
    origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, unique=False, null=True, editable=False,)
    name_and_family = models.CharField(max_length=100, null=False, blank=False)
    contact = ForeignKey(Contact, blank=False, null=False)
    REGISTRATION_STATUS_CHOICES = (
        ('K', 'OK'),
        ('C', 'Cancel'),
        ('U', 'Unknown'),
    )
    register_status = models.CharField(max_length=1, choices=REGISTRATION_STATUS_CHOICES, default='U')
    question = models.TextField(blank=True)
    operator = models.ManyToManyField(User, related_name='lead_operator', unique=False, editable=False)
    registered_by = models.ForeignKey(User, related_name='lead_registered_by',unique=False, null=True, editable=False)
    comments = models.ManyToManyField(Comment, blank=True)
    label = models.ManyToManyField(Label, blank=True)

    def __unicode__(self):
        return "{} ----- {}".format(self.phone_number, self.name_and_family)
       