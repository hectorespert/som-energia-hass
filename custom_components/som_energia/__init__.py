"""Som Energia integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up the Som Energia component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Som Energia from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
