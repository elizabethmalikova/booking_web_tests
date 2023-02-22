from datetime import date, timedelta

headless_setting = False
base_url_settings = "https://www.booking.com"


def first_day_and_next_day_of_next_month():
    today = date.today()
    year = today.year
    month = today.month
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    first_day_of_next_month = date(year, month, 1)
    next_day = first_day_of_next_month + timedelta(days=1)
    return first_day_of_next_month.strftime("%Y-%d-%m"), next_day.strftime("%Y-%d-%m")
