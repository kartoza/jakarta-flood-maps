# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

from django.contrib.gis.gdal import DataSource


def import_rw(apps, schema_editor):
    data_source = DataSource('flood_mapper/data/rw_jakarta_update.shp')
    RW = apps.get_model("flood_mapper", "RW")
    Village = apps.get_model("flood_mapper", "Village")
    # The data is on the first layer
    layer = data_source[0]
    for feature in layer:
        village_name = feature['KEL_NAME'].value
        rw_name = feature['RW'].value
        geometry = feature.geom.geojson
        village, created = Village.objects.get_or_create(
            name=village_name, slug=slugify(unicode(village_name)))
        village.save()
        rw = RW(name=rw_name)
        if 'MultiPolygon' not in geometry:
            rw.geometry = geometry
        rw.village = village
        rw.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_rw),
    ]
