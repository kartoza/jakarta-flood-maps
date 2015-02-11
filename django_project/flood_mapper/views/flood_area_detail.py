# coding=utf-8
"""Views."""
from django.shortcuts import render
from django.template import RequestContext

from flood_mapper.utilities.utilities import get_time_slice


def flood_area_detail(request):
    """View the flooded currently flooded areas. (Or upcoming if next is
    requested)
    """
    rw = request.GET.get('rw')
    if not rw:
        rw = 0
    if request.path_info == '/':
        home_page = True
    else:
        home_page = False
    if request.path_info == '/flood_area_detail_next/':
        time_slice = 'next'
        start, end = get_time_slice('next')
        time_slice_verbose = '%s - Now' % str(start)
    else:
        time_slice = 'current'
        start, end = get_time_slice()
        time_slice_verbose = '%s - %s' % (str(start), str(end))
    context = {
        'home_page': home_page,
        'time_slice': time_slice,
        'time_slice_verbose': time_slice_verbose,
        'rw': rw,
    }
    return render(
        request,
        # 'flood_mapper/add_flood_status_report.html',
        'flood_mapper/flood_area_detail.html',
        context_instance=RequestContext(request, context))
