from datetime import datetime, timedelta

headless_setting = True 
base_url_settings = "https://www.booking.com/"


def format_date(date_string, days=0):
    date_obj = datetime.strptime(date_string, '%d.%m.%Y')
    end_date = date_obj + timedelta(days=days)
    clicks = (date_obj.year - datetime.now().year) * 12 + (date_obj.month - datetime.now().month)
    start_date_str = date_obj.strftime('%Y-%m-%d')
    if datetime.now().day >= date_obj.day:
        clicks -= 1
    if days != 0:
        clicks += days // 30
        end_date_str = end_date.strftime('%Y-%m-%d')
        return clicks, start_date_str, end_date_str
    else:
        return clicks, start_date_str

