from asyncio import get_running_loop
import csv
import datetime
import os

from homeassistant.exceptions import HomeAssistantError
from homeassistant.util.dt import async_get_time_zone

from custom_components.som_energia.price.tariff_holiday import is_tariff_holiday

TIME_ZONE = "Europe/Madrid"


def _read_price_csv() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "prices.csv")
    prices_data = {}
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
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


async def _madrid_time(current_datetime: datetime.datetime) -> datetime.datetime:
    """Convert to Spanish local time, which is what every tariff rule is defined in."""
    tz = await async_get_time_zone(TIME_ZONE)
    if tz is None:
        # astimezone(None) would silently fall back to the host's local time and
        # serve the prices of the wrong hours, so refuse instead.
        raise HomeAssistantError(f"Time zone {TIME_ZONE} is not available")
    return current_datetime.astimezone(tz)


async def _prices_for_current_period(timezone_datetime: datetime.datetime) -> dict | None:
    prices_data = await get_running_loop().run_in_executor(None, _read_price_csv)
    tz = timezone_datetime.tzinfo
    for (start, end), prices_of_the_period in prices_data.items():
        prices_period_start = datetime.datetime.strptime(start, "%Y-%m-%d").replace(tzinfo=tz)
        prices_period_end = datetime.datetime.strptime(end, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, microsecond=999999, tzinfo=tz
        )
        if prices_period_start <= timezone_datetime <= prices_period_end:
            return prices_of_the_period
    return None


async def _price(current_datetime: datetime.datetime, valle: str, llano: str, punta: str) -> float | None:
    timezone_datetime = await _madrid_time(current_datetime)
    prices_of_the_period = await _prices_for_current_period(timezone_datetime)
    if prices_of_the_period is None:
        return None
    current_period = await period(current_datetime)
    if current_period == "P1":
        return prices_of_the_period[punta]
    elif current_period == "P2":
        return prices_of_the_period[llano]
    else:
        return prices_of_the_period[valle]


async def price(current_datetime: datetime.datetime) -> float | None:
    return await _price(current_datetime, 'valle', 'llano', 'punta')


async def price_generation_kwh(current_datetime: datetime.datetime) -> float | None:
    return await _price(current_datetime, 'valle_generation_kwh', 'llano_generation_kwh', 'punta_generation_kwh')


async def compensation(current_datetime: datetime.datetime) -> float | None:
    timezone_datetime = await _madrid_time(current_datetime)
    prices_of_the_period = await _prices_for_current_period(timezone_datetime)
    if prices_of_the_period is None:
        return None
    return prices_of_the_period['compensation']


async def period(current_datetime: datetime.datetime) -> str:
    timezone_datetime = await _madrid_time(current_datetime)
    if is_tariff_holiday(timezone_datetime):
        return "P3"
    weekday = timezone_datetime.isoweekday()
    if weekday == 6 or weekday == 7:
        return "P3"
    hour = timezone_datetime.hour
    if 0 <= hour < 8:
        return "P3"
    elif 8 <= hour < 10 or 14 <= hour < 18 or 22 <= hour < 24:
        return "P2"
    else:
        return "P1"
