# Copilot instructions

A Home Assistant custom integration (HACS-distributed) that exposes Som Energia
electricity tariff data as sensors. It has **no network I/O and no API client**: every
price is baked into `custom_components/som_energia/price/prices.csv`, so `iot_class` is
`calculated` and sensor values are pure functions of the current time.

The full development guide lives in `AGENTS.md`. Copilot code review does not read that
file, which is why the review-critical parts are repeated here.

## Reviewing changes to `prices.csv`

Rows are keyed by `(Inicio Periodo, Final Periodo)` and the **first matching row wins**,
so the table must stay:

- in chronological order,
- free of overlapping ranges,
- **free of gaps.** A date matching no row returns `None` and the sensors go `unknown`.
  Check the whole file, not only the diff — a gap is invisible in a diff that adds rows
  somewhere else.

Exactly one row may be open-ended, and it must end at `2999-12-31`. Adding a new price
period means closing that row with a real end date and adding a new `2999-12-31` one.
Empty cells parse as `0.0`.

Prices are the *sin impuestos* figures published by Som Energia, for both the periodos
tariff and Generation kWh. The published history is at
<https://www.somenergia.coop/es/historico-tarifa-periodos>.

Every new price row needs a matching `test_price_on_<period>` case. Dates used in price
tests must be real non-holiday weekdays — otherwise the period logic changes the expected
value and the test asserts the wrong thing while still passing.

## Repository invariants

- `manifest.json` `version` is CalVer (`YYYY.M.D`). The release workflow reads it and the
  BlueSky announcement posts it, so it must be bumped in the same commit as the change
  being released.
- `manifest.json` must stay at the root of `custom_components/som_energia`: the release
  ZIP takes that directory's **contents**, and `verify-zip.yml` fails the build otherwise.
- `price/tariff_holiday.py` holds a frozen set of nine fixed `(month, day)` tariff
  holidays and **deliberately excludes Good Friday and Maundy Thursday**. CNMC Circular
  3/2020 art. 7.3 excludes holidays that are substitutable or have no fixed date, so the
  tariff calendar is a closed list. Do not flag this as a bug, suggest "fixing" it, or
  propose a holiday package.
- Home Assistant forbids blocking calls in the event loop. Reading the CSV goes through
  `run_in_executor`, and timezone lookups use
  `homeassistant.util.dt.async_get_time_zone` rather than `ZoneInfo(...)`. Flag any new
  file, network or heavy-CPU work placed directly on the loop.
- The CSV is parsed once into the module-level `_price_table` and shared from there. Do
  not suggest dropping the `run_in_executor` now that the read happens once — HA patches
  `builtins.open` and warns for any read on the loop, including the first. Do not suggest
  re-typing the shared table as `dict`: `Mapping` is what makes mypy reject mutation of an
  object every caller holds.
- The four sensors are `CoordinatorEntity` subclasses that only pick a field out of
  `coordinator.data`; the values are computed once per tick by `SomEnergiaCoordinator`
  from a single `utcnow()`. Do not suggest giving the sensors `async_update` or a
  `SCAN_INTERVAL` back, and do not suggest that any of them read the clock: that single
  reading is what stops a tick on a period boundary from publishing the period of P2
  next to the price of P1. The shared availability that comes with it, and the
  `UpdateFailed` wrapping in `_async_update_data`, are deliberate too.
- That helper must come from `homeassistant.util.dt`, never from `aiozoneinfo` directly:
  the package is an undeclared internal HA dependency. Flag any reintroduced
  `from aiozoneinfo import ...`. Its `None` return is handled once, in `_local_time`;
  do not suggest dropping that guard as dead code, since `astimezone(None)` would
  silently serve prices in the host's timezone rather than the zone's.
- `price/zone.py` maps the three supply zones to a time zone and **nothing else**. The
  periodos tariff is priced once for the whole state, so do not suggest per-zone price
  rows or a `Zona` column in `prices.csv`; zone-dependent pricing belongs to the
  *indexada* tariff, which this integration does not model. Baleares maps to
  `Europe/Madrid` on purpose and is therefore identical to Península — that is not a
  copy-paste bug. Ceuta y Melilla is absent because Som Energia does not supply there;
  it is also the only zone whose tariff *hours* differ, which is why `_period_of` takes
  no zone.
- The zone values stored on the config entry (`peninsula`, `baleares`, `canarias`) and
  the `zone` key itself are persisted, so they must never be renamed. Config flow
  `VERSION` is 2; `async_migrate_entry` stamps version 1 entries as peninsular, and the
  coordinator then reads `entry.data[CONF_ZONE]` outright rather than defaulting — do
  not suggest a `.get(..., PENINSULA)` fallback there, which would mask a failed
  migration by quietly serving peninsular hours.
- Adding a translatable string means editing `strings.json` **and** both
  `translations/en.json` and `translations/es.json`.
- The README is bilingual, Spanish first and then English; both sections must stay in sync.

## Tests

`pytest.ini` sets `asyncio_mode = auto`, so tests are `async def` with no
`@pytest.mark.asyncio`. It sets no addopts, so coverage flags must be passed explicitly;
`setup.cfg` holds only the `[coverage:*]` sections.

Entries under `[coverage:report] exclude_lines` are regexes matched as substrings, and
coverage drops the entire clause under a match. Flag any added pattern that names code and
is not anchored — one of them previously hid the whole config flow while the total still
reported 100%. `pragma: no cover` is deliberately unanchored; it is a trailing marker.

Price and period tests are written as explicit datetime → expected-value assertions.
Follow that style rather than introducing parametrisation.

## Before reporting a finding

`TODO.md` is the ledger of audit findings, one line each with a link to the pull request
that fixed it. Nothing is open there right now, so a finding that matches a row in that
table has already been dealt with — check it before flagging something as new.
