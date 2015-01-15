# coding=utf-8
"""Views."""
from django.shortcuts import render
from django.template import RequestContext

from flood_mapper.utilities.utilities import get_time_slice

# @login_required
# @staff_member_required
def flood_area_detail(request):
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
        'time_slice_verbose': time_slice_verbose
    }
    return render(
        request,
        # 'flood_mapper/add_flood_status_report.html',
        'flood_mapper/flood_area_detail.html',
        context_instance=RequestContext(request, context))
