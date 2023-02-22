from playwright.sync_api import Playwright
from web_tests.pages.stays_page import StaysPage
from web_tests.settings.settings import *


class App:

    def __init__(self, playwright: Playwright, base_url: str, storage_state='state.json'):
        self.browser = playwright.chromium.launch(headless=headless_setting)
        self.context = self.browser.new_context(locale='en-GB', storage_state=storage_state)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.page.goto(base_url)
        self.stays_page = StaysPage(self.page)

    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)
