import datetime as datetime
import os
import csv

from pytz import timezone

from custom_components.som_energia.price.holidays import holidays

def read_price_csv() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "prices.csv")
    prices_data = {}
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            period = (row["Inicio Periodo"], row["Final Periodo"])
            prices_data[period] = {
                "punta": float(row["Punta"]),
                "llano": float(row["Llano"]),
                "valle": float(row["Valle"]),
                "compensation": float(row["Compensación"])
            }
    return prices_data

def price(current_datetime: datetime) -> float:
    tz = timezone("Europe/Madrid")
    timezone_datetime = current_datetime.astimezone(tz)
    prices_of_the_period = {
        "punta": 0.0,
        "llano": 0.0,
        "valle": 0.0,
    }
    for period, prices_of_the_period in read_price_csv().items():
        prices_period_start = tz.localize(datetime.datetime.strptime(period[0], "%Y-%m-%d"))
        prices_period_end = tz.localize(datetime.datetime.strptime(period[1], "%Y-%m-%d")).replace(hour=23, minute=59, second=59, microsecond=999999)
        if prices_period_start <= timezone_datetime <= prices_period_end:
            prices_of_the_period = prices_of_the_period
            break

    date = timezone_datetime.strftime("%Y-%m-%d")
    if date in holidays:
        return prices_of_the_period['valle']
    weekday = timezone_datetime.isoweekday()
    if weekday == 6 or weekday == 7:
        return prices_of_the_period['valle']
    hour = timezone_datetime.hour
    if 0 <= hour < 8:
        return prices_of_the_period['valle']
    elif 8 <= hour < 10 or 14 <= hour < 18 or 22 <= hour < 24:
        return prices_of_the_period['llano']
    else:
        return prices_of_the_period['punta']


def compensation(current_datetime: datetime) -> float:
    tz = timezone("Europe/Madrid")
    timezone_datetime = current_datetime.astimezone(tz)
    compensation_price = 0
    for period, prices_of_the_period in read_price_csv().items():
        prices_period_start = tz.localize(datetime.datetime.strptime(period[0], "%Y-%m-%d"))
        prices_period_end = tz.localize(datetime.datetime.strptime(period[1], "%Y-%m-%d")).replace(hour=23, minute=59, second=59, microsecond=999999)
        if prices_period_start <= timezone_datetime <= prices_period_end:
            compensation_price = prices_of_the_period['compensation']
            break
    return compensation_price

