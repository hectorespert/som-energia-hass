from datetime import datetime

from custom_components.som_energia.price import price, compensation
from custom_components.som_energia.price.prices import price_generation_kwh, period


async def test_price_on_monday():
    monday = datetime(2022, 1, 24, 0, 0, 0)
    assert await price(monday) == 0.228

    monday = datetime(2022, 1, 24, 8, 0, 0)
    assert await price(monday) == 0.286

    monday = datetime(2022, 1, 24, 10, 0, 0)
    assert await price(monday) == 0.396

    monday = datetime(2022, 1, 24, 14, 0, 0)
    assert await price(monday) == 0.286

    monday = datetime(2022, 1, 24, 18, 0, 0)
    assert await price(monday) == 0.396

    monday = datetime(2022, 1, 24, 22, 0, 0)
    assert await price(monday) == 0.286

async def test_price_on_2024():
    monday = datetime(2024, 1, 24, 0, 0, 0)
    assert await price(monday) == 0.154

    monday = datetime(2024, 1, 24, 8, 0, 0)
    assert await price(monday) == 0.189

    monday = datetime(2024, 1, 24, 10, 0, 0)
    assert await price(monday) == 0.247

    monday = datetime(2024, 1, 24, 14, 0, 0)
    assert await price(monday) == 0.189

    monday = datetime(2024, 1, 24, 18, 0, 0)
    assert await price(monday) == 0.247

    monday = datetime(2024, 1, 24, 22, 0, 0)
    assert await price(monday) == 0.189

async def test_price_on_sunday():
    sunday = datetime(2022, 1, 23, 16, 57, 0)
    assert await price(sunday) == 0.228

async def test_price_on_2023():
    sunday = datetime(2023, 12, 23, 12, 30, 0)
    assert await price(sunday) == 0.199


async def test_price_on_holiday():
    holiday = datetime(2023, 1, 6, 16, 57, 0)
    assert await price(holiday) == 0.234

async def test_compensation():
    day = datetime(2023, 12, 23, 0, 0, 0)
    assert await compensation(day) == 0.130

async def test_compensation_2024():
    day = datetime(2024, 1, 23, 0, 0, 0)
    assert await compensation(day) == 0.070

async def test_price_generation_kwh():
    monday = datetime(2024, 1, 24, 0, 0, 0)
    assert await price_generation_kwh(monday) == 0.116

    monday = datetime(2024, 1, 24, 8, 0, 0)
    assert await price_generation_kwh(monday) == 0.139

    monday = datetime(2024, 1, 24, 10, 0, 0)
    assert await price_generation_kwh(monday) == 0.187

    monday = datetime(2024, 1, 24, 14, 0, 0)
    assert await price_generation_kwh(monday) == 0.139

    monday = datetime(2024, 1, 24, 18, 0, 0)
    assert await price_generation_kwh(monday) == 0.187

    monday = datetime(2024, 1, 24, 22, 0, 0)
    assert await price_generation_kwh(monday) == 0.139

async def test_period_on_weekday_valle():
    monday = datetime(2022, 1, 24, 0, 0, 0)
    assert await period(monday) == "P3"

    monday = datetime(2022, 1, 24, 4, 30, 0)
    assert await period(monday) == "P3"

    monday = datetime(2022, 1, 24, 7, 59, 0)
    assert await period(monday) == "P3"

async def test_period_on_weekday_llano():
    monday = datetime(2022, 1, 24, 8, 0, 0)
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 9, 30, 0)
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 14, 0, 0)
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 16, 0, 0)
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 22, 0, 0)
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 23, 30, 0)
    assert await period(monday) == "P2"

async def test_period_on_weekday_punta():
    monday = datetime(2022, 1, 24, 10, 0, 0)
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 12, 0, 0)
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 13, 59, 0)
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 18, 0, 0)
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 20, 0, 0)
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 21, 59, 0)
    assert await period(monday) == "P1"

async def test_period_on_weekend():
    saturday = datetime(2022, 1, 22, 12, 0, 0)
    assert await period(saturday) == "P3"

    sunday = datetime(2022, 1, 23, 16, 57, 0)
    assert await period(sunday) == "P3"

    sunday = datetime(2022, 1, 23, 0, 0, 0)
    assert await period(sunday) == "P3"

async def test_period_on_holiday():
    holiday = datetime(2023, 1, 6, 16, 57, 0)
    assert await period(holiday) == "P3"

    holiday = datetime(2023, 1, 6, 10, 0, 0)
    assert await period(holiday) == "P3"

    holiday = datetime(2023, 12, 25, 12, 0, 0)
    assert await period(holiday) == "P3"


