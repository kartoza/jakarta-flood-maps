# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon


def import_rw(apps, schema_editor):
    data_source = DataSource('flood_mapper/data/rw_jakarta_update.shp')
    RW = apps.get_model("flood_mapper", "RW")
    Village = apps.get_model("flood_mapper", "Village")
    # The data is on the first layer
    layer = data_source[0]
    for feature in layer:
        village_name = feature['KEL_NAME'].value
        rw_name = feature['RW'].value
        geometry = feature.geom
        village, created = Village.objects.get_or_create(
            name=village_name, slug=slugify(unicode(village_name)))
        village.save()
        rw, created = RW.objects.get_or_create(name=rw_name, village=village)
        if created:
            if 'MultiPolygon' not in geometry.geojson:
                geometry = MultiPolygon(Polygon(geometry.coords[0])).geojson
            else:
                geometry = geometry.geojson
        else:
            if 'MultiPolygon' not in geometry.geojson:
                geometry = MultiPolygon(
                    [Polygon(coords) for coords in rw.geometry.coords[0]] +
                    [Polygon(geometry.coords[0])]).geojson
            else:
                geometry = MultiPolygon(
                    [Polygon(coords) for coords in rw.geometry.coords[0]] +
                    [Polygon(coords) for coords in geometry.coords[0]]).geojson
        rw.geometry = geometry
        rw.slug = slugify(rw_name)
        rw.save()


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_rw),
    ]
