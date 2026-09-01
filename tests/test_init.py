from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.helpers import entity_platform
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.som_energia import DOMAIN

SENSORS = [
    "sensor.electricity_price",
    "sensor.generation_kwh_price",
    "sensor.surplus_compensation",
    "sensor.tariff_period",
]


async def _add_loaded_entry(hass) -> MockConfigEntry:
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def test_setup_entry_loads_the_sensor_platform(hass):
    entry = await _add_loaded_entry(hass)

    assert entry.state is ConfigEntryState.LOADED
    for entity_id in SENSORS:
        assert hass.states.get(entity_id) is not None


async def test_unload_entry_removes_the_sensors(hass):
    entry = await _add_loaded_entry(hass)

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
    # The entity registry keeps the ids reserved, but nothing backs them any
    # more: the states go unavailable instead of holding the last price.
    for entity_id in SENSORS:
        state = hass.states.get(entity_id)
        assert state is not None
        assert state.state == STATE_UNAVAILABLE
    # Home Assistant keeps the EntityPlatform object around but resets it. What
    # matters is that it holds no entities: an unreset platform goes on polling
    # them every SCAN_INTERVAL with the entry already marked NOT_LOADED.
    for platform in entity_platform.async_get_platforms(hass, DOMAIN):
        assert platform.entities == {}


async def test_reload_entry_sets_the_platform_up_again(hass, caplog):
    entry = await _add_loaded_entry(hass)

    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED
    for entity_id in SENSORS:
        assert hass.states.get(entity_id) is not None
    # A reload that does not unload first fails with "has already been setup!",
    # which config_entries logs and swallows while leaving the entry LOADED.
    assert "already been setup" not in caplog.text
