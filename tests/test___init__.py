from datetime import datetime

from custom_components.som_energia.price import price, compensation


def test_price_on_monday():
    monday = datetime(2022, 1, 24, 0, 0, 0)
    assert price(monday) == 0.241994

    monday = datetime(2022, 1, 24, 8, 0, 0)
    assert price(monday) == 0.288204

    monday = datetime(2022, 1, 24, 10, 0, 0)
    assert price(monday) == 0.358735

    monday = datetime(2022, 1, 24, 14, 0, 0)
    assert price(monday) == 0.288204

    monday = datetime(2022, 1, 24, 18, 0, 0)
    assert price(monday) == 0.358735

    monday = datetime(2022, 1, 24, 22, 0, 0)
    assert price(monday) == 0.288204


def test_price_on_sunday():
    sunday = datetime(2022, 1, 23, 16, 57, 0)
    assert price(sunday) == 0.241994


def test_price_on_holiday():
    holiday = datetime(2023, 1, 6, 16, 57, 0)
    assert price(holiday) == 0.241994


def test_compensation():
    monday = datetime(2022, 1, 24, 0, 0, 0)
    assert compensation(monday) == 0.130
