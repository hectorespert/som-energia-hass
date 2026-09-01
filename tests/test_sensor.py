from homeassistant.helpers import entity_registry as er
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

    # The entities have no device (device_info is added in a follow-up), so
    # `_attr_has_entity_name` does not prefix the friendly name with a device
    # name: `name` is exactly the translated string, measured against the
    # default (English) test locale.
    state = hass.states.get("sensor.generation_kwh_price")
    assert state
    assert state.state > "0.0"
    assert state.name == "Generation kWh price"
    assert state.attributes["unit_of_measurement"] == "€/kWh"

    state = hass.states.get("sensor.tariff_period")
    assert state
    assert state.state in ["P1", "P2", "P3"]
    assert state.name == "Tariff period"

    state = hass.states.get("sensor.surplus_compensation")
    assert state
    assert state.state > "0.0"
    assert state.name == "Surplus compensation"
    assert state.attributes["unit_of_measurement"] == "€/kWh"

    state = hass.states.get("sensor.electricity_price")
    assert state
    assert state.state > "0.0"
    assert state.name == "Electricity price"
    assert state.attributes["unit_of_measurement"] == "€/kWh"


async def test_sensor_names_are_translated_to_spanish(hass):
    """translation_key resolves through translations/es.json, not just en.json."""
    hass.config.language = "es"

    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.precio_de_la_electricidad")
    assert state
    assert state.name == "Precio de la electricidad"

    state = hass.states.get("sensor.precio_generacion_kwh")
    assert state
    assert state.name == "Precio Generación kWh"

    state = hass.states.get("sensor.compensacion_de_excedentes")
    assert state
    assert state.name == "Compensación de excedentes"

    state = hass.states.get("sensor.periodo_tarifario")
    assert state
    assert state.name == "Periodo tarifario"


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
