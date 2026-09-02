"""Som Energia integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import CONF_ZONE, DOMAIN, PLATFORMS
from .coordinator import SomEnergiaConfigEntry, SomEnergiaCoordinator
from .price.zone import PENINSULA

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Som Energia component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: SomEnergiaConfigEntry) -> bool:
    """Set up Som Energia from a config entry."""
    coordinator = SomEnergiaCoordinator(hass, entry)
    # The first refresh parses prices.csv — in the executor, where blocking work
    # belongs — and gives the sensors a value before they are added, so none of them
    # is ever published as unknown.
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_migrate_entry(hass: HomeAssistant, entry: SomEnergiaConfigEntry) -> bool:
    """Bring a version 1 entry forward by naming the zone it always had.

    Version 1 stored no zone because there was only one: every existing installation is
    peninsular by construction. Stamping it explicitly is what lets the coordinator read
    entry.data[CONF_ZONE] outright instead of defaulting, which would quietly serve
    peninsular hours to anyone whose migration had failed.
    """
    if entry.version == 1:
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, CONF_ZONE: PENINSULA}, version=2
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: SomEnergiaConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
