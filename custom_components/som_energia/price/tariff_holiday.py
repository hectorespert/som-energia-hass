"""Tariff holidays for the Spanish 2.0TD access toll.

CNMC Circular 3/2020, article 7.3, makes period P3 (valle) every hour of
Saturdays, Sundays, 6 January and the national holidays of the official
calendar, "con exclusión tanto de los festivos sustituibles como de los que no
tienen fecha fija".

Dropping the substitutable and the movable ones leaves a closed list of nine
fixed dates, the same every year. Good Friday is out because it moves, not as a
special case — the same clause drops Maundy Thursday. 6 January is named
explicitly by the Circular because it is substitutable and would otherwise fall
out too.

This is the *electricity* calendar, not the labour one. They happen to overlap
today, but nothing keeps them in step, which is why the list lives here instead
of coming from a general-purpose holiday package.

The same nine dates apply in every zone this integration serves. The Circular does set
a different schedule for one non-peninsular system, Ceuta y Melilla, but it shifts the
*hours*, not the calendar, and Som Energia does not supply there anyway — see
price/zone.py. What changes between zones is the clock the hours are read on, which is
why this list takes no zone.
"""

from datetime import datetime

TARIFF_HOLIDAYS = frozenset(
    {
        (1, 1),  # Año Nuevo
        (1, 6),  # Epifanía del Señor
        (5, 1),  # Fiesta del Trabajo
        (8, 15),  # Asunción de la Virgen
        (10, 12),  # Fiesta Nacional de España
        (11, 1),  # Todos los Santos
        (12, 6),  # Día de la Constitución
        (12, 8),  # Inmaculada Concepción
        (12, 25),  # Navidad
    }
)


def is_tariff_holiday(timezone_datetime: datetime) -> bool:
    """Check if the given datetime falls on a tariff holiday in Spain."""
    return (timezone_datetime.month, timezone_datetime.day) in TARIFF_HOLIDAYS
