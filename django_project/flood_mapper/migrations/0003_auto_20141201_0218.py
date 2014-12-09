# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

import csv


def import_rt(apps, schema_editor):
    file = 'flood_mapper/data/List of RT DKI Jakarta - updated 2012.csv'
    RT = apps.get_model("flood_mapper", "RT")
    RW = apps.get_model("flood_mapper", "RW")
    Village = apps.get_model("flood_mapper", "Village")
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            village_name = row[0]
            rw_number = row[1]
            rt_number = row[2]
            village_name_slug = slugify(unicode(village_name))
            try:
                village = Village.objects.get(slug=village_name_slug)
            except:
                continue
            try:
                rw = RW.objects.get(village=village, name='RW %s' % rw_number)
            except:
                continue
            rt = RT()
            rt.rw = rw
            rt.name = 'RT %s' % rt_number
            rt.slug = slugify(rt.name)
            rt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0002_auto_20141130_2153'),
    ]

    operations = [
        migrations.RunPython(import_rt),
    ]
