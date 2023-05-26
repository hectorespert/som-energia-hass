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

from custom_components.som_energia.price import price, compensation


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([ElectricityPriceSensor(), ElectricityCompensationSensor()], True)

SCAN_INTERVAL = timedelta(minutes=1)


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
        self._state = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = price(utcnow())


class ElectricityCompensationSensor(SensorEntity):
    """Class to hold the compensation of electricity as a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = 'som_energia_electricity_compensation'
        self._attr_name = 'Som Energia electricity compensation'
        self.entity_description = SensorEntityDescription(
            key='electricity_price',
            icon="mdi:currency-eur",
            native_unit_of_measurement=f"{CURRENCY_EURO}/{ENERGY_KILO_WATT_HOUR}",
            state_class=SensorStateClass.MEASUREMENT,
        )
        self._state = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = compensation(utcnow())
