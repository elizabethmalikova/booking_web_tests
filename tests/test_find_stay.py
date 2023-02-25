from сonftest import app_without_auth, get_playwright, app


def test_find_stay(app_without_auth):
    app_without_auth. \
        stays_page. \
        close_sign_window(). \
        change_count_of_travellers(adults=1, children=2, rooms=3, ages=['5', '4']). \
        find_stay(place='Astana', start_date='15.04.2023', days=14, work='yes')
