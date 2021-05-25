from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.encoding import smart_unicode

from common.models import Address, EmailAddress, PhoneNumber, TimeStampMixin
from common.models import User

class Contact(TimeStampMixin):
    CONTACT_TYPE_CHOICES = {
        "-1": "Unknown",
        "0": "Staff",
        "1": "Teacher",
        "2": "Student",
        "3": "Faniherfeii",
        "4": "Third Party",
        "4": "Lead",
    }
    type_ = models.CharField(
        max_length = 2, 
        choices = CONTACT_TYPE_CHOICES, 
        null = False, 
        blank = False,
        default = "-1"
    )
    user = ForeignKey(User, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=False, null=False)
    addresses = models.ManyToManyField(Address, blank=True)
    phone_numbers =  models.ManyToManyField(PhoneNumber, blank=True)
    email_addresses = models.ManyToManyField(EmailAddress, blank=True)
    description = models.TextField(blank=True, null=True)