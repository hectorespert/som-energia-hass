from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CURRENCY_EURO, UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import utcnow

from custom_components.som_energia.const import DOMAIN
from custom_components.som_energia.price import compensation, price
from custom_components.som_energia.price.prices import period, price_generation_kwh


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    device_info = DeviceInfo(
        identifiers={(DOMAIN, config_entry.entry_id)},
        name="Som Energia",
        manufacturer="Som Energia",
        entry_type=DeviceEntryType.SERVICE,
    )
    async_add_entities([
        ElectricityPriceSensor(device_info),
        ElectricityCompensationSensor(device_info),
        GenerationKWHElectricityPriceSensor(device_info),
        ElectricityPeriodSensor(device_info)
    ], True)

SCAN_INTERVAL = timedelta(minutes=1)


class ElectricityPriceSensor(SensorEntity):
    """Class to hold the prices of electricity as a sensor."""

    _attr_has_entity_name = True

    def __init__(self, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = 'som_energia_electricity_price'
        self._attr_device_info = device_info
        self.entity_description = SensorEntityDescription(
            key='price',
            translation_key='price',
            icon="mdi:currency-eur",
            native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
            state_class=SensorStateClass.MEASUREMENT,
        )
        self._state: float | None = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._state = await price(utcnow())


class GenerationKWHElectricityPriceSensor(SensorEntity):
    """Class to hold the prices of electricity as a sensor."""

    _attr_has_entity_name = True

    def __init__(self, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = 'som_energia_generation_kwh_electricity_price'
        self._attr_device_info = device_info
        self.entity_description = SensorEntityDescription(
            key='price_generation_kwh',
            translation_key='price_generation_kwh',
            icon="mdi:currency-eur",
            native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
            state_class=SensorStateClass.MEASUREMENT,
        )
        self._state: float | None = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._state = await price_generation_kwh(utcnow())


class ElectricityCompensationSensor(SensorEntity):
    """Class to hold the compensation of electricity as a sensor."""

    _attr_has_entity_name = True

    def __init__(self, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = 'som_energia_electricity_compensation'
        self._attr_device_info = device_info
        self.entity_description = SensorEntityDescription(
            key='compensation',
            translation_key='compensation',
            icon="mdi:currency-eur",
            native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
            state_class=SensorStateClass.MEASUREMENT,
        )
        self._state: float | None = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._state = await compensation(utcnow())


class ElectricityPeriodSensor(SensorEntity):
    """Class to hold the current electricity tariff period as a sensor."""

    _attr_has_entity_name = True

    def __init__(self, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = 'som_energia_electricity_period'
        self._attr_device_info = device_info
        self.entity_description = SensorEntityDescription(
            key='period',
            translation_key='period',
            icon="mdi:clock-outline",
            device_class=SensorDeviceClass.ENUM,
            options=["P1", "P2", "P3"],
        )
        self._state: str | None = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._state = await period(utcnow())
