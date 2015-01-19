from django.http import Http404, HttpResponse
import os


def download_api(request, report_type, time_slice, filename):
    def sanitize(text_string):
        return text_string.replace('/', '').replace('..', '')
    report_type = sanitize(report_type)
    time_slice = sanitize(time_slice)
    filename = sanitize(filename)
    if report_type not in ['pdf', 'kml', 'csv', 'shp', 'sqlite']:
        raise Http404
    if time_slice not in ['6h', '24h']:
        raise Http404
    full_report_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        os.path.pardir,
        'reports',
        report_type,
        time_slice,
        filename))
    if not os.path.exists(full_report_path):
        raise Http404
    fd = open(full_report_path, 'r')
    response = HttpResponse(fd, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response


