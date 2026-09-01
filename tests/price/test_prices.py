from datetime import datetime
import os
import pathlib
import subprocess
import sys
import threading
from unittest.mock import patch
from zoneinfo import ZoneInfo

from homeassistant.exceptions import HomeAssistantError
import pytest

from custom_components.som_energia.price import compensation, price, prices
from custom_components.som_energia.price.prices import period, price_generation_kwh


async def test_price_on_monday():
    monday = datetime(2022, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.228

    monday = datetime(2022, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.286

    monday = datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.396

    monday = datetime(2022, 1, 24, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.286

    monday = datetime(2022, 1, 24, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.396

    monday = datetime(2022, 1, 24, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.286


async def test_price_on_2022_02():
    monday = datetime(2022, 2, 28, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.262

    monday = datetime(2022, 2, 28, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.320

    monday = datetime(2022, 2, 28, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.407


async def test_price_on_2022_04():
    monday = datetime(2022, 4, 4, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.261

    monday = datetime(2022, 4, 4, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.315

    monday = datetime(2022, 4, 4, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.380


async def test_price_on_2022_06():
    monday = datetime(2022, 6, 6, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.241

    monday = datetime(2022, 6, 6, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.293

    monday = datetime(2022, 6, 6, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.357


async def test_price_on_2022_10():
    monday = datetime(2022, 10, 3, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.234

    monday = datetime(2022, 10, 3, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.281

    monday = datetime(2022, 10, 3, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.343


async def test_price_on_2024():
    monday = datetime(2024, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.154

    monday = datetime(2024, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.189

    monday = datetime(2024, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.247

    monday = datetime(2024, 1, 24, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.189

    monday = datetime(2024, 1, 24, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.247

    monday = datetime(2024, 1, 24, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.189


async def test_price_on_2026():
    monday = datetime(2026, 1, 26, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.125

    monday = datetime(2026, 1, 26, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.153

    monday = datetime(2026, 1, 26, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.229

    monday = datetime(2026, 1, 26, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.153

    monday = datetime(2026, 1, 26, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.229

    monday = datetime(2026, 1, 26, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.153


async def test_price_on_2026_05():
    monday = datetime(2026, 5, 4, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.124

    monday = datetime(2026, 5, 4, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.150

    monday = datetime(2026, 5, 4, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.226

    monday = datetime(2026, 5, 4, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.150

    monday = datetime(2026, 5, 4, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.226

    monday = datetime(2026, 5, 4, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.150


async def test_price_on_2026_10():
    monday = datetime(2026, 10, 5, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.150

    monday = datetime(2026, 10, 5, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.169

    monday = datetime(2026, 10, 5, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.249

    monday = datetime(2026, 10, 5, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.169

    monday = datetime(2026, 10, 5, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.249

    monday = datetime(2026, 10, 5, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(monday) == 0.169


async def test_price_on_sunday():
    sunday = datetime(2022, 1, 23, 16, 57, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(sunday) == 0.228


async def test_price_on_2023():
    sunday = datetime(2023, 12, 23, 12, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(sunday) == 0.199


async def test_price_on_holiday():
    holiday = datetime(2023, 1, 6, 16, 57, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(holiday) == 0.234


async def test_compensation():
    day = datetime(2023, 12, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await compensation(day) == 0.130


async def test_compensation_2024():
    day = datetime(2024, 1, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await compensation(day) == 0.070


async def test_compensation_2026():
    day = datetime(2026, 1, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await compensation(day) == 0.030


async def test_compensation_2026_10():
    day = datetime(2026, 10, 5, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await compensation(day) == 0.030


async def test_price_generation_kwh():
    monday = datetime(2024, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.116

    monday = datetime(2024, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.139

    monday = datetime(2024, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.187

    monday = datetime(2024, 1, 24, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.139

    monday = datetime(2024, 1, 24, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.187

    monday = datetime(2024, 1, 24, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.139


async def test_price_generation_kwh_2022():
    monday = datetime(2022, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.105

    monday = datetime(2022, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.137

    monday = datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.236


async def test_price_generation_kwh_2022_02():
    monday = datetime(2022, 2, 28, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.110

    monday = datetime(2022, 2, 28, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.137

    monday = datetime(2022, 2, 28, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.209


async def test_price_generation_kwh_2022_04():
    monday = datetime(2022, 4, 4, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.109

    monday = datetime(2022, 4, 4, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.132

    monday = datetime(2022, 4, 4, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.183


async def test_price_generation_kwh_2022_06():
    monday = datetime(2022, 6, 6, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.096

    monday = datetime(2022, 6, 6, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.120

    monday = datetime(2022, 6, 6, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.170


async def test_price_generation_kwh_2022_10():
    # Punta and llano match the June row; only valle tells the two periods apart.
    monday = datetime(2022, 10, 3, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.095

    monday = datetime(2022, 10, 3, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.120

    monday = datetime(2022, 10, 3, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.170


async def test_price_generation_kwh_2023():
    monday = datetime(2023, 1, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.111

    monday = datetime(2023, 1, 23, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.135

    monday = datetime(2023, 1, 23, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.183

    monday = datetime(2023, 5, 22, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.126

    monday = datetime(2023, 5, 22, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.150

    monday = datetime(2023, 5, 22, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.197


async def test_price_generation_kwh_2026():
    monday = datetime(2026, 1, 26, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.110

    monday = datetime(2026, 1, 26, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.135

    monday = datetime(2026, 1, 26, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.205

    monday = datetime(2026, 1, 26, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.135

    monday = datetime(2026, 1, 26, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.205

    monday = datetime(2026, 1, 26, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.135


async def test_price_generation_kwh_2026_05():
    monday = datetime(2026, 5, 4, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.099

    monday = datetime(2026, 5, 4, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

    monday = datetime(2026, 5, 4, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.194

    monday = datetime(2026, 5, 4, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

    monday = datetime(2026, 5, 4, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.194

    monday = datetime(2026, 5, 4, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124


async def test_price_generation_kwh_2026_10():
    monday = datetime(2026, 10, 5, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.099

    monday = datetime(2026, 10, 5, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

    monday = datetime(2026, 10, 5, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.194

    monday = datetime(2026, 10, 5, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124

    monday = datetime(2026, 10, 5, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.194

    monday = datetime(2026, 10, 5, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price_generation_kwh(monday) == 0.124


async def test_price_before_the_first_price_period():
    before = datetime(2019, 6, 12, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(before) is None
    assert await price_generation_kwh(before) is None
    assert await compensation(before) is None

    before = datetime(2021, 12, 31, 23, 59, 59, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(before) is None
    assert await price_generation_kwh(before) is None
    assert await compensation(before) is None


async def test_price_on_the_first_second_of_the_first_price_period():
    first = datetime(2022, 1, 1, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(first) == 0.228
    assert await compensation(first) == 0.000


async def test_period_on_weekday_valle():
    monday = datetime(2022, 1, 24, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P3"

    monday = datetime(2022, 1, 24, 4, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P3"

    monday = datetime(2022, 1, 24, 7, 59, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P3"


async def test_period_on_weekday_llano():
    monday = datetime(2022, 1, 24, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 9, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 14, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 16, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 22, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"

    monday = datetime(2022, 1, 24, 23, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P2"


async def test_period_on_weekday_punta():
    monday = datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 13, 59, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 18, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 20, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"

    monday = datetime(2022, 1, 24, 21, 59, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(monday) == "P1"


async def test_period_on_weekend():
    saturday = datetime(2022, 1, 22, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(saturday) == "P3"

    sunday = datetime(2022, 1, 23, 16, 57, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(sunday) == "P3"

    sunday = datetime(2022, 1, 23, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(sunday) == "P3"


async def test_period_on_holiday():
    holiday = datetime(2023, 1, 6, 16, 57, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(holiday) == "P3"

    holiday = datetime(2023, 1, 6, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(holiday) == "P3"

    holiday = datetime(2023, 12, 25, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await period(holiday) == "P3"


async def test_price_with_utc_timezone():
    monday_utc = datetime(2022, 1, 24, 7, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await price(monday_utc) == 0.286

    monday_utc = datetime(2022, 1, 24, 9, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await price(monday_utc) == 0.396

    monday_utc = datetime(2022, 1, 24, 17, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await price(monday_utc) == 0.396


async def test_period_with_utc_timezone():
    monday_utc = datetime(2022, 1, 23, 23, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await period(monday_utc) == "P3"

    monday_utc = datetime(2022, 1, 24, 7, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await period(monday_utc) == "P2"

    monday_utc = datetime(2022, 1, 24, 9, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await period(monday_utc) == "P1"

    monday_utc = datetime(2022, 1, 24, 13, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert await period(monday_utc) == "P2"


async def test_price_refuses_when_the_time_zone_is_unavailable():
    # HA's async_get_time_zone returns None instead of raising when tzdata cannot
    # resolve the name. Falling through would call astimezone(None), which silently
    # converts to the host's local time and serves the prices of the wrong hours.
    monday = datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    with patch(
        "custom_components.som_energia.price.prices.async_get_time_zone",
        return_value=None,
    ):
        with pytest.raises(HomeAssistantError):
            await price(monday)


async def test_the_price_csv_is_parsed_once_for_many_lookups():
    """prices.csv ships inside the integration and cannot change while Home Assistant
    is running, so re-reading it on every sensor update is pure waste. Four sensors on
    a one-minute SCAN_INTERVAL used to mean 4320 reads a day."""
    monday = datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    reads = 0
    real_read = prices._read_price_csv

    def counting_read():
        nonlocal reads
        reads += 1
        return real_read()

    with patch(
        "custom_components.som_energia.price.prices._read_price_csv",
        new=counting_read,
    ):
        for _ in range(5):
            assert await price(monday) == 0.396
            assert await price_generation_kwh(monday) == 0.236
            assert await compensation(monday) == 0.000
            assert await period(monday) == "P1"

    assert reads == 1
    assert await prices._get_price_table() is await prices._get_price_table()


async def test_the_price_csv_is_never_parsed_on_the_event_loop():
    """Home Assistant patches builtins.open and logs a blocking-call warning for any
    read on the event loop. The warning is non-strict and skipped under tests, so
    nothing else here would catch the read drifting out of the executor. The one read
    now happens inside the coordinator's first refresh, during setup."""
    loop_thread = threading.current_thread()
    parsing_threads = []
    real_read = prices._read_price_csv

    def recording_read():
        parsing_threads.append(threading.current_thread())
        return real_read()

    with patch(
        "custom_components.som_energia.price.prices._read_price_csv",
        new=recording_read,
    ):
        await prices._get_price_table()

    assert parsing_threads
    assert loop_thread not in parsing_threads


async def test_price_period_bounds_include_the_whole_last_day():
    """Rows are matched by date now, not by rebuilt 00:00:00 -> 23:59:59.999999
    datetime bounds; the last microsecond of a row must still belong to it."""
    last = datetime(2025, 5, 31, 23, 59, 59, 999999, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(last) == 0.127

    first = datetime(2025, 6, 1, 0, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    assert await price(first) == 0.119


def test_the_price_csv_is_read_as_utf8_regardless_of_the_locale():
    """The header carries "Compensación". With no explicit encoding, open() resolves one
    from the locale, and a C/POSIX locale resolves to ASCII:

        UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 39

    The table is parsed during async_setup_entry, so that would take the whole config
    entry down rather than one sensor update. The locale is fixed per process and cannot
    be patched in, hence the subprocess.
    """
    repo_root = pathlib.Path(__file__).parents[2]
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from custom_components.som_energia.price.prices import _read_price_csv;"
            "print(len(_read_price_csv()))",
        ],
        capture_output=True,
        text=True,
        cwd=repo_root,
        env={**os.environ, "LC_ALL": "C", "LANG": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"},
    )

    assert result.returncode == 0, result.stderr
    assert int(result.stdout.strip()) > 0


async def test_current_prices_is_one_time_zone_conversion_and_one_table_scan():
    """A tick across the four sensors used to cost 6 time zone conversions and 3 table
    scans, because every function converted and scanned for itself — price and
    price_generation_kwh each called period internally, converting a second time."""
    monday = datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    counts = {"tz": 0, "scan": 0}
    real_madrid_time = prices._madrid_time
    real_prices_for_current_period = prices._prices_for_current_period

    async def counting_madrid_time(current_datetime):
        counts["tz"] += 1
        return await real_madrid_time(current_datetime)

    async def counting_prices_for_current_period(timezone_datetime):
        counts["scan"] += 1
        return await real_prices_for_current_period(timezone_datetime)

    with patch(
        "custom_components.som_energia.price.prices._madrid_time",
        new=counting_madrid_time,
    ), patch(
        "custom_components.som_energia.price.prices._prices_for_current_period",
        new=counting_prices_for_current_period,
    ):
        snapshot = await prices.current_prices(monday)

    assert counts == {"tz": 1, "scan": 1}
    assert snapshot == prices.PriceSnapshot(
        period="P1",
        price=0.396,
        price_generation_kwh=0.236,
        compensation=0.000,
    )


async def test_current_prices_outside_every_price_period():
    """The period is a function of the clock alone, so it is still known when no row of
    prices.csv covers the date; the three prices are not."""
    before = datetime(2019, 6, 12, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))

    assert await prices.current_prices(before) == prices.PriceSnapshot(
        period="P1",
        price=None,
        price_generation_kwh=None,
        compensation=None,
    )


async def test_the_individual_functions_agree_with_the_snapshot():
    """price, price_generation_kwh and compensation are wrappers over current_prices
    now. Nothing may drift between what they return and what the sensors publish."""
    moments = [
        datetime(2022, 1, 24, 10, 0, 0, tzinfo=ZoneInfo("Europe/Madrid")),  # P1
        datetime(2026, 1, 5, 9, 0, 0, tzinfo=ZoneInfo("Europe/Madrid")),    # P2
        datetime(2026, 1, 5, 3, 0, 0, tzinfo=ZoneInfo("Europe/Madrid")),    # P3, valle
        datetime(2026, 1, 6, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid")),   # P3, holiday
        datetime(2026, 10, 3, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid")),  # P3, weekend
        datetime(2019, 6, 12, 12, 0, 0, tzinfo=ZoneInfo("Europe/Madrid")),  # no prices
    ]

    for moment in moments:
        snapshot = await prices.current_prices(moment)
        assert await price(moment) == snapshot.price
        assert await price_generation_kwh(moment) == snapshot.price_generation_kwh
        assert await compensation(moment) == snapshot.compensation
        assert await period(moment) == snapshot.period
