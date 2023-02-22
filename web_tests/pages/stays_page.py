from playwright.sync_api import Page, expect, TimeoutError
from web_tests.settings.settings import first_day_and_next_day_of_next_month


where_input = "//input[@class='c-autocomplete__input sb-searchbox__input sb-destination__input']"
calendar_button = "//div[@data-visible='accommodation,flights,rentalcars']"
date_button = "//td[@data-bui-ref='calendar-date']"
search_button = "//button[@type='submit']"

# accommodation
accommodation_button = "//div[@data-component='search/group/group-with-modal']"
decrease_adult_button = "//button[@aria-label='Decrease number of Adults']"
increase_adult_button = "//button[@aria-label='Increase number of Adults']"
decrease_child_button = "//button[@aria-label='Decrease number of Children']"
increase_child_button = "//button[@aria-label='Increase number of Children']"
decrease_room_button = "//button[@aria-label='Decrease number of Rooms']"
increase_room_button = "//button[@aria-label='Increase number of Rooms]"


class StaysPage:

    def __init__(self, page: Page):
        self.page = page

    def find_stay(self, place, adults, children, rooms):
        self.page.locator(where_input).fill(place)
        self.page.locator(calendar_button).click()
        data_start, data_end = first_day_and_next_day_of_next_month()
        self.page.locator(f"//td[@data-date='{data_start}']").click()
        self.page.locator(f"//td[@data-date='{data_end}']").click()
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
        self.page.locator(search_button).click()
        return self
