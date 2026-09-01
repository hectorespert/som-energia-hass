# TODO

Prioritised backlog for this integration: verified defects first, then supply-chain and
compatibility risks, then deprecations and quality work. See [AGENTS.md](AGENTS.md) for
how the code is meant to work.

Findings were produced by auditing the code against **Home Assistant 2025.11.3** and
running the affected paths — the reproductions below are actual observed output, not
inference. Line references are against `master` at the time of writing.

## Critical — verified defects

### 1. ~~The coverage config hides the entire config flow, and the 100% badge is false~~ — fixed

`setup.cfg` listed `main()` under `[coverage:report] exclude_lines`. Those entries are
**regexes**, so `main()` read as "the substring `main` followed by an empty group" — and it
matched `domain=DOMAIN` in `class SomEnergiaConfigFlow(ConfigFlow, domain=DOMAIN)`. Coverage
excludes by *clause*, so the match took the whole class body with it: every statement in
`async_step_user` was unexecuted, reported as neither covered nor missing, and the total
still read 100% — which is what the Codecov badge reported.

```
                    config_flow.py               TOTAL
before        7 stmts, 0 miss, excluded 14..26     100%   <- false
regex fixed  15 stmts, 5 miss, excluded none        97%   <- honest, 21-26 uncovered
plus tests   15 stmts, 0 miss, excluded none       100%   <- earned
```

That line was the only one in `custom_components` matching any of the four patterns. The
`main()` entry is gone, and `raise NotImplemented()` went with it — malformed (it is
`NotImplementedError`), unanchored, and matching nothing; it is now
`raise NotImplementedError`. `pragma: no cover` stays, because defining `exclude_lines`
*replaces* coverage's default rather than extending it. `tests/test_config_flow.py` covers
the form step, entry creation and the single-instance abort, so the total is back to a
genuine 100% with zero excluded lines.

A second inflator, not part of the original finding: CI ran `pytest --cov=./`, which
overrode `[coverage:run] source = custom_components` and counted the 344 statements of test
code — 100% covered by definition — alongside the integration, reporting 99%. It now runs
`--cov=custom_components`.

### 2. ~~`async_unload_entry` never unloads the sensor platform~~ — fixed

`__init__.py` returned `True` without calling
`hass.config_entries.async_unload_platforms(entry, PLATFORMS)`, leaving
`async_forward_entry_setups` without its counterpart. Home Assistant marked the entry
`NOT_LOADED` while the `EntityPlatform` stayed registered with its four sensors and its
one-minute polling timer.

Reload was the worse half, and the original finding did not record it. `async_reload`
unloads and then sets up again, so the second setup reached a platform that had never been
released:

```
ValueError: Config entry Mock Title (01M1E48BVRG25SXW1NS3NCQECQ)
            for som_energia.sensor has already been setup!
```

`config_entries` logs that and swallows it, leaving the entry marked `LOADED` with the stale
platform still polling. The UI's "Reload" button, `homeassistant.reload_config_entry` and
HACS upgrades all appeared to work and did not.

`async_unload_entry` now returns `async_unload_platforms`. `tests/test_init.py` covers setup,
unload and reload; with the one-line fix reverted, the unload and reload tests both fail
while the setup test still passes. The unused `hass.data.setdefault(DOMAIN, {})` in
`async_setup` went too — nothing ever read or wrote that dict.

### 3. ~~Price lookup silently serves the last CSV row for unmatched dates~~ — fixed

`_prices_for_current_period` used `prices_of_the_period` as both the zero fallback and the
`for` loop variable, so the fallback was destroyed on the first iteration and the no-op
self-assignment `prices_of_the_period = prices_of_the_period` did nothing. When no row
matched, the function returned whatever the last iterated row was — and the loop variable
`period` also shadowed the module-level `period()` function.

The loop now returns the matching row directly and returns `None` when nothing matches;
`price`, `price_generation_kwh` and `compensation` propagate that `None`, so the sensors
report `unknown` instead of a plausible-looking wrong price. Returning `0.0` was rejected
because a `0.00 €/kWh` reading looks like a valid price and would pollute Home Assistant's
long-term statistics.

```
pre-2022  2019-06-12 -> None   (was 0.226 €/kWh, compensation 0.03)
gap date  2022-06-15 -> 0.357  (gap since filled from the official tariff history)
current   2026-10-15 -> 0.249
```

The Feb–Dec 2022 gap that made this reachable has been filled, so no date from 2022-01-01
onwards hits the `None` branch; only genuinely out-of-range dates do.

## Supply chain and compatibility

### 4. Good Friday detection depends on an unpinned localized string

`price/tariff_holiday.py:19` compares the holiday name against the literal
`"Viernes Santo"`, which only exists because line 8 requests `language="es"`. Meanwhile
`manifest.json` declares `"requirements": ["holidays"]` with **no version bound**, so
Home Assistant installs whatever is current at runtime.

