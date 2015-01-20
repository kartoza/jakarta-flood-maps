# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from flood_mapper.utilities.utilities import create_reports_directories


def create_report_directories(apps, schema_editor):
    create_reports_directories()


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0004_auto_20141216_1042'),
    ]

    operations = [
        migrations.RunPython(create_report_directories),
    ]
