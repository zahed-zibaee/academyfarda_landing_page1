# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Score(models.Model):
    name = models.CharField(max_length=100, null=False)
    family = models.CharField(max_length=100, null=False)
    id_card = forms.RegexField(regex=r'^[\d-]+$', required=True, max_length=50, null=False)
    score_t1 = models.FloatField(default=-1)
    score_t2 = models.FloatField(default=-1)
    score_a1 = models.FloatField(default=-1)
    score_a2 = models.FloatField(default=-1)
    code_govahi = models.BigIntegerField(default=-1)
    confirmation = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name + " " + self.family + " ========== " + self.id_card 