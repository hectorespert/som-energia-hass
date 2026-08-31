# AGENTS.md

Guidance for AI coding agents (Claude Code, Copilot, Codex, …) working in this repository.

## Known issues

[TODO.md](TODO.md) tracks the open defects, deprecations and supply-chain risks in this
codebase, ranked. Read it before trusting anything here: it documents, among others, a
coverage-config bug that makes the reported 100% coverage false, and a price-lookup
fallback that silently returns the wrong row.

## What this is

A **Home Assistant custom integration** (HACS-distributed) that exposes Som Energia
electricity tariff data as sensors. It has **no network I/O and no API client**: all
prices are baked into a CSV shipped with the integration, so `iot_class` is
`calculated`. Sensor values are pure functions of the current time.

## Commands

```bash
pip install -r requirements-test.txt   # install test deps (also the devcontainer postCreate step)

pytest                                 # full suite
pytest tests/price/test_prices.py      # one file
pytest tests/price/test_prices.py::test_price_on_2026   # one test
pytest -k "holiday"                    # by name
pytest --cov=custom_components --cov-report=term-missing
```

CI (`.github/workflows/python.yaml`) runs on Python 3.12; the devcontainer image is
3.13. There is no linter or formatter wired into CI — `setup.cfg` carries flake8 /
isort / mypy settings that nothing currently invokes.

Run a real Home Assistant against the integration with the devcontainer
(`.devcontainer/docker-compose.yml`): it mounts `custom_components/som_energia`
read-only into a `homeassistant` container on port 8123. The README's bare
`docker compose up -d` only works from inside `.devcontainer/`.

### Config gotcha

Both `pytest.ini` and a `[tool:pytest]` section in `setup.cfg` exist. **`pytest.ini`
wins**, so the `--strict` and `--cov=custom_components` addopts in `setup.cfg` are
dead config — pass coverage flags explicitly. `pytest.ini` only sets
`asyncio_mode = auto`, which is why tests are `async def` with no `@pytest.mark.asyncio`.

## Architecture

```
custom_components/som_energia/
  __init__.py        setup/unload entry, forwards to PLATFORMS
  const.py           DOMAIN, PLATFORMS
  config_flow.py     single-step, no user input, fixed unique_id
  sensor.py          4 SensorEntity classes, SCAN_INTERVAL 1 min
  price/
    prices.py        period + price calculation (the actual domain logic)
    tariff_holiday.py  Spanish holiday lookup
    prices.csv       the price table
```

**The whole domain model lives in `price/prices.py`.** Everything flows from
`period(datetime) -> "P1" | "P2" | "P3"`:

- Time is converted to `Europe/Madrid` first — every calculation is in local Spanish
  time regardless of the HA instance's timezone.
- P3 (valle) for weekends, tariff holidays, and 00:00–08:00.
- P2 (llano) for 08–10, 14–18, 22–24. P1 (punta) otherwise.
- `tariff_holiday.is_tariff_holiday` uses the `holidays` package for Spain, but
  **excludes Good Friday** ("Viernes Santo"), which is a national holiday yet not a
  tariff holiday. Don't "fix" this.

`prices.csv` maps date ranges to per-period prices. Row keys are
`(Inicio Periodo, Final Periodo)` and the *first* matching row wins, so rows must stay
in chronological order and must not overlap. The open-ended current row ends at
`2999-12-31` — when adding a new price period, close that row and add a new
`2999-12-31` one. Empty cells parse as `0.0`.

`sensor.py` exposes four sensors, all recomputed every minute from `utcnow()`:
`price`, `price_generation_kwh`, `compensation` (all €/kWh) and `period` (P1/P2/P3).
Sensors hold no coordinator and no shared state; each `async_update` calls the price
functions directly.

### Async discipline

Home Assistant forbids blocking calls in the event loop. Both blocking operations —
reading `prices.csv` and constructing the `holidays` object — are wrapped in
`get_running_loop().run_in_executor(None, ...)`, and timezone lookup uses
`aiozoneinfo.async_get_time_zone` rather than `ZoneInfo(...)`. Keep any new file,
network, or heavy-CPU work off the loop the same way; this pattern exists because of
real "blocking call detected" warnings in HA logs.

## Conventions

- `manifest.json` `version` is CalVer (`YYYY.M.D`). The release workflow reads the
  version from it and the BlueSky announcement posts it, so bump it in the same
  commit as the change being released.
- Adding a translatable string means editing `strings.json` **and** both
  `translations/en.json` and `translations/es.json`.
- Tests import via the full path (`custom_components.som_energia...`), matching
  `known_first_party` in `setup.cfg`. `tests/conftest.py` autouses
  `enable_custom_integrations` from `pytest-homeassistant-custom-component`.
- Price/period tests are written as explicit datetime → expected-value assertions;
  add new price rows to `prices.csv` together with a `test_price_on_<year>` case.
- The ZIP built for releases takes the **contents** of `custom_components/som_energia`,
  so `manifest.json` must stay at the root of that directory — `verify-zip.yml`
  fails the build otherwise.
- README is bilingual (Spanish first, then English); keep both sections in sync.
