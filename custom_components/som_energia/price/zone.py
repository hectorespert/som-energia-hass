"""The Som Energia supply zones, and which clock each one counts its hours against.

Som Energia serves the whole Spanish state "a excepción de Ceuta y Melilla", so there
are exactly three zones to model. That exclusion is what keeps this module to a
mapping: Ceuta y Melilla is the *only* 2.0TD zone whose hourly boundaries actually
differ — CNMC Circular 3/2020 art. 7 puts its punta at 11-15 and 19-23 instead of 10-14
and 18-22 — and it is precisely the one nobody can contract. Every zone that is left
shares one hour table, which is why `_period_of` takes no zone and why there is no
per-zone schedule here.

The prices do not vary either. Zone-dependent pricing is a property of Som Energia's
*indexada* tariff, whose energy cost tracks a wholesale market, and Baleares and
Canarias are non-peninsular systems dispatched by REE rather than traded on OMIE. This
integration models the *periodos* tariff, which is a fixed price quoted once for the
whole state; the published punta/llano/valle figures match prices.csv exactly. The
only thing Som Energia says about Canarias on that tariff is that IGIC applies instead
of IVA, and prices.csv is pre-tax, so even that falls outside what is modelled here.

What is left is the clock. Baleares keeps peninsular time and is therefore, for every
purpose this integration has, identical to Península; it is listed anyway because it is
how Som Energia asks members where their supply point is, and because a zone already
stored on the entry costs nothing if the tariffs ever do diverge.

Canarias is UTC+0 and needs its own zone for that reason alone. The Circular never
states which clock its hour ranges are counted against — the words "hora oficial",
"hora peninsular" and "huso horario" appear nowhere in it — but it assigns Canarias the
same ranges as the peninsula while explicitly shifting the ranges for Ceuta y Melilla,
which shares the peninsular clock. A shift written for the zone that needs no
conversion, and no shift for the zone that does, only reads one way: the hours are
local. So the peninsular table, evaluated in Atlantic/Canary.
"""

from collections.abc import Mapping

PENINSULA = "peninsula"
BALEARES = "baleares"
CANARIAS = "canarias"

# Mapping, not dict: the zone table is read from every price lookup and must not be
# mutated, the same reason the parsed price table is typed this way.
ZONE_TIME_ZONES: Mapping[str, str] = {
    PENINSULA: "Europe/Madrid",
    BALEARES: "Europe/Madrid",
    CANARIAS: "Atlantic/Canary",
}

# The order the config flow offers them in, and the values stored on the config entry.
# These strings are persisted, so they must never change.
ZONES = tuple(ZONE_TIME_ZONES)
