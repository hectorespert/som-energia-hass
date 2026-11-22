from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntryState
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.som_energia import DOMAIN
from custom_components.som_energia.const import CONF_ZONE
from custom_components.som_energia.price.zone import CANARIAS, PENINSULA


async def test_form_is_shown_without_user_input(hass):
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] is None


async def test_entry_is_created_on_submit(hass):
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Som Energia"
    # The zone field is required but carries a default, so an empty submission still
    # produces the peninsular entry the flow used to create unconditionally.
    assert result["data"] == {CONF_ZONE: PENINSULA}

    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1
    assert entries[0].unique_id is None


async def test_only_one_entry_is_allowed(hass):
    # single_config_entry in manifest.json blocks the second flow in the flow
    # manager itself: async_step_user is never reached, so there is no
    # flow_id to configure and no unique_id involved.
    MockConfigEntry(domain=DOMAIN).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1


async def test_pre_existing_unique_id_entry_still_blocks_a_second_one(hass):
    # Regression check for users upgrading from the unique-id hack: an entry
    # saved by the old config flow still carries unique_id="som_energia_unique".
    # single_config_entry blocks on domain occupancy alone, so that stored
    # value is irrelevant to whether a second entry is allowed.
    MockConfigEntry(domain=DOMAIN, unique_id="som_energia_unique").add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"

    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1
    assert entries[0].unique_id == "som_energia_unique"


async def test_the_chosen_zone_is_stored_on_the_entry(hass):
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_ZONE: CANARIAS}
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["data"] == {CONF_ZONE: CANARIAS}

    entries = hass.config_entries.async_entries(DOMAIN)
    assert entries[0].data[CONF_ZONE] == CANARIAS
    # The entry has to be written at the current version, or every reload would try to
    # migrate it again.
    assert entries[0].version == 2


async def test_the_zone_can_be_changed_by_reconfiguring(hass):
    """Moving house must not mean deleting the entry: that would drop the four entity
    registry entries and with them their recorder history."""
    entry = MockConfigEntry(domain=DOMAIN, version=2, data={CONF_ZONE: PENINSULA})
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    result = await entry.start_reconfigure_flow(hass)
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_ZONE: CANARIAS}
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    assert entry.data[CONF_ZONE] == CANARIAS
    # Reconfiguring reloads the entry, which is what rebuilds the coordinator against
    # the new zone; without that the sensors would go on publishing the old one.
    assert entry.state is ConfigEntryState.LOADED
