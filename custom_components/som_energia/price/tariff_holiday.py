from asyncio import get_running_loop
from datetime import datetime
from holidays import country_holidays

async def is_tariff_holiday(timezone_datetime: datetime) -> bool:
    """Check if the given datetime is a tariff holiday in Spain.

    Returns True for Spanish holidays except Good Friday (Viernes Santo),
    as Good Friday is not considered a tariff holiday for pricing purposes.
    """
    def _get_holiday_name():
        holidays_in_spain = country_holidays(country="ES", years=timezone_datetime.year, language="es")
        return holidays_in_spain.get(timezone_datetime.date())
    
    holiday_name = await get_running_loop().run_in_executor(None, _get_holiday_name)
    return holiday_name is not None and holiday_name != "Viernes Santo"
