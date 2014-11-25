# coding=utf-8
"""Views."""

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from flood_mapper.models import FloodStatus
from flood_mapper.app_settings import *


def index(request):
    """Index page which renders a basic hello.

    :param request: A django request object.
    :type request: request

    :returns: Response will be a nice looking index page.
    :rtype: HttpResponse
    """
    context = dict()
    return render(
        request,
        'flood_mapper/index.html',
        context_instance=RequestContext(request, context))
