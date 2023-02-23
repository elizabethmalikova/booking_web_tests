from сonftest import app_without_auth, get_playwright, app


def test_registration(app_without_auth):
    app_without_auth. \
        stays_page. \
        close_sign_window(). \
        registration()
