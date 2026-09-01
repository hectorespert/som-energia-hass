# TODO

**Nothing is open.** The fifteen findings of the audit against Home Assistant 2025.11.3
are all fixed on `master`.

This file used to carry the full write-up of every finding — 580 lines that every agent
reads at the start of every session. None of that reasoning is lost: each row below
names the pull request that carries it, `git log -p TODO.md` still holds the long-form
text, and the parts that must not regress were moved to where they actually get read,
[AGENTS.md](AGENTS.md) and
[.github/copilot-instructions.md](.github/copilot-instructions.md).

New findings go back at the top of this file, one section each with the reproduction,
and get struck through when fixed. Keep the closed ones down to their one line here.

## Fixed

| # | Finding | PR |
| --- | --- | --- |
| 1 | An unanchored `exclude_lines` regex hid the whole config flow from coverage while the total still read 100% | [#73] |
| 2 | `async_unload_entry` never unloaded the sensor platform, so the old entities kept polling after a reload | [#74] |
| 3 | A date matching no CSV row silently served the last row instead of `None` | [#71] |
| 4 | Good Friday detection depended on an unpinned localized string; the 2.0TD calendar is a closed list of nine fixed dates and needs no holiday package | [#75] |
| 5 | `aiozoneinfo` was imported directly, and CI pinned to Python 3.12 was testing a January Home Assistant while looking green | [#76] |
| 6 | Deprecated config-flow and platform typing | [#77] |
| 7 | A unique-id hack stood in for `single_config_entry` | [#78] |
| 8 | Entity names were hardcoded in English, on an integration whose users are Spanish | [#79] |
| 9 | The period sensor was not an enum, and the four entities belonged to no device | [#80] |
| 10 | No lint or security gate in CI, though `setup.cfg` had the settings | [#81] |
| 11 | `prices.csv` was re-read and re-parsed on every one of the 4320 sensor updates a day | [#85] |
| 12 | `config_flow.py` was opted out of the mypy gate | [#81] |
| 13 | A sensor test compared a price as a string, so `0.9 > 0.11` passed | [#83] |
| 14 | `tests/bandit.yaml` listed two checks bandit no longer has | [#84] |
| 15 | Each sensor recomputed the values from its own `utcnow()`, so a tick on a period boundary could publish P2's period next to P1's price | [#86] |

[#71]: https://github.com/hectorespert/som-energia-hass/pull/71
[#73]: https://github.com/hectorespert/som-energia-hass/pull/73
[#74]: https://github.com/hectorespert/som-energia-hass/pull/74
[#75]: https://github.com/hectorespert/som-energia-hass/pull/75
[#76]: https://github.com/hectorespert/som-energia-hass/pull/76
[#77]: https://github.com/hectorespert/som-energia-hass/pull/77
[#78]: https://github.com/hectorespert/som-energia-hass/pull/78
[#79]: https://github.com/hectorespert/som-energia-hass/pull/79
[#80]: https://github.com/hectorespert/som-energia-hass/pull/80
[#81]: https://github.com/hectorespert/som-energia-hass/pull/81
[#83]: https://github.com/hectorespert/som-energia-hass/pull/83
[#84]: https://github.com/hectorespert/som-energia-hass/pull/84
[#85]: https://github.com/hectorespert/som-energia-hass/pull/85
[#86]: https://github.com/hectorespert/som-energia-hass/pull/86
