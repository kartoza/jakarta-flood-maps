# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0007_auto_20150125_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floodstatus',
            name='date_time',
            field=models.DateTimeField(help_text=b'Kapan kedalaman banjir tercapai. <br>Pergunakan pemilih tanggal dan waktu atau tambahkan sendiri <br>YYYY-MM-DD hh:mm', verbose_name='Date Time (Asia/Jakarta)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='floodstatus',
            name='rt',
            field=models.ForeignKey(help_text=b'RT yang terdampak.', to='flood_mapper.RT'),
            preserve_default=True,
        ),
    ]
