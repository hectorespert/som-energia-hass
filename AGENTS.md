# AGENTS.md

Guidance for AI coding agents (Claude Code, Copilot, Codex, …) working in this repository.

## Known issues

[TODO.md](TODO.md) is the ledger of audit findings. **Nothing is open right now** — the
fifteen entries are all fixed — so it is one line per finding with a link to the pull
request that carries the reasoning. Check it before reporting something as new, and add
new findings there. The invariants that must not regress are in this file and in
`.github/copilot-instructions.md`, not there.

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

CI (`.github/workflows/python.yaml`) and the devcontainer image both run Python 3.13.
**Do not lower the CI Python version.** Home Assistant declares
`requires-python >= 3.13` from 2025.3.0 onwards, so on a 3.12 runner pip cannot install
any newer HA: it backtracks to `pytest-homeassistant-custom-component==0.13.205`, which
pulls `homeassistant==2025.1.4`. CI ran that way for months and looked green while
testing against a January release — the failure only surfaced when a symbol added in
2025.3.0 was used. `.github/workflows/lint.yaml` is a blocking gate running flake8,
isort, bandit and mypy over `custom_components` and `tests` with the `setup.cfg`
settings; there is still no formatter.

Run a real Home Assistant against the integration with the devcontainer
(`.devcontainer/docker-compose.yml`): it mounts `custom_components/som_energia`
read-only into a `homeassistant` container on port 8123. The README's bare
`docker compose up -d` only works from inside `.devcontainer/`.

### Config gotcha

`pytest.ini` is the only pytest config — it sets `asyncio_mode = auto`, which is why tests
are `async def` with no `@pytest.mark.asyncio`. It sets no addopts, so **coverage flags
have to be passed explicitly**; `setup.cfg` carries only the `[coverage:*]` sections.
`setup.cfg` used to hold a shadowed `[tool:pytest]` section too; it was removed, so don't
put pytest settings there.

`[coverage:report] exclude_lines` entries are **regexes matched as substrings**, and
coverage excludes the whole clause under a match. An unanchored pattern there once hid the
entire config flow while the total still read 100% — see item 1 of TODO.md. Anchor anything
that names code (`^\s*raise NotImplementedError`); `pragma: no cover` is the exception and
stays unanchored, since it is a trailing marker rather than a statement. After touching the
section, check `excluded_lines` in `--cov-report=json` — it should be empty.

## Architecture

```
custom_components/som_energia/
  __init__.py        setup/unload entry, forwards to PLATFORMS
  const.py           DOMAIN, PLATFORMS
  config_flow.py     single step, one field (the supply zone), plus reconfigure
  coordinator.py     one snapshot a minute, shared by the four sensors
  sensor.py          4 CoordinatorEntity classes, no polling of their own
  price/
    prices.py        period + price calculation (the actual domain logic)
    tariff_holiday.py  Spanish holiday lookup
    zone.py            supply zone -> time zone
    prices.csv       the price table
```

**The whole domain model lives in `price/prices.py`.** Everything flows from
`period(datetime) -> "P1" | "P2" | "P3"`:

- Time is converted to the entry's zone first — `Europe/Madrid` for Península and
  Baleares, `Atlantic/Canary` for Canarias — so every calculation is in local Spanish
  time regardless of the HA instance's timezone.
- P3 (valle) for weekends, tariff holidays, and 00:00–08:00.
- P2 (llano) for 08–10, 14–18, 22–24. P1 (punta) otherwise.
- `tariff_holiday.is_tariff_holiday` matches against `TARIFF_HOLIDAYS`, a frozen set of
  nine `(month, day)` pairs. CNMC Circular 3/2020 art. 7.3 makes P3 the whole of every
  Saturday, Sunday, 6 January and national holiday "con exclusión tanto de los festivos
  sustituibles como de los que no tienen fecha fija" — so the tariff calendar has **no
  movable component at all** and needs no holiday package. **Good Friday is excluded**
  because it moves, not as a special case; the same clause drops Maundy Thursday. Don't
  "fix" this, and don't add Semana Santa.

`prices.csv` maps date ranges to per-period prices. Row keys are the parsed
`(Inicio Periodo, Final Periodo)` dates and the *first* matching row wins, so rows must
stay in chronological order and must not overlap. The open-ended current row ends at
`2999-12-31` — when adding a new price period, close that row and add a new
`2999-12-31` one. Empty cells parse as `0.0`.

`sensor.py` exposes four sensors: `price`, `price_generation_kwh`, `compensation` (all
€/kWh) and `period` (P1/P2/P3). They do not compute anything and are not polled. A
`SomEnergiaCoordinator` reads the clock once a minute and calls
`prices.current_prices(utcnow())`, which returns the whole `PriceSnapshot` from **one**
time zone conversion and **one** table scan; the sensors are `CoordinatorEntity`
subclasses whose `native_value` picks one field out of it.

