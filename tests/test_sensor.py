from datetime import datetime, timedelta
from unittest.mock import patch
from zoneinfo import ZoneInfo

from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.util import utcnow
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_time_changed,
)

from custom_components.som_energia import DOMAIN
from custom_components.som_energia.const import CONF_ZONE
from custom_components.som_energia.coordinator import UPDATE_INTERVAL
from custom_components.som_energia.price.prices import current_prices
from custom_components.som_energia.price.zone import CANARIAS, PENINSULA

SENSORS = [
    "sensor.som_energia_electricity_price",
    "sensor.som_energia_generation_kwh_price",
    "sensor.som_energia_surplus_compensation",
    "sensor.som_energia_tariff_period",
]


async def test_sensors(hass):
    assert hass is not None

    entry = MockConfigEntry(
        domain=DOMAIN,
    )
    assert entry is not None
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    # All four entities now share a `device_info`, so `_attr_has_entity_name`
    # prefixes the friendly name with the device name ("Som Energia") and a
    # new install's entity_id is derived from "som_energia " + the translated
    # name, slugified — measured against the default (English) test locale.
    state = hass.states.get("sensor.som_energia_generation_kwh_price")
    assert state
    assert float(state.state) > 0.0
    assert state.name == "Som Energia Generation kWh price"
    assert state.attributes["unit_of_measurement"] == "€/kWh"

    state = hass.states.get("sensor.som_energia_tariff_period")
    assert state
    assert state.state in ["P1", "P2", "P3"]
    assert state.name == "Som Energia Tariff period"
    assert state.attributes["device_class"] == "enum"
    assert state.attributes["options"] == ["P1", "P2", "P3"]

    state = hass.states.get("sensor.som_energia_surplus_compensation")
    assert state
    assert float(state.state) > 0.0
    assert state.name == "Som Energia Surplus compensation"
    assert state.attributes["unit_of_measurement"] == "€/kWh"

    state = hass.states.get("sensor.som_energia_electricity_price")
    assert state
    assert float(state.state) > 0.0
    assert state.name == "Som Energia Electricity price"
    assert state.attributes["unit_of_measurement"] == "€/kWh"


async def test_sensor_names_are_translated_to_spanish(hass):
    """translation_key resolves through translations/es.json, not just en.json."""
    hass.config.language = "es"

    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.som_energia_precio_de_la_electricidad")
    assert state
    assert state.name == "Som Energia Precio de la electricidad"

    state = hass.states.get("sensor.som_energia_precio_generacion_kwh")
    assert state
    assert state.name == "Som Energia Precio Generación kWh"

    state = hass.states.get("sensor.som_energia_compensacion_de_excedentes")
    assert state
    assert state.name == "Som Energia Compensación de excedentes"

    state = hass.states.get("sensor.som_energia_periodo_tarifario")
    assert state
    assert state.name == "Som Energia Periodo tarifario"


async def test_unique_ids_are_unchanged(hass):
    """The unique_id values must never change: they are what ties an existing
    installation's entity registry entry (and its user-chosen entity_id,
    dashboards, automations, long-term statistics, ...) to the entity."""
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    registry = er.async_get(hass)
    unique_ids = {
        entry_.unique_id
        for entry_ in er.async_entries_for_config_entry(registry, entry.entry_id)
    }
    assert unique_ids == {
        "som_energia_electricity_price",
        "som_energia_generation_kwh_electricity_price",
        "som_energia_electricity_compensation",
        "som_energia_electricity_period",
    }


async def test_entities_are_grouped_under_one_device(hass):
    """All four sensors declare the same `device_info`, so a `hub` integration
    stops producing four ungrouped entities and instead shows one "Som
    Energia" device with the four sensors underneath it."""
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    device_registry = dr.async_get(hass)
    device = device_registry.async_get_device(identifiers={(DOMAIN, entry.entry_id)})
    assert device is not None
    assert device.name == "Som Energia"
    assert device.manufacturer == "Som Energia"
    assert device.model is None
    assert device.configuration_url is None
    assert device.entry_type == dr.DeviceEntryType.SERVICE

    entity_registry = er.async_get(hass)
    entities = er.async_entries_for_config_entry(entity_registry, entry.entry_id)
    assert len(entities) == 4
    assert all(entity.device_id == device.id for entity in entities)


async def test_existing_entity_ids_survive_setup_and_reload(hass):
    """An existing installation's entity registry already maps these
    unique_ids to the pre-translation_key entity_ids. Home Assistant looks
    entities up by unique_id, not by the object_id it would otherwise
    generate from the (now translated) name, so upgrading must not rename
    any entity_id a real installation already has."""
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)

    registry = er.async_get(hass)
    legacy_entity_ids = {
        "som_energia_electricity_price": "sensor.som_energia_electricity_price",
        "som_energia_generation_kwh_electricity_price":
            "sensor.som_energia_generation_kwh_electricity_price",
        "som_energia_electricity_compensation": "sensor.som_energia_electricity_compensation",
        "som_energia_electricity_period": "sensor.som_energia_electricity_period",
    }
    for unique_id, entity_id in legacy_entity_ids.items():
        registry.async_get_or_create(
            "sensor",
            DOMAIN,
            unique_id,
            suggested_object_id=entity_id.split(".", 1)[1],
            config_entry=entry,
        )

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    for entity_id in legacy_entity_ids.values():
        assert hass.states.get(entity_id) is not None

    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()

    for entity_id in legacy_entity_ids.values():
        assert hass.states.get(entity_id) is not None


