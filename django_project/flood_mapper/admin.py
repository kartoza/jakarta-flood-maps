# coding=utf-8
"""Model Admin Class."""

from django.contrib import admin
from flood_mapper.models.wms_resource import FloodReport


class FloodReportAdmin(admin.ModelAdmin):
    """Admin Class for FloodReport Model."""
    exclude = ('slug',)
    list_display = ('name', 'uri')
    list_filter = ['name', 'uri']
    search_fields = ['name', 'description']

admin.site.register(FloodReport, FloodReportAdmin)