If upstream renames or re-localises that entry, `is_tariff_holiday` starts returning
`True` on Good Friday, the period flips to P3, and the reported price is wrong — silently,
with the test suite still green, because the tests assert the *behaviour* rather than the
string.

The versions in play already disagree: unpinned in the manifest, `0.103` in
`requirements-test.txt`, `0.86` in the local virtualenv.

**Fix:** pin a compatible range in `manifest.json`, and identify Good Friday by a
language-independent signal (Easter minus two days) instead of a display name.

### 5. `aiozoneinfo` is imported directly, and the declared HA floor is unverified

`price/prices.py` does `from aiozoneinfo import async_get_time_zone`. That package is an
implementation detail of Home Assistant (`aiozoneinfo==0.2.3` is one of HA's own
dependencies), and it is not declared in `manifest.json` — the integration works only
because HA happens to ship it. HA exposes a supported, caching wrapper:
`homeassistant.util.dt.async_get_time_zone`.

Related: `hacs.json` declares `"homeassistant": "2024.1.0"` as the minimum, but nothing
tests that floor — CI and the devcontainer both run current HA — and `aiozoneinfo`
postdates it. Verify the true minimum and raise the declaration.

## Deprecations

### 6. Outdated config-flow and platform typing

- `config_flow.py` annotates `async_step_user` as returning `FlowResult`, which is now
  the generic base class; config flows should return `ConfigFlowResult`.
- `sensor.py:11,22` uses `AddEntitiesCallback`; the config-entry form is
  `AddConfigEntryEntitiesCallback`.
- `const.py` should use `[Platform.SENSOR]` rather than the bare string `["sensor"]`.

### 7. The unique-id hack predates `single_config_entry`

`config_flow.py` enforces single-instance behaviour by assigning a hardcoded unique id
(`'som_energia_unique'`) and aborting on duplicates. Home Assistant now supports
`"single_config_entry": true` in `manifest.json`, which expresses the same intent
declaratively.

`tests/test_config_flow.py` now covers the form step, entry creation and the
single-instance abort (see item 1), so the switch to `single_config_entry` has a
regression net to land against.

## Quality

### 8. Entity names are hardcoded English, so the translations never apply

All four sensors set `_attr_name` directly (`sensor.py:40,64,88,112`) instead of using
`_attr_has_entity_name` with a `translation_key`. As a result `translations/es.json`
cannot localise any entity name — on an integration whose users are Spanish-speaking and
whose README leads in Spanish.

Three of the four `SensorEntityDescription`s also share `key='electricity_price'`
(lines 42, 66, 90), including the compensation sensor, which is wrong on its own terms
and blocks deriving translation keys from `key`.

### 9. The period sensor should be an enum, and the entities have no device

`ElectricityPeriodSensor` returns one of exactly three values, so it should declare
`SensorDeviceClass.ENUM` with `options=["P1", "P2", "P3"]` — this gives correct UI
handling and validation. None of the entities set `device_info`, so an integration
declaring `integration_type: hub` produces four ungrouped entities.

### 10. No lint or security gate in CI

- `tests/bandit.yaml` exists but no workflow runs bandit.
- `setup.cfg` configures flake8, isort and mypy that nothing invokes.

The dead `[tool:pytest]` section that used to sit in `setup.cfg` — shadowed by
`pytest.ini` — was removed with item 1. `pytest.ini` is now the only pytest config;
`setup.cfg`'s `[coverage:*]` sections remain live.

### 11. The CSV and the holidays table are rebuilt on every sensor update

`_read_price_csv` re-reads and re-parses `prices.csv` from disk on every call, and
`_holidays_in_spain` reconstructs the `holidays` object on every call. Neither result can
change while Home Assistant is running: the CSV ships inside the integration and only
changes on upgrade, which restarts HA anyway.

With four sensors on a one-minute `SCAN_INTERVAL`, measured on Python 3.13:

```
_read_price_csv     0.031 ms x 4320 calls/day = 0.14 s
_holidays_in_spain  0.151 ms x 4320 calls/day = 0.65 s
                                       total    0.79 s CPU/day, 8640 executor round-trips
```

**The CPU cost is not the argument** — 0.79 s/day is negligible, and an earlier revision of
this file deliberately left the item out for exactly that reason. What makes it worth
listing is the ratio: `functools.cache` on both functions is a two-line change that removes
all 4320 file reads and 4320 object constructions per day.

Two caveats for whoever picks this up:

- `@cache` does **not** remove the executor round-trip on its own — `run_in_executor` still
  dispatches to a thread even when the wrapped call returns instantly. Reading the cached
  value directly on the event loop is what removes it, and that is safe once the call is a
  pure in-memory lookup with no I/O.
- `_read_price_csv` currently returns a fresh dict each call. Cached, every caller shares
  one object, so it must not be mutated. Nothing mutates it today, but nothing enforces it
  either.

`_holidays_in_spain` is keyed by year, so its cache stays bounded at one entry per year
queried.