**That single reading of the clock is the point.** With each sensor calling `utcnow()`
for itself, an update landing on a period boundary could publish a period of P2 next to
a price still computed as P1 — see `test_a_period_boundary_cannot_split_the_sensors`,
which fails the moment anything reads the clock twice. It follows that the four sensors
share a fate: `CoordinatorEntity.available` tracks `last_update_success`, so a failed
computation takes all four to `unavailable` together instead of leaving each holding
whatever it last managed. `_async_update_data` turns the one reachable failure — an
unresolvable `Europe/Madrid` — into `UpdateFailed`, which during setup becomes
`ConfigEntryNotReady` and retries the entry.

`price`, `price_generation_kwh` and `compensation` remain as module-level wrappers over
`current_prices`, which is what the price tests use. `period` is not routed through it:
it needs no price row, and going through the snapshot would make the cheapest value pay
for a table scan.

### Supply zones

`price/zone.py` maps the three zones Som Energia serves — `peninsula`, `baleares`,
`canarias` — to an IANA time zone, and that mapping is the **whole** of what a zone
changes. Everything else is deliberately shared:

- **Prices do not vary by zone.** Zone-dependent pricing is a property of Som Energia's
  *indexada* tariff, whose energy cost tracks a wholesale market that Baleares and
  Canarias are not part of. This integration models the *periodos* tariff, quoted once
  for the whole state; the published figures match `prices.csv` exactly. Don't add a
  `Zona` column. The only thing Som Energia says about Canarias there is that IGIC
  applies instead of IVA, and the CSV is pre-tax, so that falls outside the model too.
- **The hour table does not vary either**, which is why `_period_of` takes no zone.
  Ceuta y Melilla is the one 2.0TD zone whose hours differ — CNMC Circular 3/2020 art. 7
  puts its punta at 11–15 and 19–23 — and Som Energia serves "todo el Estado español, a
  excepción de Ceuta y Melilla", so it is exactly the zone nobody can contract.
- **Baleares maps to `Europe/Madrid`** and is therefore identical to Península in every
  respect this integration models. It exists because it is how Som Energia asks members
  where their supply point is; it is not a copy-paste slip.

So Canarias is the only zone that does anything, and what it does is read the same hours
on a clock an hour behind. The Circular never states which clock its ranges are counted
against — "hora oficial", "hora peninsular" and "huso horario" appear nowhere in it — but
it shifts the ranges for Ceuta y Melilla, which shares the peninsular clock, while giving
Canarias the unshifted ones. A shift written for the zone needing no conversion and none
for the zone that does only reads one way: the hours are local.

The zone strings and the `zone` key are persisted on the config entry and must never be
renamed. Config flow `VERSION` is 2; `async_migrate_entry` stamps version 1 entries as
peninsular, which is what they were, and the coordinator then reads
`entry.data[CONF_ZONE]` outright. Don't give that read a default — a `.get(...,
PENINSULA)` would turn a failed migration into a Canarian install quietly served
peninsular hours, which is the one failure here that still looks plausible.

### Async discipline

Home Assistant forbids blocking calls in the event loop. The one blocking operation —
reading `prices.csv` — is wrapped in
`get_running_loop().run_in_executor(None, ...)`, and timezone lookup uses
`homeassistant.util.dt.async_get_time_zone` rather than `ZoneInfo(...)`. Keep any new
file, network, or heavy-CPU work off the loop the same way; this pattern exists because
of real "blocking call detected" warnings in HA logs.

That read now happens **once per process**: `_read_price_csv` fills a module-level
`_price_table`, warmed by the coordinator's `async_config_entry_first_refresh()` during
`async_setup_entry`, and every lookup afterwards is an in-memory scan with no thread
hop. Keep the read in the
executor anyway — HA's `block_async_io` patches `builtins.open` and exempts only
`/proc`, so parsing on the loop logs a blocking-call warning even the one time. It
warns rather than raising and is skipped under tests, so nothing but
`test_the_price_csv_is_never_parsed_on_the_event_loop` would catch the regression. The
table is typed `Mapping`, not `dict`: it is shared by every caller and mypy is what
stops anyone mutating it.

Import that helper **from `homeassistant.util.dt`, never from `aiozoneinfo`**. HA's
wrapper is a two-line delegation to that package, so it is the same lookup and the same
cache, but `aiozoneinfo` is an internal HA dependency this integration does not declare
and must not import. The wrapper also returns `None` instead of raising when the zone
cannot be resolved, which `_local_time` turns into a `HomeAssistantError` — letting it
through would reach `astimezone(None)` and silently serve prices in the host's timezone.

Requiring `homeassistant.util.dt.async_get_time_zone` is what first put a floor in
`hacs.json`, at `2024.6.0`: that helper and `aiozoneinfo` both landed in that release.
The floor is `2025.3.0` today for an unrelated reason — item 5 of TODO.md, the CI Python
version — so that is the version the code may assume.

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
