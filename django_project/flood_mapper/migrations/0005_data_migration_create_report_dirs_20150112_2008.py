# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import os


def create_report_directories(apps, schema_editor):
    reports_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        os.path.pardir,
        'reports'))
    if not os.path.exists(reports_dir):
        os.mkdir(reports_dir)
    for report_type in ['pdf', 'sqlite', 'shp', 'kml', 'csv']:
        report_type_dir = os.path.join(reports_dir, report_type)
        if not os.path.exists(report_type_dir):
            os.mkdir(report_type_dir)
        for report_period in ['6h', '24h']:
            report_type_time_period_dir = os.path.join(
                report_type_dir, report_period)
            if not os.path.exists(report_type_time_period_dir):
                os.mkdir(report_type_time_period_dir)


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0004_auto_20141216_1042'),
    ]

    operations = [
        migrations.RunPython(create_report_directories),
    ]
