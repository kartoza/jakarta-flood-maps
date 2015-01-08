# coding=utf-8
"""Views."""
from django.shortcuts import render
from django.template import RequestContext


# @login_required
# @staff_member_required
def flood_area_detail(request):
    if request.path_info == '/':
        context = {'home_page': True}
    else:
        context = {'home_page': False}
    return render(
        request,
        # 'flood_mapper/add_flood_status_report.html',
        'flood_mapper/flood_area_detail.html',
        context_instance=RequestContext(request, context))