async def _setup_entry(hass) -> MockConfigEntry:
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def _tick(hass) -> None:
    """Advance past the coordinator's interval and let the refresh run.

    The scheduled refresh is a background task, and a plain async_block_till_done()
    returns before it has finished — the assertions would then read the state of the
    previous tick.
    """
    async_fire_time_changed(hass, utcnow() + UPDATE_INTERVAL + timedelta(seconds=1))
    await hass.async_block_till_done(wait_background_tasks=True)


async def test_one_tick_computes_the_values_once_for_the_four_sensors(hass):
    """The four sensors follow the coordinator instead of polling; a tick is a single
    computation, where it used to be four."""
    await _setup_entry(hass)

    computations = 0

    async def counting_current_prices(current_datetime, zone):
        nonlocal computations
        computations += 1
        return await current_prices(current_datetime, zone)

    with patch(
        "custom_components.som_energia.coordinator.current_prices",
        new=counting_current_prices,
    ):
        await _tick(hass)

    assert computations == 1
    for entity_id in SENSORS:
        assert hass.states.get(entity_id).state not in (None, STATE_UNAVAILABLE)


async def test_a_period_boundary_cannot_split_the_sensors(hass):
    """This is what the coordinator buys. Each sensor used to call utcnow() for itself,
    so an update landing on 08:00 — the end of valle on a working Monday — could
    publish a period of P2 next to a price still computed as P1. One reading of the
    clock feeds all four, so the four always describe the same instant."""
    await _setup_entry(hass)

    # 2026-01-05 is a Monday and no tariff holiday: P3 until 08:00, P2 from it.
    boundary = datetime(2026, 1, 5, 8, 0, 0, tzinfo=ZoneInfo("Europe/Madrid"))
    clock_reads = 0

    def clock_crossing_the_boundary():
        """Every read lands a second later, so a second caller sees the other side."""
        nonlocal clock_reads
        clock_reads += 1
        return boundary + timedelta(seconds=clock_reads - 1) - timedelta(microseconds=1)

    with patch(
        "custom_components.som_energia.coordinator.utcnow",
        new=clock_crossing_the_boundary,
    ):
        await _tick(hass)

    assert clock_reads == 1
    assert hass.states.get("sensor.som_energia_tariff_period").state == "P3"
    # The valle prices of the 2026-01-01 row, not the llano ones (0.153 / 0.135).
    assert float(hass.states.get("sensor.som_energia_electricity_price").state) == 0.125
    assert float(hass.states.get("sensor.som_energia_generation_kwh_price").state) == 0.110


async def test_a_failed_update_takes_the_four_sensors_down_together(hass, caplog):
    """Availability is shared now: the sensors are unavailable exactly when the last
    computation failed, instead of each holding whatever it last managed to compute."""
    await _setup_entry(hass)

    async def unresolvable_time_zone(current_datetime, zone):
        raise HomeAssistantError("Time zone Europe/Madrid is not available")

    with patch(
        "custom_components.som_energia.coordinator.current_prices",
        new=unresolvable_time_zone,
    ):
        await _tick(hass)

    for entity_id in SENSORS:
        assert hass.states.get(entity_id).state == STATE_UNAVAILABLE
    # UpdateFailed, so one line at error level; an unhandled exception would log a
    # traceback every single minute.
    assert "Unexpected error fetching" not in caplog.text
    assert "Time zone Europe/Madrid is not available" in caplog.text


async def test_a_failed_first_refresh_retries_the_entry(hass):
    """The first refresh is what parses prices.csv. If it fails the entry must be
    retried, not left loaded with four unavailable sensors."""
    async def unresolvable_time_zone(current_datetime, zone):
        raise HomeAssistantError("Time zone Europe/Madrid is not available")

    with patch(
        "custom_components.som_energia.coordinator.current_prices",
        new=unresolvable_time_zone,
    ):
        entry = await _setup_entry(hass)

    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_a_canarias_entry_publishes_the_canarian_period(hass, freezer):
    """End to end, and the only check that the zone survives the trip from the config
    entry to the computation.

    13:00 UTC is 14:00 in Madrid and already llano, but 13:00 in Las Palmas and still
    punta. A coordinator that dropped the zone on the way to current_prices would
    publish P2 here and look entirely plausible doing it, which is why the assertion is
    on the sensor states rather than on the call.
    """
    freezer.move_to(datetime(2026, 1, 26, 13, 0, 0, tzinfo=ZoneInfo("UTC")))

    entry = MockConfigEntry(domain=DOMAIN, version=2, data={CONF_ZONE: CANARIAS})
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.som_energia_tariff_period").state == "P1"
    assert float(hass.states.get("sensor.som_energia_electricity_price").state) == 0.229


async def test_a_peninsula_entry_publishes_the_peninsular_period(hass, freezer):
    """The other side of the same instant: what a Canarian install must not show."""
    freezer.move_to(datetime(2026, 1, 26, 13, 0, 0, tzinfo=ZoneInfo("UTC")))

    entry = MockConfigEntry(domain=DOMAIN, version=2, data={CONF_ZONE: PENINSULA})
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.som_energia_tariff_period").state == "P2"
    assert float(hass.states.get("sensor.som_energia_electricity_price").state) == 0.153
