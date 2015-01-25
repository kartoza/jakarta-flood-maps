# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flood_mapper', '0006_auto_20150120_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floodstatus',
            name='date_time',
            field=models.DateTimeField(help_text=b'Kapan kedalaman banjir tercapai. <br>Pergunakan pemilih tanggal dan waktu atau tambahkan sendiri <br>YYYY-MM-DD hh:mm'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='floodstatus',
            name='depth',
            field=models.DecimalField(help_text=b'Kedalaman dalam meter banjir RT tersebut. <br>Pilih kedalaman antara 0m and 10m', max_digits=4, decimal_places=2, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rt',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Nomor telepon harus dimasukan dalam format: '+6288888888888'. Diperbolehkan sampai 15 digit.")]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rt',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(help_text=b'Batas geografis', srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rt',
            name='name',
            field=models.CharField(help_text=b'Nama untuk RT.', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rw',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Nomor telepon harus dimasukan dalam format: '+6288888888888'. Diperbolehkan sampai 15 digit.")]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rw',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(help_text=b'Batas geografis', srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rw',
            name='name',
            field=models.CharField(help_text=b'Nama untuk RW.', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='village',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Nomor telepon harus dimasukan dalam format: '+6288888888888'. Diperbolehkan sampai 15 digit.")]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='village',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(help_text=b'Batas geografis', srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='village',
            name='name',
            field=models.CharField(help_text=b'Nama untuk kelurahan.', unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
