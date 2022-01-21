"""Som Energia integration."""

from homeassistant.core import Config, HomeAssistant

from .const import DOMAIN
from .sensor import ElectricityPriceSensor


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True
