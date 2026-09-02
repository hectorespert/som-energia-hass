from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
import voluptuous as vol

from .const import CONF_ZONE, DOMAIN
from .price.zone import PENINSULA, ZONES

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ZONE, default=PENINSULA): SelectSelector(
            SelectSelectorConfig(
                options=list(ZONES),
                translation_key="zone",
                mode=SelectSelectorMode.DROPDOWN,
            )
        )
    }
)


class SomEnergiaConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    # Bumped to 2 when the supply zone was added; async_migrate_entry stamps the
    # entries created by version 1 as peninsular, which is what they were.
    VERSION = 2

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

        return self.async_create_entry(title='Som Energia', data=user_input)

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Let an existing entry change its zone.

        Reconfigure rather than an options flow: the zone belongs in the entry's data,
        and an options flow would leave it in two places to read it back from.
        """
        reconfigure_entry = self._get_reconfigure_entry()
        if user_input is None:
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=self.add_suggested_values_to_schema(
                    STEP_USER_DATA_SCHEMA, reconfigure_entry.data
                ),
            )

        # Reloads the entry, which rebuilds the coordinator against the new zone.
        return self.async_update_reload_and_abort(reconfigure_entry, data_updates=user_input)
