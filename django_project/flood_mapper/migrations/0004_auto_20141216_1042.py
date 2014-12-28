# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0003_data_migration_20141201_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floodstatus',
            name='notes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='village',
            name='slug',
            field=models.SlugField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
