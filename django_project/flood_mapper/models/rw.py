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
from django.core.validators import MaxValueValidator, MinValueValidator
from owslib.wms import WebMapService, ServiceException, CapabilitiesError

from flood_mapper.models.boundary import Boundary
from flood_mapper.models.village import Village


class RW(Boundary):
    """RW Boundary."""

    class Meta:
        """Meta class."""
        app_label = 'flood_maps'

    slug = models.SlugField(
        unique=True,
        primary_key=True
    )

    name = models.CharField(
        help_text='A name for the RW.',
        null=False,
        blank=False,
        unique=True,
        max_length=100
    )

    village = models.ForeignKey(Village)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Overloaded save method."""
        self.slug = slugify(unicode(self.name))
        super(RW, self).save(*args, **kwargs)
