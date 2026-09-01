from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from custom_components.som_energia.price.tariff_holiday import is_tariff_holiday

HOLIDAYS = [
    # Every tariff year in full. The calendar is a closed list of nine fixed
    # dates (CNMC Circular 3/2020 art. 7.3), so each year carries the same nine
    # regardless of which weekday they land on.
    '2023-01-01',
    '2023-01-06',
    '2023-05-01',
    '2023-08-15',
    '2023-10-12',
    '2023-11-01',
    '2023-12-06',
    '2023-12-08',
    '2023-12-25',
    '2024-01-01',
    '2024-01-06',
    '2024-05-01',
    '2024-08-15',
    '2024-10-12',
    '2024-11-01',
    '2024-12-06',
    '2024-12-08',
    '2024-12-25',
    '2025-01-01',
    '2025-01-06',
    '2025-05-01',
    '2025-08-15',
    '2025-10-12',
    '2025-11-01',
    '2025-12-06',
    '2025-12-08',
    '2025-12-25',
    '2026-01-01',
    '2026-01-06',
    '2026-05-01',
    '2026-08-15',
    '2026-10-12',
    '2026-11-01',
    '2026-12-06',
    '2026-12-08',
    '2026-12-25',
    '2027-01-01',
    '2027-01-06',
    '2027-05-01',
    '2027-08-15',
    '2027-10-12',
    '2027-11-01',
    '2027-12-06',
    '2027-12-08',
    '2027-12-25',
    '2028-01-01',
    '2028-01-06',
    '2028-05-01',
    '2028-08-15',
    '2028-10-12',
    '2028-11-01',
    '2028-12-06',
    '2028-12-08',
    '2028-12-25',
]


@pytest.mark.parametrize("date_str", HOLIDAYS)
def test_is_tariff_holiday_true(date_str: str):
    dt = datetime.strptime(date_str + ' 12:00:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo("Europe/Madrid"))
    assert is_tariff_holiday(dt), f"Should be a holiday: {date_str}"


NON_HOLIDAYS = [
    '2023-01-05',
    '2023-02-14',
    '2023-03-15',
    '2023-07-14',
    '2024-02-29',
    '2024-04-02',
    '2025-07-01',
]


@pytest.mark.parametrize("date_str", NON_HOLIDAYS)
def test_is_tariff_holiday_false(date_str: str):
    dt = datetime.strptime(date_str + ' 12:00:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo("Europe/Madrid"))
    assert not is_tariff_holiday(dt), f"Should not be a holiday: {date_str}"


@pytest.mark.parametrize("date_str", ['2023-04-07', '2025-04-18', '2026-04-03', '2027-03-26', '2028-04-14'])
def test_is_tariff_holiday_excluded_good_friday(date_str: str):
    dt = datetime.strptime(date_str + ' 12:00:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo("Europe/Madrid"))
    assert not is_tariff_holiday(dt), "Good Friday should not be considered a tariff holiday"


@pytest.mark.parametrize("date_str", ['2023-04-06', '2025-04-17', '2026-04-02', '2027-03-25', '2028-04-13'])
def test_is_tariff_holiday_excluded_maundy_thursday(date_str: str):
    dt = datetime.strptime(date_str + ' 12:00:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo("Europe/Madrid"))
    assert not is_tariff_holiday(dt), "Maundy Thursday should not be considered a tariff holiday"
