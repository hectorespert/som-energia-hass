from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import CURRENCY_EURO, UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.som_energia.const import DOMAIN
from custom_components.som_energia.coordinator import (
    SomEnergiaConfigEntry,
    SomEnergiaCoordinator,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: SomEnergiaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = config_entry.runtime_data
    device_info = DeviceInfo(
        identifiers={(DOMAIN, config_entry.entry_id)},
        name="Som Energia",
        manufacturer="Som Energia",
        entry_type=DeviceEntryType.SERVICE,
    )
    # No update_before_add: the coordinator already refreshed during setup, and the
    # sensors are not polled at all any more — they follow it.
    async_add_entities([
        ElectricityPriceSensor(coordinator, device_info),
        ElectricityCompensationSensor(coordinator, device_info),
        GenerationKWHElectricityPriceSensor(coordinator, device_info),
        ElectricityPeriodSensor(coordinator, device_info)
    ])


class SomEnergiaSensor(CoordinatorEntity[SomEnergiaCoordinator], SensorEntity):
    """Base for the four sensors: same device, same snapshot, one value each."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SomEnergiaCoordinator,
        device_info: DeviceInfo,
        unique_id: str,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        # The unique_id values must never change: they are what ties an existing
        # installation's registry entry to the entity.
        self._attr_unique_id = unique_id
        self._attr_device_info = device_info
        self.entity_description = entity_description


class ElectricityPriceSensor(SomEnergiaSensor):
    """Class to hold the prices of electricity as a sensor."""

    def __init__(self, coordinator: SomEnergiaCoordinator, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_info,
            'som_energia_electricity_price',
            SensorEntityDescription(
                key='price',
                translation_key='price',
                icon="mdi:currency-eur",
                native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
                state_class=SensorStateClass.MEASUREMENT,
            ),
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data.price


class GenerationKWHElectricityPriceSensor(SomEnergiaSensor):
    """Class to hold the prices of electricity as a sensor."""

    def __init__(self, coordinator: SomEnergiaCoordinator, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_info,
            'som_energia_generation_kwh_electricity_price',
            SensorEntityDescription(
                key='price_generation_kwh',
                translation_key='price_generation_kwh',
                icon="mdi:currency-eur",
                native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
                state_class=SensorStateClass.MEASUREMENT,
            ),
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data.price_generation_kwh


class ElectricityCompensationSensor(SomEnergiaSensor):
    """Class to hold the compensation of electricity as a sensor."""

    def __init__(self, coordinator: SomEnergiaCoordinator, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_info,
            'som_energia_electricity_compensation',
            SensorEntityDescription(
                key='compensation',
                translation_key='compensation',
                icon="mdi:currency-eur",
                native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
                state_class=SensorStateClass.MEASUREMENT,
            ),
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data.compensation


class ElectricityPeriodSensor(SomEnergiaSensor):
    """Class to hold the current electricity tariff period as a sensor."""

    def __init__(self, coordinator: SomEnergiaCoordinator, device_info: DeviceInfo) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device_info,
            'som_energia_electricity_period',
            SensorEntityDescription(
                key='period',
                translation_key='period',
                icon="mdi:clock-outline",
                device_class=SensorDeviceClass.ENUM,
                options=["P1", "P2", "P3"],
            ),
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data.period
