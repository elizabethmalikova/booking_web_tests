from pathlib import Path
from pytest import fixture
from playwright.sync_api import sync_playwright
from slugify import slugify
from pages.app import App
from settings.settings import *
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    screen_file = ''
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        if report.failed and "app_without_auth" in item.funcargs:
            app_without_auth = item.funcargs["app_without_auth"]
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            screen_file = str(screenshot_dir / f"{slugify(item.nodeid)}.png")
            app_without_auth.page.screenshot(path=screen_file)
        if report.failed and "app" in item.funcargs:
            app = item.funcargs["app"]
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            screen_file = str(screenshot_dir / f"{slugify(item.nodeid)}.png")
            app.page.screenshot(path=screen_file)
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # add the screenshots to the html report
            extra.append(pytest_html.extras.png(screen_file))
        report.extra = extra


@fixture(scope='function')
def get_playwright():
    with sync_playwright() as p:
        yield p


@fixture(scope='function')
def app(get_playwright):
    app = App(get_playwright, base_url=base_url_settings)
    yield app


@fixture(scope='function')
def app_without_auth(get_playwright, base_url=base_url_settings):
    app = App(get_playwright, base_url=base_url_settings, storage_state=None)
    yield app
