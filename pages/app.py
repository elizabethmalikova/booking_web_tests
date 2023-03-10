from playwright.sync_api import Playwright
from pages.stays_page import StaysPage
from pages.flights_page import FlightsPage
from settings.settings import *


class App:

    def __init__(self, playwright: Playwright, base_url: str, storage_state='state.json'):
        self.browser = playwright.chromium.launch(headless=headless_setting)
        self.context = self.browser.new_context(locale='en-GB', storage_state=storage_state)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.page.goto(base_url)
        self.stays_page = StaysPage(self.page)
        self.flights_page = FlightsPage(self.page)

    def save_state(self):
        self.context.storage_state(path="state.json")

    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)