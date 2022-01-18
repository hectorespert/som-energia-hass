"""Som Energia integration."""

from homeassistant.core import Config, HomeAssistant

DOMAIN = "som-energia"


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up configured FMI."""
    hass.data.setdefault(DOMAIN, {})
    return True
