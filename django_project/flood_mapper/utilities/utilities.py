from datetime import datetime, timedelta


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

