    # coding=utf-8
"""Model class for WMS Resource"""
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

from flood_mapper.models.rt import RT
from flood_mapper.models.user import User


class FloodStatus(models.Model):
    """Flood status model."""

    class Meta:
        """Meta class."""
        app_label = 'flood_maps'

    rt = models.ForeignKey(
        RT,
        help_text='The RT that has is affected.',
    )
    depth = models.DecimalField(
        max_digits=2,
        decimal_places=2,
        helper_ext='The depth in metres that the RT is flooded.'
    )
    date_time = models.DateTimeField()
    recorded_by = models.ForeignKey(User)
    reporter_name = models.CharField(
        max_length=100
    )
    reporting_medium = models.CharField(
        max_length=100
    )
    notes = models.TextField()


    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Overloaded save method."""
        super(FloodStatus, self).save(*args, **kwargs)
