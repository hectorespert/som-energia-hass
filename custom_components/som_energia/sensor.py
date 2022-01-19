from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

class ElectricityPriceSensor(SensorEntity):
    """Class to hold the prices of electricity as a sensor."""

    @property
    def name(self):
        """Return the name of the sensor"""
        return "Som Energia electricity prices"