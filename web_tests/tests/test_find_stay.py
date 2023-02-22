from сonftest import app_without_auth, get_playwright, app


def test_find_stay(app_without_auth):
    app_without_auth. \
        stays_page. \
        find_stay(place='Almaty', adults=2, children=2, rooms=2)