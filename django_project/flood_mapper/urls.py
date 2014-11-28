# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(
        r'^add-flood-status-report/$',
        'flood_mapper.views.add_flood_status_report.add_flood_status_report'
    ),
)
