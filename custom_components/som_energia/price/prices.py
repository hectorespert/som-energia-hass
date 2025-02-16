import datetime as datetime
import os
from zoneinfo import ZoneInfo

from aiocsv import AsyncDictReader
from aiofiles import open
from aiozoneinfo import async_get_time_zone

from custom_components.som_energia.price.holidays import holidays

async def _read_price_csv() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "prices.csv")
    prices_data = {}
    async with open(file_path, mode='r') as file:
        async for row in AsyncDictReader(file):
            period = (row["Inicio Periodo"], row["Final Periodo"])
            prices_data[period] = {
                "punta": float(row["Punta"] if row["Punta"] != "" else 0.0),
                "llano": float(row["Llano"] if row["Llano"] != "" else 0.0),
                "valle": float(row["Valle"] if row["Valle"] != "" else 0.0),
                "compensation": float(row["Compensación"] if row["Compensación"] != "" else 0.0),
                "punta_generation_kwh": float(
                    row["Punta Generation kWh"] if row["Punta Generation kWh"] != "" else 0.0),
                "llano_generation_kwh": float(
                    row["Llano Generation kWh"] if row["Llano Generation kWh"] != "" else 0.0),
                "valle_generation_kwh": float(
                    row["Valle Generation kWh"] if row["Valle Generation kWh"] != "" else 0.0),
            }
    return prices_data


async def _prices_for_current_period(timezone_datetime: datetime, tz: ZoneInfo) -> dict:
    prices_of_the_period = {
        "punta": 0.0,
        "llano": 0.0,
        "valle": 0.0,
        "compensation": 0.0,
        "punta_generation_kwh": 0.0,
        "llano_generation_kwh": 0.0,
        "valle_generation_kwh": 0.0,
    }
    for period, prices_of_the_period in (await _read_price_csv()).items():
        prices_period_start = datetime.datetime.strptime(period[0], "%Y-%m-%d").replace(tzinfo=tz)
        prices_period_end = datetime.datetime.strptime(period[1], "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, microsecond=999999, tzinfo=tz
        )
        if prices_period_start <= timezone_datetime <= prices_period_end:
            prices_of_the_period = prices_of_the_period
            break
    return prices_of_the_period


async def _price(current_datetime: datetime, valle: str, llano: str, punta: str) -> float:
    tz = await async_get_time_zone("Europe/Madrid")
    timezone_datetime = current_datetime.astimezone(tz)
    prices_of_the_period = await _prices_for_current_period(timezone_datetime, tz)

    date = timezone_datetime.strftime("%Y-%m-%d")
    if date in holidays:
        return prices_of_the_period[valle]
    weekday = timezone_datetime.isoweekday()
    if weekday == 6 or weekday == 7:
        return prices_of_the_period[valle]
    hour = timezone_datetime.hour
    if 0 <= hour < 8:
        return prices_of_the_period[valle]
    elif 8 <= hour < 10 or 14 <= hour < 18 or 22 <= hour < 24:
        return prices_of_the_period[llano]
    else:
        return prices_of_the_period[punta]

async def price(current_datetime: datetime) -> float:
    return await _price(current_datetime, 'valle', 'llano', 'punta')


async def price_generation_kwh(current_datetime: datetime) -> float:
    return await _price(current_datetime, 'valle_generation_kwh', 'llano_generation_kwh', 'punta_generation_kwh')

async def compensation(current_datetime: datetime) -> float:
    tz = await async_get_time_zone("Europe/Madrid")
    timezone_datetime = current_datetime.astimezone(tz)
    prices_of_the_period = await _prices_for_current_period(timezone_datetime, tz)
    return prices_of_the_period['compensation']
