# coding=utf-8
"""Views."""
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from flood_mapper.models import FloodStatus
from flood_mapper.app_settings import *


@login_required
@staff_member_required
def report_flood_status(request):
    """Add a flood status report

    :param request: A django request object.
    :type request: request

    :returns: Returns a flood status rport
    :rtype: HttpResponse
    """
    context = dict()
    return render(
        request,
        'flood_mapper/index.html',
        context_instance=RequestContext(request, context))
