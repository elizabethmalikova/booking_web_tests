from сonftest import app_without_auth, get_playwright, app


def test_find_stay(app_without_auth):
    app_without_auth. \
        stays_page. \
        find_stay(place='Astana', rooms=2, start_date='25.04.2023', days=14, work='yes')