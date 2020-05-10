# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import os

from django.db import models

# Create your models here.

class Score(models.Model):
    """ store name, lastname, id, scores, peyments, conformation here """
    name = models.CharField(max_length=100, null=False)
    family = models.CharField(max_length=100, null=False)
    id_card = models.CharField(max_length=100,null=False)
    score_t1 = models.FloatField(default=-1)
    score_a1 = models.FloatField(default=-1)
    score_a2 = models.FloatField(default=-1)
    score_total = models.FloatField(default=-1)
    code_govahi = models.BigIntegerField(default=-1)
    confirmation = models.BooleanField(default=False)


    def __unicode__(self):
        return self.name + " " + self.family + " |==========| " + self.id_card + " |==========| " + self.score_total

def import_exam_csv(file_location="exams/score.csv"):
    """ import csv file to db, the column must be 
        name, last name, id, score exam 1st, score practical exam 1st, score practical exam 2nd, score total, payment code, conformation """
    with open(file_location, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[8] == "تایید":
                confirmation = True
            else:
                confirmation = False
            Score.objects.create(name=row[0], family=row[1], id_card=row[2], score_t1=float(row[3]), score_a1=float(
                row[4]), score_a2=float(row[5]), score_total=float(row[6]), code_govahi=int(row[7]), confirmation=confirmation)
        return 0
            