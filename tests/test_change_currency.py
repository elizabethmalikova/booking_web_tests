from сonftest import app_without_auth, get_playwright, app


# test doesn't work in headless
def test_change_currency(app_without_auth):
    app_without_auth. \
        stays_page. \
        close_sign_window(). \
        change_currency("CLP")
