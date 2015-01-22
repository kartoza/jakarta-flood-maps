from datetime import datetime, timedelta
import os


def get_time_slice(time_slice='current'):
    """Get the most recent start and end date range.


    :return: last time slice start, and end date
    :rtype: datetime, datetime
    """
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    if now.hour > 18:
        start_date_time = datetime(
            now.year, now.month, now.day, 12, 0, 0, 0)
        end_date_time = datetime(
            now.year, now.month, now.day, 18, 0, 0, 0)
    elif now.hour > 12:
        start_date_time = datetime(
            now.year, now.month, now.day, 6, 0, 0, 0)
        end_date_time = datetime(
            now.year, now.month, now.day, 12, 0, 0, 0)
    elif now.hour > 6:
        start_date_time = datetime(
            now.year, now.month, now.day, 0, 0, 0, 0)
        end_date_time = datetime(
            now.year, now.month, now.day, 6, 0, 0, 0)
    else:
        start_date_time = datetime(
            yesterday.year, yesterday.month, yesterday.day, 18, 0, 0, 0)
        end_date_time = datetime(
            now.year, now.month, now.day, 0, 0, 0, 0)
    if time_slice == 'current':
        return start_date_time, end_date_time
    elif time_slice == 'next':
        return end_date_time, now


def create_reports_directories():
    reports_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        os.path.pardir,
        'reports'))
    if not os.path.exists(reports_dir):
        os.mkdir(reports_dir)
    if not os.path.exists(reports_dir):
        raise Exception('could not create report directories')
    for report_type in ['pdf', 'sqlite', 'shp', 'kml', 'csv']:
        report_type_dir = os.path.join(reports_dir, report_type)
        if not os.path.exists(report_type_dir):
            os.mkdir(report_type_dir)
        if not os.path.exists(report_type_dir):
            raise Exception('could not create report directories')
        for report_period in ['6h', '24h']:
            report_type_time_period_dir = os.path.join(
                report_type_dir, report_period)
            if not os.path.exists(report_type_time_period_dir):
                os.mkdir(report_type_time_period_dir)
            if not os.path.exists(report_type_time_period_dir):
                raise Exception('could not create report directories')
