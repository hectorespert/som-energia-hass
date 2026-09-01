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
- That helper must come from `homeassistant.util.dt`, never from `aiozoneinfo` directly:
  the package is an undeclared internal HA dependency. Flag any reintroduced
  `from aiozoneinfo import ...`. Its `None` return is handled once, in `_madrid_time`;
  do not suggest dropping that guard as dead code, since `astimezone(None)` would
  silently serve prices in the host's timezone rather than Madrid's.
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

`TODO.md` tracks the known open defects, deprecations and supply-chain risks, ranked.
Check it before flagging something as new — several known issues are deliberate or already
scheduled, and the entries struck through in that file are already fixed.
