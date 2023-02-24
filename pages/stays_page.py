from playwright.sync_api import Playwright, Page, expect, TimeoutError
from settings.settings import format_date, base_url_settings
import random
import string

# simple buttons
where_input = "//input[@placeholder='Where are you going?']"
calendar_button = "text=Check-out"
date_button = "//td[@data-bui-ref='calendar-date']"
submit_button = "//button[@type='submit']"
sign_close_button = "//button[@aria-label='Dismiss sign in information.']"
work_checkbox = "//label[@for='sb_travel_purpose_checkbox']"
next_month = "//div[@data-bui-ref='calendar-next']"
reg_button = "//a[@aria-label='Create an account']"

# registration
email_input = "//input[@type='email']"
password_input = "//input[@name='new_password']"
confirmed_password_input = "//input[@name='confirmed_password']"
wellcome_window = "text=Welcome to Booking.com"
close_wellcome_window_button = "//button[@class='modal-mask-closeBtn']"

# accommodation
accommodation_button = "//div[@data-component='search/group/group-with-modal']"
decrease_adult_button = "//button[@aria-label='Decrease number of Adults']"
increase_adult_button = "//button[@aria-label='Increase number of Adults']"
increase_child_button = "//button[@aria-label='Increase number of Children']"
increase_room_button = "//button[@aria-label='Increase number of Rooms']"

result_of_searching = "//div[@data-capla-component='b-search-web-searchresults/HeaderDesktop']"

# currencies
all_currencies = "//div[@data-testid='All currencies']"
currency_button = "//button[@data-testid='header-currency-picker-trigger']/span"


class StaysPage:

    def __init__(self, page: Page):
        self.page = page

    def close_sign_window(self): # without authorization there could be a window to dign up
        try:
            self.page.locator(sign_close_button).click()
        except TimeoutError:
            expect(self.page.locator(where_input)).to_be_visible(timeout=5000)
        return self

    def find_stay(self, place='', adults=2, children=0, rooms=1, work='', start_date='', days=''):

        # filling place
        self.page.locator(where_input).fill(place)

        # filling date
        self.page.query_selector(calendar_button).click(force=True)
        clicks, data_start, data_end = format_date(start_date, days)
        while clicks != 0:
            self.page.locator(next_month).click()
            clicks -= 1
        self.page.locator(f"//td[@data-date='{data_start}']").click()
        self.page.locator(f"//td[@data-date='{data_end}']").click()
        # checkbox work
        if work != '':
            self.page.locator(work_checkbox).click()
        # filling accommodation details
        if not adults == 2 and children == 0 and rooms == 1:
            self.page.locator(accommodation_button).click()
            if adults == 1:
                self.page.locator(decrease_adult_button).click()
            elif adults > 2:
                for i in range(adults - 2):
                    self.page.locator(increase_adult_button).click()
            if children > 0:
                for i in range(children):
                    self.page.locator(increase_child_button).click()
            if rooms > 1:
                for i in range(rooms - 1):
                    self.page.locator(increase_room_button).click()
        # search
        self.page.locator(submit_button).click()
        assert self.page.url.startswith(base_url_settings + 'searchresults')
        return self

    def change_currency(self, currency):
        # open currency window
        self.page.locator(currency_button).click()
        expect(self.page.locator(f"//div[text()='{currency}']")).to_be_visible(timeout=5000)
        # choose currency
        self.page.locator(f"//div[text()='{currency}']").click()
        # check edition
        expect(self.page.locator(currency_button).locator(f"text={currency}")).to_be_visible(timeout=10000)
        return self

    def registration(self):
        random_email = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '@mail.ru'
        random_password = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(9)) + '_'
        self.page.locator(reg_button).click()
        assert self.page.url.startswith('https://account.booking.com/register')
        self.page.locator(email_input).fill(random_email)
        self.page.locator(submit_button).click()
        self.page.locator(password_input).fill(random_password)
        self.page.locator(confirmed_password_input).fill(random_password)
        self.page.locator(submit_button).click()
        expect(self.page.locator(wellcome_window)).to_be_visible(timeout=10000)
        self.page.locator(close_wellcome_window_button).click()
        return self
