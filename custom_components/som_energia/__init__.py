"""Som Energia integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS
from .coordinator import SomEnergiaConfigEntry, SomEnergiaCoordinator

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


async def async_unload_entry(hass: HomeAssistant, entry: SomEnergiaConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
