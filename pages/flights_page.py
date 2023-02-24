from playwright.sync_api import Playwright, Page, expect, TimeoutError
from settings.settings import base_url_settings, format_date

flight_page_text = "text=Compare and book flights with ease"
flight_class = "//select[@title='Cabin class']"
travellers_button = "text=1 adult"
increase_adults_button = "//button[@data-ui-sr='occupancy_adults_input_plus']"
increase_children_button = "//button[@data-ui-sr='occupancy_children_input_plus']"
child_age_element = "sr_occupancy_children_age_"
travellers_done_button = "//span[text()='Done']"
where_to_button = "//button[@data-ui-sr='location_input_to_0']"
where_to_input = "//input[@placeholder='Airport or city']"
calendar_button = "//button[@data-ui-sr='segment_date_input_0']"
submit_button = "text=Search"
next_month = "//button[@class='Actionable-module__root___TkUWg Button-module__root___2-9mg " \
             "Button-module__root--variant-tertiary___4w3xP Button-module__root--icon-only___Up8uO " \
             "Button-module__root--size-large___3piz9 Button-module__root--wide-false___geg2Y " \
             "Button-module__root--variant-tertiary-neutral___lxeUx Calendar-module__control___DIsDK " \
             "Calendar-module__control--next___jfyUl'] "


class FlightsPage:

    def __init__(self, page: Page):
        self.page = page

    def goto_flights(self):
        self.page.goto(base_url_settings + "flights")
        expect(self.page.locator(flight_page_text)).to_be_visible(timeout=10000)
        return self

    def find_round_flight(self, class_flight='', where_to='', start_date='',
                          days=''):
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
        # choose dates
        self.page.locator(calendar_button).click()
        clicks, data_start, data_end = format_date(start_date, days)
        while clicks != 0:
            self.page.locator(next_month).click()
            clicks -= 1
        self.page.locator(f"//span[@data-date='{data_start}']").click()
        self.page.locator(f"//span[@data-date='{data_end}']").click()
        # search
        self.page.locator(submit_button).click()
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
