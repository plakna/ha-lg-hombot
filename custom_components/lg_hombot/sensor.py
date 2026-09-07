"""Battery sensor platform for LG Hombot.

Split out from the vacuum entity because Home Assistant removed
VacuumEntityFeature.BATTERY and the vacuum battery_level property in 2026.9.
The battery level is now exposed as a dedicated battery sensor.
"""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.const import PERCENTAGE
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Setup of Entry."""
    url = config_entry.data.get("url")
    name = config_entry.data.get("name")
    async_add_entities([HombotBatterySensor(name, url)])


class HombotBatterySensor(SensorEntity):
    """Battery level of a Hombot vacuum cleaner robot."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, name: str, url: str) -> None:
        self._name = name
        self._url = url
        self._attr_name = name + " Battery"
        self._attr_native_value = None

    @property
    def unique_id(self) -> str | None:
        return "hombot_battery_" + self._url

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, "hombot_" + self._url)},
            name=self._name,
            manufacturer="LG",
            model="Hombot",
            configuration_url=self._url
        )

    async def async_update(self):
        url = self._url + "status.txt"
        session = async_get_clientsession(self.hass)
        response = await session.get(url)
        response_bytes = await response.read()
        response_body = response_bytes.decode("ascii")
        for line in response_body.splitlines():
            key, var = line.partition("=")[::2]
            if key == "JSON_BATTPERC":
                self._attr_native_value = int(var.strip('"'))
                break
