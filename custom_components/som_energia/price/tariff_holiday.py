from datetime import datetime
from holidays import country_holidays

def is_tariff_holiday(timezone_datetime: datetime) -> bool:
    """Check if the given datetime is a tariff holiday in Spain.

    Returns True for Spanish holidays except Good Friday (Viernes Santo),
    as Good Friday is not considered a tariff holiday for pricing purposes.
    """
    holidays_in_spain = country_holidays(country="ES", years=timezone_datetime.year, language="es")
    holiday_name = holidays_in_spain.get(timezone_datetime.date())
    return holiday_name is not None and holiday_name != "Viernes Santo"
