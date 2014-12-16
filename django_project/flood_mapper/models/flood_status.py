    # coding=utf-8
"""Model class for WMS Resource"""
__author__ = 'timlinux'
__project_name = 'jakarta-flood-maps'
__filename = 'village.py'
__date__ = '11/11/14'
__copyright__ = 'tim@kartoza.com'
__doc__ = ''

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from flood_mapper.models.rt import RT
from users.models import User

from rest_framework import serializers


class FloodStatus(models.Model):
    """Flood status model."""

    class Meta:
        """Meta class."""
        app_label = 'flood_mapper'

    name = models.CharField(max_length=200)
    rt = models.ForeignKey(
        RT,
        help_text='The RT that is affected.',
    )
    depth = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text='The depth in metres that the RT is flooded.',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
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

    def save_base(self, *args, **kwargs):
        self.name = '%s -- %s: %s' % (self.date_time, self.rt, self.depth)
        super(FloodStatus, self).save_base(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Overloaded save method."""
        super(FloodStatus, self).save(*args, **kwargs)


class FloodStatusSerializer(serializers.ModelSerializer):

    def transform_rw(self, obj, value):
        return obj.rt.rw

    def transform_village(self, obj, value):
        return obj.rt.rw.village

    class Meta:
        model = FloodStatus
        fields = ('id', 'rt', 'rw', 'village', 'depth')


class FloodStatusFullSerializer(FloodStatusSerializer):

    def transform_contact_person(self, obj, value):
        return obj.rt.contact_person

    def transform_contact_phone(self, obj, value):
        return obj.rt.contact_phone

    class Meta:
        model = FloodStatus
        fields = (
            'id', 'rt', 'rw', 'village', 'depth', 'contact_person',
            'contact_phone'
        )
