from datetime import datetime
from zoneinfo import ZoneInfo
import pytest

from custom_components.som_energia.price.tariff_holiday import is_tariff_holiday


HOLIDAYS = [
    '2023-01-06',
    '2023-05-01',
    '2023-08-15',
    '2023-10-12',
    '2023-11-01',
    '2023-12-08',
    '2023-12-25',
    '2024-01-01',
    '2024-05-01',
    '2024-08-15',
    '2024-11-01',
    '2024-12-06',
    '2024-12-25',
    '2025-01-01',
    '2025-05-01',
    '2025-08-15',
    '2025-11-01',
    '2025-12-06',
    '2025-12-08',
    '2025-12-25',
    '2026-05-01',
    '2026-08-15',
    '2026-10-12',
    '2026-12-08',
    '2026-12-25',
]


@pytest.mark.parametrize("date_str", HOLIDAYS)
async def test_is_tariff_holiday_true(date_str: str):
    dt = datetime.strptime(date_str + ' 12:00:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo("Europe/Madrid"))
    assert await is_tariff_holiday(dt), f"Should be a holiday: {date_str}"


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
async def test_is_tariff_holiday_false(date_str: str):
    dt = datetime.strptime(date_str + ' 12:00:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo("Europe/Madrid"))
    assert not await is_tariff_holiday(dt), f"Should not be a holiday: {date_str}"


@pytest.mark.parametrize("date_str", ['2023-04-07', '2025-04-18', '2026-04-03'])
async def test_is_tariff_holiday_excluded_good_friday(date_str: str):
    dt = datetime.strptime(date_str + ' 12:00:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo("Europe/Madrid"))
    assert not await is_tariff_holiday(dt), "Good Friday should not be considered a tariff holiday"
