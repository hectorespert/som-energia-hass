import datetime as datetime

from pytz import timezone

holidays = [
    '2023-01-06',
    '2023-04-07',
    '2023-05-01',
    '2023-08-15',
    '2023-10-12',
    '2023-11-01',
    '2022-12-30',
    '2023-12-08',
    '2023-12-25'
]

prices = {
    "punta": 0.415889,
    "llano": 0.341710,
    "valle": 0.284556
}


def price(current_datetime: datetime) -> float:
    timezone_datetime = current_datetime.astimezone(timezone('Europe/Madrid'))
    date = timezone_datetime.strftime("%Y-%m-%d")
    if date in holidays:
        return prices['valle']
    weekday = timezone_datetime.isoweekday()
    if weekday == 6 or weekday == 7:
        return prices['valle']
    hour = timezone_datetime.hour
    if 0 <= hour < 8:
        return prices['valle']
    elif 8 <= hour < 10 or 14 <= hour < 18 or 22 <= hour < 24:
        return prices['llano']
    else:
        return prices['punta']
