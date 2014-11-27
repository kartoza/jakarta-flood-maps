# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'flood_mapper.views.report_flood_status.report_flood_status',
        name='report_flood_status'),
)
