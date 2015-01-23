    # coding=utf-8
"""Model class for villages."""
__author__ = 'timlinux'
__project_name = 'jakarta-flood-maps'
__filename = 'village.py'
__date__ = '11/11/14'
__copyright__ = 'tim@kartoza.com'
__doc__ = ''

import os
from django.contrib.gis.db import models
from django.conf.global_settings import MEDIA_ROOT
from django.utils.text import slugify
# from django.core.validators import MaxValueValidator, MinValueValidator
# from owslib.wms import WebMapService, ServiceException, CapabilitiesError

from flood_mapper.models.boundary import Boundary
from flood_mapper.models.rw import RW

from rest_framework import serializers


class RT(Boundary):
    """RW Boundary."""

    class Meta:
        """Meta class."""
        app_label = 'flood_mapper'

    slug = models.SlugField(max_length=100)

    name = models.CharField(
        help_text='Nama untuk RT.',
        null=False,
        blank=False,
        unique=False,
        max_length=100
    )

    rw = models.ForeignKey(RW)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Overloaded save method."""
        self.slug = slugify(unicode(self.name))
        super(RT, self).save(*args, **kwargs)


class RTSerializer(serializers.ModelSerializer):

    class Meta:
        model = RT
        fields = ('id', 'name', 'slug', 'population', 'geometry')
