from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.som_energia import DOMAIN


async def test_sensors(hass):
    assert hass is not None

    entry = MockConfigEntry(
        domain=DOMAIN,
    )
    assert entry is not None
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.som_energia_electricity_price")
    assert state
    assert state.state > "0.0"
    assert state.name == "Som Energia electricity price"
    assert state.attributes["unit_of_measurement"] == "€/kWh"

    state = hass.states.get("sensor.som_energia_electricity_compensation")
    assert state
    assert state.state > "0.0"
    assert state.name == "Som Energia electricity compensation"
    assert state.attributes["unit_of_measurement"] == "€/kWh"

    state = hass.states.get("sensor.som_energia_generation_kwh_electricity_price")
    assert state
    assert state.state > "0.0"
    assert state.name == "Som Energia Generation kWh electricity price"
    assert state.attributes["unit_of_measurement"] == "€/kWh"