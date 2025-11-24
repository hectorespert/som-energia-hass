from datetime import timedelta

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CURRENCY_EURO, UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import utcnow

from custom_components.som_energia.price import price, compensation
from custom_components.som_energia.price.prices import price_generation_kwh, period


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([
        ElectricityPriceSensor(),
        ElectricityCompensationSensor(),
        GenerationKWHElectricityPriceSensor(),
        ElectricityPeriodSensor()
    ], True)

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
            native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
            state_class=SensorStateClass.MEASUREMENT,
        )
        self._state = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = await price(utcnow())

class GenerationKWHElectricityPriceSensor(SensorEntity):
    """Class to hold the prices of electricity as a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = 'som_energia_generation_kwh_electricity_price'
        self._attr_name = 'Som Energia Generation kWh electricity price'
        self.entity_description = SensorEntityDescription(
            key='electricity_price',
            icon="mdi:currency-eur",
            native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
            state_class=SensorStateClass.MEASUREMENT,
        )
        self._state = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = await price_generation_kwh(utcnow())

class ElectricityCompensationSensor(SensorEntity):
    """Class to hold the compensation of electricity as a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = 'som_energia_electricity_compensation'
        self._attr_name = 'Som Energia electricity compensation'
        self.entity_description = SensorEntityDescription(
            key='electricity_price',
            icon="mdi:currency-eur",
            native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
            state_class=SensorStateClass.MEASUREMENT,
        )
        self._state = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = await compensation(utcnow())

class ElectricityPeriodSensor(SensorEntity):
    """Class to hold the current electricity tariff period as a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = 'som_energia_electricity_period'
        self._attr_name = 'Som Energia electricity period'
        self.entity_description = SensorEntityDescription(
            key='electricity_period',
            icon="mdi:clock-outline",
        )
        self._state = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = await period(utcnow())

