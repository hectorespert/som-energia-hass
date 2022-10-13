import datetime as datetime

from pytz import timezone


def price(current_datetime: datetime) -> float:
    timezone_datetime = current_datetime.astimezone(timezone('Europe/Madrid'))
    weekday = timezone_datetime.isoweekday()
    if weekday == 6 or weekday == 7:
        return 0.284556
    hour = timezone_datetime.hour
    if 0 <= hour < 8:
        return 0.284556
    elif 8 <= hour < 10 or 14 <= hour < 18 or 22 <= hour < 24:
        return 0.341710
    else:
        return 0.417105
