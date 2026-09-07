"""Constants for LG Hombot integration."""

from homeassistant.components.vacuum import VacuumEntityFeature


DOMAIN = "lg_hombot"

SUPPORTED_SERVICES = (
    VacuumEntityFeature.STATE
    | VacuumEntityFeature.FAN_SPEED
    | VacuumEntityFeature.START
    | VacuumEntityFeature.PAUSE
    | VacuumEntityFeature.RETURN_HOME
    | VacuumEntityFeature.STOP
)

SPEED_NORMAL = "Normal"
SPEED_TURBO = "Turbo"

SUPPORTED_SPEEDS = (
    SPEED_NORMAL,
    SPEED_TURBO
)
