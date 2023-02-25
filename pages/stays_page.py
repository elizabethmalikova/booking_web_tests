from playwright.sync_api import Playwright, Page, expect, TimeoutError
from settings.settings import format_date, base_url_settings
import random
import string
from pages.locators import *


class StaysPage:

    def __init__(self, page: Page):
        self.page = page

    def close_sign_window(self):  # without authorization there could be a window to sign up
        try:
            self.page.locator(sign_close_button).click()
        except TimeoutError:
            expect(self.page.locator(where_input)).to_be_visible(timeout=5000)
        return self

    def find_stay(self, place='', work='', start_date='', days=''):
        # filling place
        self.page.locator(where_input).fill(place)
        # filling date
        self.page.query_selector(stays_calendar_button).click(force=True)
        clicks, data_start, data_end = format_date(start_date, days)
        while clicks:
            self.page.locator(next_month_button).click()
            clicks -= 1
        self.page.locator(f"//td[@data-date='{data_start}']").click()
        self.page.locator(f"//td[@data-date='{data_end}']").click()
        # checkbox work
        if work:
            self.page.locator(work_checkbox).click()
        # search
        self.page.locator(submit_button).click()
        assert self.page.url.startswith(base_url_settings + 'searchresults')
        return self

    def change_count_of_travellers(self, adults=2, children=0, ages=None, rooms=1):
        if ages is None:
            ages = []
        # filling accommodation details
        if not (adults == 2 and children == 0 and rooms == 1):
            self.page.locator(accommodation_button).click()
            if adults == 1:
                self.page.locator(decrease_adult_button).click()
            elif adults > 2:
                for i in range(adults - 2):
                    self.page.locator(increase_adult_button).click()
            for i in range(children):
                self.page.locator(increase_child_button).click()
                self.page.select_option(f"//select[@data-group-child-age='{str(i)}']", ages[i])
            for i in range(rooms - 1):
                self.page.locator(increase_room_button).click()
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
