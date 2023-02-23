from сonftest import app_without_auth, get_playwright, app


def test_find_stay(app_without_auth):
    app_without_auth. \
        stays_page. \
        close_sign_window(). \
        find_stay(place='Astana', adults=1, children=4, rooms=3, start_date='25.04.2023', days=14, work='yes')
