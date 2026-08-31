from datetime import datetime
from zoneinfo import ZoneInfo

from custom_components.som_energia.price import price, compensation
from custom_components.som_energia.price.prices import price_generation_kwh, period


async def test_price_on_monday():
    monday = datetime(2022, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.228

    monday = datetime(2022, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.286

    monday = datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.396

    monday = datetime(2022, 1, 24, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.286

    monday = datetime(2022, 1, 24, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.396

    monday = datetime(2022, 1, 24, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.286

async def test_price_on_2022_02():
    monday = datetime(2022, 2, 28, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.262

    monday = datetime(2022, 2, 28, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.320

    monday = datetime(2022, 2, 28, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.407

async def test_price_on_2022_04():
    monday = datetime(2022, 4, 4, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.261

    monday = datetime(2022, 4, 4, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.315

    monday = datetime(2022, 4, 4, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.380

async def test_price_on_2022_06():
    monday = datetime(2022, 6, 6, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.241

    monday = datetime(2022, 6, 6, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.293

    monday = datetime(2022, 6, 6, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.357

async def test_price_on_2022_10():
    monday = datetime(2022, 10, 3, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.234

    monday = datetime(2022, 10, 3, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.281

    monday = datetime(2022, 10, 3, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.343

async def test_price_on_2024():
    monday = datetime(2024, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.154

    monday = datetime(2024, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.189

    monday = datetime(2024, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.247

    monday = datetime(2024, 1, 24, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.189

    monday = datetime(2024, 1, 24, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.247

    monday = datetime(2024, 1, 24, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.189

async def test_price_on_2026():
    monday = datetime(2026, 1, 26, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.125

    monday = datetime(2026, 1, 26, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.153

    monday = datetime(2026, 1, 26, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.229

    monday = datetime(2026, 1, 26, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.153

    monday = datetime(2026, 1, 26, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.229

    monday = datetime(2026, 1, 26, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.153

async def test_price_on_2026_05():
    monday = datetime(2026, 5, 4, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.124

    monday = datetime(2026, 5, 4, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.150

    monday = datetime(2026, 5, 4, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.226

    monday = datetime(2026, 5, 4, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.150

    monday = datetime(2026, 5, 4, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.226

    monday = datetime(2026, 5, 4, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.150

async def test_price_on_2026_10():
    monday = datetime(2026, 10, 5, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.150

    monday = datetime(2026, 10, 5, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.169

    monday = datetime(2026, 10, 5, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.249

    monday = datetime(2026, 10, 5, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.169

    monday = datetime(2026, 10, 5, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.249

    monday = datetime(2026, 10, 5, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.169

async def test_price_on_sunday():
    sunday = datetime(2022, 1, 23, 16, 57, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(sunday) == 0.228

async def test_price_on_2023():
    sunday = datetime(2023, 12, 23, 12, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(sunday) == 0.199


async def test_price_on_holiday():
    holiday = datetime(2023, 1, 6, 16, 57, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(holiday) == 0.234

async def test_compensation():
    day = datetime(2023, 12, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await compensation(day) == 0.130

async def test_compensation_2024():
    day = datetime(2024, 1, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await compensation(day) == 0.070

async def test_compensation_2026():
    day = datetime(2026, 1, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await compensation(day) == 0.030

async def test_compensation_2026_10():
    day = datetime(2026, 10, 5, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await compensation(day) == 0.030

async def test_price_generation_kwh():
    monday = datetime(2024, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.116

    monday = datetime(2024, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.139

    monday = datetime(2024, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.187

    monday = datetime(2024, 1, 24, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.139

    monday = datetime(2024, 1, 24, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.187

    monday = datetime(2024, 1, 24, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.139

async def test_price_generation_kwh_2022():
    monday = datetime(2022, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.105

    monday = datetime(2022, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.137

    monday = datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.236

    monday = datetime(2022, 6, 6, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.170

async def test_price_generation_kwh_2023():
    monday = datetime(2023, 1, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.111

    monday = datetime(2023, 1, 23, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.135

    monday = datetime(2023, 1, 23, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.183

    monday = datetime(2023, 5, 22, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.126

    monday = datetime(2023, 5, 22, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.150

    monday = datetime(2023, 5, 22, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.197

async def test_price_generation_kwh_2026():
    monday = datetime(2026, 1, 26, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.110

    monday = datetime(2026, 1, 26, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.135

    monday = datetime(2026, 1, 26, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.205

    monday = datetime(2026, 1, 26, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.135

    monday = datetime(2026, 1, 26, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.205

    monday = datetime(2026, 1, 26, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.135

async def test_price_generation_kwh_2026_05():
    monday = datetime(2026, 5, 4, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.099

    monday = datetime(2026, 5, 4, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

    monday = datetime(2026, 5, 4, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.194

    monday = datetime(2026, 5, 4, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

    monday = datetime(2026, 5, 4, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.194

    monday = datetime(2026, 5, 4, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

async def test_price_generation_kwh_2026_10():
    monday = datetime(2026, 10, 5, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.099

    monday = datetime(2026, 10, 5, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

    monday = datetime(2026, 10, 5, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.194

    monday = datetime(2026, 10, 5, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

    monday = datetime(2026, 10, 5, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.194

    monday = datetime(2026, 10, 5, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

async def test_price_before_the_first_price_period():
    before = datetime(2019, 6, 12, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(before) is None
    assert await price_generation_kwh(before) is None
    assert await compensation(before) is None

    before = datetime(2021, 12, 31, 23, 59, 59, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(before) is None
    assert await price_generation_kwh(before) is None
    assert await compensation(before) is None


async def test_price_on_the_first_second_of_the_first_price_period():
    first = datetime(2022, 1, 1, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(first) == 0.228
    assert await compensation(first) == 0.000


async def test_period_on_weekday_valle():
    monday = datetime(2022, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P3"

    monday = datetime(2022, 1, 24, 4, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P3"

    monday = datetime(2022, 1, 24, 7, 59, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P3"

async def test_period_on_weekday_llano():
    monday = datetime(2022, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 9, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 16, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 23, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

async def test_period_on_weekday_punta():
    monday = datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 13, 59, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 20, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 21, 59, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

async def test_period_on_weekend():
    saturday = datetime(2022, 1, 22, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(saturday) == "P3"

    sunday = datetime(2022, 1, 23, 16, 57, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(sunday) == "P3"

    sunday = datetime(2022, 1, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(sunday) == "P3"

async def test_period_on_holiday():
    holiday = datetime(2023, 1, 6, 16, 57, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(holiday) == "P3"

    holiday = datetime(2023, 1, 6, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(holiday) == "P3"

    holiday = datetime(2023, 12, 25, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(holiday) == "P3"

async def test_price_with_utc_timezone():
    monday_utc = datetime(2022, 1, 24, 7, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await price(monday_utc) == 0.286

    monday_utc = datetime(2022, 1, 24, 9, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await price(monday_utc) == 0.396

    monday_utc = datetime(2022, 1, 24, 17, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await price(monday_utc) == 0.396

async def test_period_with_utc_timezone():
    monday_utc = datetime(2022, 1, 23, 23, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await period(monday_utc) == "P3"

    monday_utc = datetime(2022, 1, 24, 7, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await period(monday_utc) == "P2"

    monday_utc = datetime(2022, 1, 24, 9, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await period(monday_utc) == "P1"

    monday_utc = datetime(2022, 1, 24, 13, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await period(monday_utc) == "P2"

