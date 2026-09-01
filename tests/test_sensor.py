from homeassistant.helpers import device_registry as dr, entity_registry as er
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

    # All four entities now share a `device_info`, so `_attr_has_entity_name`
    # prefixes the friendly name with the device name ("Som Energia") and a
    # new install's entity_id is derived from "som_energia " + the translated
    # name, slugified — measured against the default (English) test locale.
    state = hass.states.get("sensor.som_energia_generation_kwh_price")
    assert state
    assert state.state > "0.0"
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
    assert state.state > "0.0"
    assert state.name == "Som Energia Surplus compensation"
    assert state.attributes["unit_of_measurement"] == "€/kWh"

    state = hass.states.get("sensor.som_energia_electricity_price")
    assert state
    assert state.state > "0.0"
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
