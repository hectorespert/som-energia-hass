"""Som Energia integration."""

from homeassistant.core import Config, HomeAssistant, DiscoveryInfoType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .sensor import ElectricityPriceSensor

DOMAIN = "som-energia"


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_platform(hass: HomeAssistant, config: Config, async_add_entities: AddEntitiesCallback, discovery_info: DiscoveryInfoType | None = None):
    async_add_entities(ElectricityPriceSensor())
