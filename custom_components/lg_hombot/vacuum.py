from __future__ import annotations

from typing import Any
from urllib.parse import quote

from homeassistant.components.vacuum import StateVacuumEntity, VacuumActivity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    SPEED_NORMAL,
    SPEED_TURBO,
    SUPPORTED_SERVICES,
    SUPPORTED_SPEEDS,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup of Entry."""
    # get url of hombot
    url = config_entry.data.get("url")
    name = config_entry.data.get("name")

    # create instance
    hombot_vac = HombotVacuum(name, url)
    async_add_entities([hombot_vac])


class HombotVacuum(StateVacuumEntity):
    """Representation of a Hombot vacuum cleaner robot."""

    def __init__(self, name: str, url: str) -> None:
        """Initialize the vacuum."""
        self._name = name
        self._attr_name = name
        self._attr_supported_features = SUPPORTED_SERVICES

        self._url = url

        self._activity = VacuumActivity.IDLE
        self._battery_level = None
        self._fan_speed = SPEED_NORMAL
        self._fan_speed_list = SUPPORTED_SPEEDS

        self._attr_unique_id = "hombot_" + self._url

    @property
    def unique_id(self) -> str | None:
        return self._attr_unique_id

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=self._name,
            manufacturer="LG",
            model="Hombot",
            configuration_url=self._url,
        )
        return device_info

    @property
    def activity(self) -> VacuumActivity:
        """Return the activity of the vacuum."""
        return self._activity

    @property
    def battery_level(self) -> int:
        """Return the status of the vacuum."""
        return self._battery_level

    @property
    def fan_speed(self) -> str | None:
        return self._fan_speed

    @property
    def fan_speed_list(self) -> list[str]:
        return self._fan_speed_list

    async def async_update(self) -> None:
        """Update status properties."""
        # generate url
        url = self._url + "status.txt"

        # execute command
        session = async_get_clientsession(self.hass)
        response = await session.get(url)
        response_bytes = await response.read()
        response_body = response_bytes.decode("ascii")

        # parse body
        attributes = {}
        for line in response_body.splitlines():
            name, var = line.partition("=")[::2]
            attributes[name] = var.strip('"')

        # assign properties
        self._activity = self.convert_state(attributes.get("JSON_ROBOT_STATE"))
        self._battery_level = int(attributes.get("JSON_BATTPERC", "0"))

        if attributes.get("JSON_TURBO") == "true":
            self._fan_speed = SPEED_TURBO
        else:
            self._fan_speed = SPEED_NORMAL

    def convert_state(self, current_state: str | None) -> VacuumActivity:
        """Convert the Hombot status to Home Assistant VacuumActivity."""
        match current_state:
            case "CHARGING":
                return VacuumActivity.DOCKED
            case "BACKMOVING_INIT":
                return VacuumActivity.CLEANING
            case "WORKING":
                return VacuumActivity.CLEANING
            case "PAUSE":
                return VacuumActivity.PAUSED
            case "HOMING":
                return VacuumActivity.RETURNING
            case "DOCKING":
                return VacuumActivity.RETURNING
            case _:
                return VacuumActivity.IDLE

    async def async_start(self, **kwargs: Any) -> None:
        """Turn the vacuum on."""
        self._activity = VacuumActivity.CLEANING
        await self.query('{"COMMAND":"CLEAN_START"}')

    async def async_pause(self, **kwargs: Any) -> None:
        """Turn the vacuum on."""
        self._activity = VacuumActivity.PAUSED
        await self.query('{"COMMAND":"PAUSE"}')

    async def async_return_to_base(self, **kwargs: Any) -> None:
        """Turn the vacuum off."""
        self._activity = VacuumActivity.RETURNING
        await self.query('{"COMMAND":"HOMING"}')

    async def async_stop(self, **kwargs: Any) -> None:
        """Turn the vacuum off."""
        self._activity = VacuumActivity.RETURNING
        await self.query('{"COMMAND":"HOMING"}')

    async def async_set_fan_speed(self, fan_speed: str, **kwargs: Any) -> None:
        """Sets fan speed."""
        self._fan_speed = fan_speed

        if fan_speed == SPEED_TURBO:
            await self.query('{"COMMAND":{"TURBO":"true"}}')
        else:
            await self.query('{"COMMAND":{"TURBO":"false"}}')

    async def query(self, command: str) -> bool:
        """Execute command."""
        # generate url
        url = self._url + "json.cgi?" + quote(command)

        # execute command
        session = async_get_clientsession(self.hass)
        response = await session.get(url)
        await response.read()

        return True
