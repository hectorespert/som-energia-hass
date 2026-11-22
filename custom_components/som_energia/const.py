from homeassistant.const import Platform

DOMAIN = "som_energia"
PLATFORMS = [Platform.SENSOR]

# Key of the supply zone on the config entry's data. The stored values are the ones in
# price.zone.ZONES; both the key and the values are persisted and must never change.
CONF_ZONE = "zone"
