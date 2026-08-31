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
- `price/tariff_holiday.py` **deliberately excludes Good Friday** ("Viernes Santo"). It is
  a Spanish national holiday but not a tariff holiday. Do not flag this as a bug or
  suggest "fixing" it.
- Home Assistant forbids blocking calls in the event loop. Reading the CSV and building
  the `holidays` object both go through `run_in_executor`, and timezone lookups use
  `aiozoneinfo.async_get_time_zone` rather than `ZoneInfo(...)`. Flag any new file,
  network or heavy-CPU work placed directly on the loop.
- Adding a translatable string means editing `strings.json` **and** both
  `translations/en.json` and `translations/es.json`.
- The README is bilingual, Spanish first and then English; both sections must stay in sync.

## Tests

`pytest.ini` sets `asyncio_mode = auto`, so tests are `async def` with no
`@pytest.mark.asyncio`. `pytest.ini` also takes precedence over the `[tool:pytest]`
section in `setup.cfg`, so that section's `--strict` and `--cov` addopts never apply and
coverage flags must be passed explicitly.

Price and period tests are written as explicit datetime → expected-value assertions.
Follow that style rather than introducing parametrisation.

## Before reporting a finding

`TODO.md` tracks the known open defects, deprecations and supply-chain risks, ranked.
Check it before flagging something as new — several known issues are deliberate or already
scheduled, and one of them explains why the reported coverage percentage is not
trustworthy.
