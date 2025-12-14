from asyncio import get_running_loop
from datetime import datetime
from holidays import country_holidays, HolidayBase


def _holidays_in_spain(year: int) -> HolidayBase:
    """Get Spanish holidays for a specific year."""
    return country_holidays(country="ES", years=year, language="es")


async def is_tariff_holiday(timezone_datetime: datetime) -> bool:
    """Check if the given datetime is a tariff holiday in Spain.

    Returns True for Spanish holidays except Good Friday (Viernes Santo),
    as Good Friday is not considered a tariff holiday for pricing purposes.
    """
    holidays_in_spain = await get_running_loop().run_in_executor(None, _holidays_in_spain, timezone_datetime.year)
    holiday_name = holidays_in_spain.get(timezone_datetime.date())
    return holiday_name is not None and holiday_name != "Viernes Santo"
