from playwright.sync_api import Playwright, Page, expect, TimeoutError
from settings.settings import base_url_settings, format_date
from pages.locators import *


class FlightsPage:

    def __init__(self, page: Page):
        self.page = page

    def goto_flights(self):
        self.page.goto(base_url_settings + "flights")
        expect(self.page.locator(flight_page_text)).to_be_visible(timeout=10000)
        return self

    def find_round_flight(self, start_date, days):
        # choose dates
        self.page.locator(flight_calendar_button).click()
        clicks, data_start, data_end = format_date(start_date, days)
        while clicks != 0:
            self.page.locator(next_month).click()
            clicks -= 1
        self.page.locator(f"//span[@data-date='{data_start}']").click()
        self.page.locator(f"//span[@data-date='{data_end}']").click()
        # search
        self.page.locator(search_button).click()
        assert self.page.url.startswith('https://flights.booking.com/flights/')
        return self

    def find_one_way_flight(self, date_of_flight):
        self.page.locator(one_way_button).click()
        # choose dates
        self.page.locator(flight_calendar_button).click()
        clicks, data_start = format_date(date_of_flight)
        while clicks != 0:
            self.page.locator(next_month).click()
            clicks -= 1
        self.page.locator(f"//span[@data-date='{data_start}']").click()
        # search
        self.page.locator(search_button).click()
        assert self.page.url.startswith('https://flights.booking.com/flights/')
        return self

    def change_count_of_travellers(self, adults=1, children=0, ages=None):
        if ages is None:
            ages = []
        if not (adults == 1 and children == 0):
            self.page.locator(travellers_button).click()
            if adults > 1:
                for i in range(adults - 1):
                    self.page.locator(increase_adults_button).click()
            if children > 0:
                for i in range(children):
                    self.page.locator(increase_children_button).click()
                    self.page.select_option(f"//select[@name='{child_age_element + str(i)}']", ages[i])
            self.page.locator(travellers_done_button).click()
        return self

    def choose_where(self, class_flight='ECONOMY', where_to=''):
        # choose class of flight
        if not class_flight == 'ECONOMY':
            self.page.select_option(flight_class, class_flight)
        # choose place of arrival
        self.page.locator(where_to_button).click()
        expect(self.page.locator(where_to_input)).to_be_visible(timeout=5000)
        self.page.locator(where_to_input).fill(where_to)
        self.page.wait_for_timeout(2000)
        self.page.keyboard.press('ArrowDown')
        self.page.keyboard.press('Enter')
        return self
