# coding=utf-8
"""Views."""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# from flood_mapper.models.flood_status import FloodStatus
# from flood_mapper.app_settings import *

from flood_mapper.forms.add_flood_status_report import AddFlodStatusForm


# @login_required
# @staff_member_required
def add_flood_status_report(request):
    """Add a flood status report

    :param request: A django request object.
    :type request: request

    :returns: Returns a flood status rport
    :rtype: HttpResponse
    """
    if request.method == "POST":
        form = AddFlodStatusForm(request.POST)
        if form.is_valid():

            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')
    else:
        form = AddFlodStatusForm()

    return render(
        request,
        # 'flood_mapper/add_flood_status_report.html',
        'flood_mapper/add_flood_status_report.html',
        context_instance=RequestContext(request, {'form': form}))
