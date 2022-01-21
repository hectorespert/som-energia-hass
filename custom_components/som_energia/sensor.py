from datetime import timedelta

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ENERGY_KILO_WATT_HOUR, CURRENCY_EURO
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import utcnow
from pytz import timezone


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([ElectricityPriceSensor()], False)

SCAN_INTERVAL = timedelta(minutes=15)


class ElectricityPriceSensor(SensorEntity):
    """Class to hold the prices of electricity as a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = 'som_energia_electricity_price'
        self._attr_name = 'Som Energia electricity price'
        self.entity_description = SensorEntityDescription(
            key='electricity_price',
            icon="mdi:currency-eur",
            native_unit_of_measurement=f"{CURRENCY_EURO}/{ENERGY_KILO_WATT_HOUR}",
            state_class=SensorStateClass.MEASUREMENT,
        )
        self._state = 0

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        datetime = utcnow().astimezone(timezone('Europe/Madrid'))
        weekday = datetime.isoweekday()
        if weekday == 6 or weekday == 7:
            return 0.262
        hour = datetime.hour
        if 0 <= hour < 8:
            return 0.262
        elif 8 <= hour < 10 or 14 <= hour < 18 or 22 <= hour < 24:
            return 0.320
        else:
            return 0.407

