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
    '2023-12-25',
    '2024-01-01',
    '2024-05-01',
    '2024-08-15',
    '2024-11-01',
    '2024-12-06',
    '2024-12-25',
]

pricesTable = {
    ("2024-01-01", "2999-12-31"): {
        "punta": 0.247,
        "llano": 0.189,
        "valle": 0.154,
        "compensation": 0.070
    },
    ("2023-05-01", "2023-12-31"): {
        "punta": 0.295,
        "llano": 0.237,
        "valle": 0.199,
        "compensation": 0.130
    },
    ("2023-01-01", "2023-04-30"): {
        "punta": 0.342,
        "llano": 0.281,
        "valle": 0.234,
        "compensation": 0.0
    }
    # TODO: Add 2022 periods
    ,
    ("2022-01-01", "2022-01-31"): {
        "punta": 0.396,
        "llano": 0.286,
        "valle": 0.228,
        "compensation": 0.0
    }

}


def price(current_datetime: datetime) -> float:
    tz = timezone("Europe/Madrid")
    timezone_datetime = current_datetime.astimezone(tz)
    prices = {
        "punta": 0.0,
        "llano": 0.0,
        "valle": 0.0,
    }
    for period, periodPrices in pricesTable.items():
        pricesPeriodStart = tz.localize(datetime.datetime.strptime(period[0], "%Y-%m-%d"))
        pricesPeriodEnd = tz.localize(datetime.datetime.strptime(period[1], "%Y-%m-%d")).replace(hour=23, minute=59, second=59, microsecond=999999)
        if pricesPeriodStart <= timezone_datetime <= pricesPeriodEnd:
            prices = periodPrices
            break

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


def compensation(current_datetime: datetime) -> float:
    tz = timezone("Europe/Madrid")
    timezone_datetime = current_datetime.astimezone(tz)
    price = 0
    for period, periodPrices in pricesTable.items():
        pricesPeriodStart = tz.localize(datetime.datetime.strptime(period[0], "%Y-%m-%d"))
        pricesPeriodEnd = tz.localize(datetime.datetime.strptime(period[1], "%Y-%m-%d")).replace(hour=23, minute=59, second=59, microsecond=999999)
        if pricesPeriodStart <= timezone_datetime <= pricesPeriodEnd:
            price = periodPrices['compensation']
            break
    return price
