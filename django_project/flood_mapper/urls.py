# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(
        r'^add-flood-status-report/$',
        'flood_mapper.views.add_flood_status_report.add_flood_status_report'
    ),
    url(
        r'^api/(?P<village>[\s|\d|\w]+)'
        r'/(?P<rw>[\s|\d|\w]+)'
        r'/('r'?P<rt>[\s|\d|\w]+)/$',
        'flood_mapper.views.boundary_api.boundary_api'
    ),
    url(
        r'^api/(?P<village>[\s|\d|\w]+)'
        r'/(?P<rw>[\s|\d|\w]+)/$',
        'flood_mapper.views.boundary_api.boundary_api'
    ),
    url(
        r'^api/(?P<village>[\s|\d|\w]+)/$',
        'flood_mapper.views.boundary_api.boundary_api'
    ),
)
