# coding=utf-8
"""Model Admin Class."""

from django.contrib import admin
from flood_mapper.models.flood_status import FloodStatus


class FloodStatusAdmin(admin.ModelAdmin):
    """Admin Class for FloodReport Model."""
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(FloodStatus, FloodStatusAdmin)
