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
        r'^flood_area_detail/$',
        'flood_mapper.views.flood_area_detail.flood_area_detail'
    ),
    url(
        r'^api/reports/rw/(?P<rw_id>[\d]+)/$',
        'flood_mapper.views.reports_api.reports_rw_api'
    ),
    url(
        r'^api/locale/(?P<village>[\d]+)'
        r'/(?P<rw>[\d]+)'
        r'/('r'?P<rt>[\d]+)/$',
        'flood_mapper.views.boundary_api.boundary_api'
    ),
    url(
        r'^api/locale/(?P<village>[\d]+)'
        r'/(?P<rw>[\d]+)/$',
        'flood_mapper.views.boundary_api.boundary_api'
    ),
    url(
        r'^api/locale/(?P<village>[\d]+)/$',
        'flood_mapper.views.boundary_api.boundary_api'
    ),
    url(
        r'^api/locale/$',
        'flood_mapper.views.boundary_api.boundary_api'
    ),
)
