# coding=utf-8
"""Model class for WMS Resource"""
__author__ = 'christian'
__project_name = 'jakarta-flood-maps'
__filename = 'boundary.py'
__date__ = '24/11/2014'
__copyright__ = 'christian@kartoza.com'
__doc__ = ''

from django.core.validators import RegexValidator
from django.contrib.gis.db import models


class Boundary(models.Model):
    """Boundary is an abstract model that RT, RW and Village inherit from."""
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    # from http://stackoverflow.com/a/19131360/1158060
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: "
                "'+6288888888888'. Up to 15 digits allowed.")
    contact_phone = models.CharField(
        max_length=15, validators=[phone_regex], blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)

    population = models.IntegerField(blank=True, null=True)

    geometry = models.PolygonField(  # MultiPolygonField
        srid=4326, null=True, blank=True, help_text='The geographic boundary')

    id = models.AutoField(primary_key=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True
        app_label = 'flood_mapper'
