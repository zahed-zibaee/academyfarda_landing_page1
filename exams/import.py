# -*- coding: utf-8 -*-

import csv
from exams.models import Score


with open(r"C:\Users\ZIZI\Desktop\python27\academyfarda_crm2\exams\score.csv", newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[8] == "تایید":
            confirmation=True
        else:
            confirmation=False
        Score.objects.create(name=row[0],family=row[1],id_card=row[2],score_t1=float(row[3]),score_t2=float(row[4]),score_a1=float(row[5]),score_a2=float(row[6]),code_govahi=int(row[7]),confirmation=confirmation)


for obj in Score.objects.all():
    if len(obj.id_card) > 10:
        id_card = obj.id_card
        string=""
        for i in range(10-len(obj.id_card)):
            string += "0"
        obj.id_card = string + id_card
        obj.save()