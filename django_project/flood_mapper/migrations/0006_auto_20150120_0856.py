# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0005_data_migration_create_report_dirs_20150112_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floodstatus',
            name='date_time',
            field=models.DateTimeField(help_text=b'When the flood level was reached. <br>Use the date time picker or add manually. <br>YYYY-MM-DD hh:mm'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='floodstatus',
            name='depth',
            field=models.DecimalField(help_text=b'The depth in metres that the RT is flooded. <br>Choose a depth between 0m and 10m', max_digits=4, decimal_places=2, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
    ]
