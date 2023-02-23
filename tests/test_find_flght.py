from сonftest import app_without_auth, get_playwright, app

class_flights = ['ECONOMY', 'PREMIUM_ECONOMY', 'BUSINESS', 'FIRST']


def test_find_flight(app_without_auth):
    app_without_auth. \
        stays_page. \
        close_sign_window()
    app_without_auth. \
        flights_page. \
        goto_flights(). \
        find_round_flight(class_flight=class_flights[1], adults=2, children=1, where_to='KUF', start_date='23.06.2023',
                          days=7)

