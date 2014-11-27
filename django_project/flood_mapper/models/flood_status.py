    # coding=utf-8
"""Model class for WMS Resource"""
__author__ = 'timlinux'
__project_name = 'jakarta-flood-maps'
__filename = 'village.py'
__date__ = '11/11/14'
__copyright__ = 'tim@kartoza.com'
__doc__ = ''

from django.contrib.gis.db import models

from flood_mapper.models.rt import RT

from users.models import User


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
        max_digits=2,
        decimal_places=2,
        help_text='The depth in metres that the RT is flooded.'
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

    def save_base(self, raw=False, cls=None, origin=None, force_insert=False,
                  force_update=False, using=None, update_fields=None):
        self.name = '%s -- %s: %s' % (self.date_time, self.rt, self.depth)
        super(FloodStatus, self).save_base(raw, cls, origin, force_insert,
                                           force_update, using, update_fields)

    def save(self, *args, **kwargs):
        """Overloaded save method."""
        super(FloodStatus, self).save(*args, **kwargs)
