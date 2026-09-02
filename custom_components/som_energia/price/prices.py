from asyncio import get_running_loop
from collections.abc import Mapping
import csv
from dataclasses import dataclass
import datetime
import os

from homeassistant.exceptions import HomeAssistantError
from homeassistant.util.dt import async_get_time_zone

from custom_components.som_energia.price.tariff_holiday import is_tariff_holiday
from custom_components.som_energia.price.zone import PENINSULA, ZONE_TIME_ZONES

# Mapping typing, not dict, so mypy rejects any mutation: the parsed table is shared by
# every caller for the life of the process.
PriceTable = Mapping[tuple[datetime.date, datetime.date], Mapping[str, float]]

# Parsed once per process. prices.csv ships inside the integration and only changes on
# upgrade, which restarts Home Assistant, so there is nothing to invalidate.
_price_table: PriceTable | None = None


@dataclass(frozen=True, slots=True)
class PriceSnapshot:
    """Everything the integration publishes, all read off a single instant.

    Computing the four values together is what makes them consistent: they share one
    time zone conversion and one table row, so an update that lands on a period
    boundary can no longer publish the period of P2 next to the price of P1.
    """

    period: str
    price: float | None
    price_generation_kwh: float | None
    compensation: float | None


def _read_price_csv() -> PriceTable:
    """Parse prices.csv. Blocking; only reachable through _get_price_table."""
    file_path = os.path.join(os.path.dirname(__file__), "prices.csv")
    prices_data: dict[tuple[datetime.date, datetime.date], Mapping[str, float]] = {}
    # Explicit encoding: the header carries "Compensación", so a C/POSIX locale would
    # otherwise resolve to ASCII and raise UnicodeDecodeError. newline="" is what the
    # csv module documents for its readers.
    with open(file_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            period_bounds = (
                datetime.datetime.strptime(row["Inicio Periodo"], "%Y-%m-%d").date(),
                datetime.datetime.strptime(row["Final Periodo"], "%Y-%m-%d").date(),
            )
            prices_data[period_bounds] = {
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

    No lock: the coordinator's first refresh warms this during setup, before any sensor
    exists, and two cold callers racing would only parse the same immutable table twice.
    """
    global _price_table
    if _price_table is None:
        _price_table = await get_running_loop().run_in_executor(None, _read_price_csv)
    return _price_table


async def _local_time(current_datetime: datetime.datetime, zone: str) -> datetime.datetime:
    """Convert to the zone's local time, which is what every tariff rule is defined in.

    Península and Baleares keep peninsular time; Canarias is an hour behind, and the
    tariff hours there are counted against the Canarian clock, so the conversion is the
    whole of what makes that zone different.
    """
    time_zone = ZONE_TIME_ZONES[zone]
    tz = await async_get_time_zone(time_zone)
    if tz is None:
        # astimezone(None) would silently fall back to the host's local time and
        # serve the prices of the wrong hours, so refuse instead.
        raise HomeAssistantError(f"Time zone {time_zone} is not available")
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


def _period_of(timezone_datetime: datetime.datetime) -> str:
    """The tariff period of an already converted Spanish local time."""
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


def _price_for_period(
    prices_of_the_period: Mapping[str, float],
    current_period: str,
    valle: str,
    llano: str,
    punta: str,
) -> float:
    if current_period == "P1":
        return prices_of_the_period[punta]
    elif current_period == "P2":
        return prices_of_the_period[llano]
    else:
        return prices_of_the_period[valle]


async def current_prices(current_datetime: datetime.datetime, zone: str) -> PriceSnapshot:
    """Compute the whole snapshot from one instant: one conversion, one table scan.

    The zone is required rather than defaulted: this is what the coordinator calls, and
    a zone that defaulted itself would publish peninsular hours to a Canarian
    installation with nothing to show for it. The wrappers below default because they
    are the price API, not the path the sensors take.
    """
    timezone_datetime = await _local_time(current_datetime, zone)
    current_period = _period_of(timezone_datetime)
    prices_of_the_period = await _prices_for_current_period(timezone_datetime)
    if prices_of_the_period is None:
        # Outside every row of prices.csv. The period is still known — it is a function
        # of the clock alone — but there is no price to publish for it.
        return PriceSnapshot(
            period=current_period,
            price=None,
            price_generation_kwh=None,
            compensation=None,
        )
    return PriceSnapshot(
        period=current_period,
        price=_price_for_period(
            prices_of_the_period, current_period, 'valle', 'llano', 'punta'),
        price_generation_kwh=_price_for_period(
            prices_of_the_period, current_period,
            'valle_generation_kwh', 'llano_generation_kwh', 'punta_generation_kwh'),
        compensation=prices_of_the_period['compensation'],
    )


async def price(current_datetime: datetime.datetime, zone: str = PENINSULA) -> float | None:
    return (await current_prices(current_datetime, zone)).price


async def price_generation_kwh(current_datetime: datetime.datetime, zone: str = PENINSULA) -> float | None:
    return (await current_prices(current_datetime, zone)).price_generation_kwh


async def compensation(current_datetime: datetime.datetime, zone: str = PENINSULA) -> float | None:
    return (await current_prices(current_datetime, zone)).compensation


async def period(current_datetime: datetime.datetime, zone: str = PENINSULA) -> str:
    # Not routed through current_prices: the period needs no price row, and asking for
    # one would make the cheapest sensor pay for a table scan it does not use.
    return _period_of(await _local_time(current_datetime, zone))
