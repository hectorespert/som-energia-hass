"""The single place the four sensor values are computed."""

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import utcnow

from custom_components.som_energia.const import CONF_ZONE, DOMAIN
from custom_components.som_energia.price.prices import PriceSnapshot, current_prices

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(minutes=1)

# The coordinator is the entry's runtime data; typing the entry with it is what lets
# mypy check `entry.runtime_data` at every use site instead of returning Any.
SomEnergiaConfigEntry = ConfigEntry["SomEnergiaCoordinator"]


class SomEnergiaCoordinator(DataUpdateCoordinator[PriceSnapshot]):
    """Compute the published values once per tick and hand the same snapshot to all
    four sensors.

    Nothing here is fetched: the values are pure functions of the clock, so an update
    cannot fail for the usual reasons a coordinator exists. What it buys is atomicity —
    with each sensor calling utcnow() for itself, an update landing on a period boundary
    could publish a period of P2 next to a price still computed as P1.
    """

    config_entry: SomEnergiaConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: SomEnergiaConfigEntry) -> None:
        """Initialize the coordinator with the one-minute cadence the sensors had."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        # Read once, at construction: changing the zone reconfigures the entry, which
        # reloads it and builds a new coordinator anyway.
        self._zone = config_entry.data[CONF_ZONE]

    async def _async_update_data(self) -> PriceSnapshot:
        """Read the clock once and derive everything from that single instant."""
        try:
            return await current_prices(utcnow(), self._zone)
        except HomeAssistantError as error:
            # The only way this fails is the zone's time zone being unresolvable.
            # UpdateFailed is the shape the coordinator understands: one line at error
            # level and the four sensors go unavailable together, rather than an
            # unexpected-exception traceback every minute. During setup it becomes
            # ConfigEntryNotReady, so the entry is retried instead of left half up.
            raise UpdateFailed(error) from error
