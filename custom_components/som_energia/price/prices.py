from asyncio import get_running_loop
from collections.abc import Mapping
import csv
import datetime
import os

from homeassistant.exceptions import HomeAssistantError
from homeassistant.util.dt import async_get_time_zone

from custom_components.som_energia.price.tariff_holiday import is_tariff_holiday

TIME_ZONE = "Europe/Madrid"

# Mapping typing, not dict, so mypy rejects any mutation: the parsed table is shared by
# every caller for the life of the process.
PriceTable = Mapping[tuple[datetime.date, datetime.date], Mapping[str, float]]

# Parsed once per process. prices.csv ships inside the integration and only changes on
# upgrade, which restarts Home Assistant, so there is nothing to invalidate.
_price_table: PriceTable | None = None


def _read_price_csv() -> PriceTable:
    """Parse prices.csv. Blocking; only reachable through _get_price_table."""
    file_path = os.path.join(os.path.dirname(__file__), "prices.csv")
    prices_data: dict[tuple[datetime.date, datetime.date], Mapping[str, float]] = {}
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            period = (
                datetime.datetime.strptime(row["Inicio Periodo"], "%Y-%m-%d").date(),
                datetime.datetime.strptime(row["Final Periodo"], "%Y-%m-%d").date(),
            )
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


async def _get_price_table() -> PriceTable:
    """Return the parsed price table, reading prices.csv at most once per process.

    The read stays in the executor even though it happens only once: Home Assistant
    patches builtins.open and logs a blocking-call warning for any read on the event
    loop. Every later call is an in-memory lookup with no thread hop.

    No lock: async_setup_entry warms this before any sensor runs, and two cold callers
    racing would only parse the same immutable table twice.
    """
    global _price_table
    if _price_table is None:
        _price_table = await get_running_loop().run_in_executor(None, _read_price_csv)
    return _price_table


async def async_load_prices() -> None:
    """Warm the price table during setup so no sensor update ever waits on disk."""
    await _get_price_table()


async def _madrid_time(current_datetime: datetime.datetime) -> datetime.datetime:
    """Convert to Spanish local time, which is what every tariff rule is defined in."""
    tz = await async_get_time_zone(TIME_ZONE)
    if tz is None:
        # astimezone(None) would silently fall back to the host's local time and
        # serve the prices of the wrong hours, so refuse instead.
        raise HomeAssistantError(f"Time zone {TIME_ZONE} is not available")
    return current_datetime.astimezone(tz)


async def _prices_for_current_period(timezone_datetime: datetime.datetime) -> Mapping[str, float] | None:
    # Row bounds are whole days in Spanish local time, so comparing dates is the same
    # test as the old 00:00:00 -> 23:59:59.999999 datetime bounds, without rebuilding
    # two aware datetimes per row on every lookup.
    current_date = timezone_datetime.date()
    for (start, end), prices_of_the_period in (await _get_price_table()).items():
        if start <= current_date <= end:
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
