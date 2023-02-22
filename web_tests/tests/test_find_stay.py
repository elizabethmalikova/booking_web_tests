
def test_find_stay(app_without_auth):
    app_without_auth. \
        stay_page. \
        find_stay(place='Almaty', adults=2, children=2, rooms=2)
