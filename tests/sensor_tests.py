from homeassistant.core import HomeAssistant

async def test_electricity_price_sensor(hass: HomeAssistant):
    await hass.async_block_till_done()
