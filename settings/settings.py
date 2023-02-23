from datetime import datetime, timedelta

headless_setting = False
base_url_settings = "https://www.booking.com/"


def format_date(date_string, days):
    date_obj = datetime.strptime(date_string, '%d.%m.%Y')
    end_date = date_obj + timedelta(days=days)
    clicks = (date_obj.year - datetime.now().year) * 12 + (date_obj.month - datetime.now().month)
    if datetime.now().day >= date_obj.day:
        clicks -= 1
    if days:
        clicks += days // 30
    start_date_str = date_obj.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    return clicks, start_date_str, end_date_str

