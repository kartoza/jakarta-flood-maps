# coding=utf-8
"""Add flood status reports.

author: christian@kartoza.com
date: December 2014
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from flood_mapper.forms.add_flood_status_report import AddFloodStatusForm


@login_required
def add_flood_status_report(request):
    """Add a flood status report

    :param request: A django request object.
    :type request: request

    :returns: Returns a flood status rport
    :rtype: HttpResponse
    """
    if request.method == "POST":
        form = AddFloodStatusForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            # model_instance.recorded_by = request.user
            model_instance.recorded_by = User.objects.all()[0]
            model_instance.save()
            return redirect(
                '/flood_area_detail_next/?rw=%s' % model_instance.rt.rw.id)
        else:
            return render(
                request,
                'flood_mapper/add_flood_status_report.html',
                context_instance=RequestContext(request, {'form': form}))

    form = AddFloodStatusForm()

    return render(
        request,
        'flood_mapper/add_flood_status_report.html',
        context_instance=RequestContext(request, {'form': form}))
