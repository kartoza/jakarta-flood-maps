# coding=utf-8
"""Views."""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext



# @login_required
# @staff_member_required
def reports(request):

    return render(
        request,
        'flood_mapper/reports.html',
        context_instance=RequestContext(request, {}))
