from playwright.sync_api import Playwright, Page, expect, TimeoutError
from settings.settings import format_date, base_url_settings

# simple buttons
where_input = "//input[@placeholder='Where are you going?']"
calendar_button = "text=Check-out"
date_button = "//td[@data-bui-ref='calendar-date']"
search_button = "//button[@type='submit']"
sign_close_button = "//button[@aria-label='Dismiss sign in information.']"
work_checkbox = "//label[@for='sb_travel_purpose_checkbox']"
next_month = "//div[@data-bui-ref='calendar-next']"

# accommodation
accommodation_button = "//div[@data-component='search/group/group-with-modal']"
decrease_adult_button = "//button[@aria-label='Decrease number of Adults']"
increase_adult_button = "//button[@aria-label='Increase number of Adults']"
decrease_child_button = "//button[@aria-label='Decrease number of Children']"
increase_child_button = "//button[@aria-label='Increase number of Children']"
decrease_room_button = "//button[@aria-label='Decrease number of Rooms']"
increase_room_button = "//button[@aria-label='Increase number of Rooms']"

result_of_searching = "//div[@data-capla-component='b-search-web-searchresults/HeaderDesktop']"


class StaysPage:

    def __init__(self, page: Page):
        self.page = page

    def find_stay(self, place='', adults=2, children=0, rooms=1, work='', start_date='', days=''):

        # for registration modal
        try:
            self.page.locator(sign_close_button).click()
        except TimeoutError:
            expect(self.page.locator(where_input)).to_be_visible(timeout=5000)

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

        # filling accommodation details
        if adults == 2 and children == 0 and rooms == 1:
            self.page.locator(search_button).click()
        else:
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

        # checkbox work-traveling
        if work != '':
            self.page.locator(work_checkbox).click()
        # search
        self.page.locator(search_button).click()
        assert self.page.url.startswith(base_url_settings + 'searchresults')
        return self
