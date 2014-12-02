# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FloodStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('depth', models.DecimalField(help_text=b'The depth in metres that the RT is flooded.', max_digits=4, decimal_places=2, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('date_time', models.DateTimeField()),
                ('reporter_name', models.CharField(max_length=100)),
                ('reporting_medium', models.CharField(max_length=100)),
                ('notes', models.TextField()),
                ('recorded_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RT',
            fields=[
                ('contact_person', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_phone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+6288888888888'. Up to 15 digits allowed.")])),
                ('area', models.CharField(max_length=100, null=True, blank=True)),
                ('population', models.IntegerField(null=True, blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(help_text=b'An rw boundary', srid=4326, null=True, blank=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(help_text=b'A name for the RT.', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RW',
            fields=[
                ('contact_person', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_phone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+6288888888888'. Up to 15 digits allowed.")])),
                ('area', models.CharField(max_length=100, null=True, blank=True)),
                ('population', models.IntegerField(null=True, blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(help_text=b'An rw boundary', srid=4326, null=True, blank=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(help_text=b'A name for the RW.', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('contact_person', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_phone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+6288888888888'. Up to 15 digits allowed.")])),
                ('area', models.CharField(max_length=100, null=True, blank=True)),
                ('population', models.IntegerField(null=True, blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(help_text=b'An rw boundary', srid=4326, null=True, blank=True)),
                ('slug', models.SlugField(unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(help_text=b'A name for the village.', unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rw',
            name='village',
            field=models.ForeignKey(to='flood_mapper.Village'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rt',
            name='rw',
            field=models.ForeignKey(to='flood_mapper.RW'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='floodstatus',
            name='rt',
            field=models.ForeignKey(help_text=b'The RT that is affected.', to='flood_mapper.RT'),
            preserve_default=True,
        ),
    ]
