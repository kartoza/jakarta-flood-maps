# coding=utf-8
"""Views."""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import os


def reports(request):
    available_reports = {}
    reports_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        os.path.pardir,
        'reports'))
    for (report_type, extention) in [
            ('pdf', '.pdf'),
            ('sqlite', '.sqlite'),
            ('shp', '.zip'),
            ('kml', '.kml'),
            ('csv', '.csv')]:
        report_type_dir = os.path.join(reports_dir, report_type)
        available_reports[report_type] = {}
        for report_period in ['6h', '24h']:
            report_type_time_period_dir = os.path.join(
                report_type_dir, report_period)
            directory_content = os.listdir(
                report_type_time_period_dir)
            available_reports[report_type][report_period] = [
                f for f in directory_content if f.endswith(extention)
            ]
            available_reports[report_type][report_period].sort(reverse=True)

    return render(
        request,
        'flood_mapper/reports.html',
        context_instance=RequestContext(
            request, {'reports': available_reports}))
