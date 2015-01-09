# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import os
from django.db import models, migrations
from django.utils.text import slugify

import csv


def import_rt(apps, schema_editor):
    file = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        'data',
        'List of RT DKI Jakarta - updated 2012.csv'))
    RT = apps.get_model("flood_mapper", "RT")
    RW = apps.get_model("flood_mapper", "RW")
    Village = apps.get_model("flood_mapper", "Village")
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            village_name = row[0]

            rw_number = int(row[1])
            rt_number = int(row[2])

            village_name_slug = slugify(unicode(village_name))
            try:
                village = Village.objects.get(slug=village_name_slug)
            except:
                print village_name
                raise
            try:
                rw = RW.objects.get(
                    village=village, name='RW %02.0f' % rw_number)
            except:
                print village_name, rw_number
                raise
            rt = RT()
            rt.rw = rw
            rt.name = 'RT %02.0f' % rt_number
            rt.slug = slugify(rt.name)
            rt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0002_data_migration_20141130_2153'),
    ]

    operations = [
        migrations.RunPython(import_rt),
    ]
