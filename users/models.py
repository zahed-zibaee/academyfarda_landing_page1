from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_unicode
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Default user for academyfarda_backend."""
    name = models.CharField(max_length=50, blank=False, null=False)
    family= models.CharField(max_length=50, blank=False, null=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    father_name = models.CharField(max_length=50, blank=True)
    meli_regex = RegexValidator(
        regex = r'^\d{10}$',
        message="Meli code must be entered in the format: 'XXXXXXXXXX'. only 10 digits allowed."
    )
    code_meli = models.CharField(
        validators=[meli_regex],
        max_length=10, 
        blank=True,
        null=False,
    )
    shenasname_regex = RegexValidator(
        regex = r'^\d+$',
        message = "Shenasname code must be entered in the format: 'XXXXXXXXXX'. 1 to 14 digits allowed."
    )
    code_shenasname = models.CharField(
        validators=[shenasname_regex], 
        max_length=14, 
        blank=True,
        null=False,
    )
    phone_regex = RegexValidator(
        regex = r'^09\d{9}$',
        message = "Phone number must be entered in the format: '09XXXXXXXXX'. \"09\" than 9 digit digits allowed."
    )
    phone_number = models.CharField(
        validators = [phone_regex],
        max_length=11, 
        null=False, 
        blank=False
    )
    origin_town = models.CharField(max_length=200, blank=True)
    birthday = models.DateField(blank=True)
    avetar = models.URLField(max_length=200, blank=True)
    photo = models.URLField(max_length=200, blank=True)
    photo_shenasname = models.URLField(max_length=200, blank=True)
    photo_meli = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __unicode__(self):
        return smart_unicode(
            "ID:{}, {}"\
            .format(
            self.id,
            self.get_full_name,
            ),
            encoding = 'utf-8',
        )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return smart_unicode(
            "ID:{}, {}"\
            .format(
            self.id,
            self.get_full_name,
            ),
            encoding = 'utf-8',
        )

    @property
    def full_name(self):
       return smart_unicode(
            "{} {}"\
            .format(
            self.name, 
            self.family,
            ),
            encoding = 'utf-8',
        ) 
