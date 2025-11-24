from datetime import datetime
from holidays import country_holidays

def is_tariff_holiday(timezone_datetime: datetime) -> bool:
    holidays_in_spain = country_holidays(country="ES", years=timezone_datetime.year, language="es")
    holiday_name = holidays_in_spain.get(timezone_datetime.date())
    return holiday_name and holiday_name != "Viernes Santo"
