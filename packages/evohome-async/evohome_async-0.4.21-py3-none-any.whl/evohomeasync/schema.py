#!/usr/bin/env python3
"""evohomeasync provides an async client for the *original* Evohome API."""

from typing import Any, Final, TypeAlias

# TCC config, status dicts
_EvoLeafT: TypeAlias = bool | float | int | str | list[str]  # Any
_DeviceDictT: TypeAlias = dict[str, Any]  # '_EvoDeviceT' | _EvoLeafT]
_EvoDictT: TypeAlias = dict[str, Any]  # '_EvoDictT' | _EvoLeafT]
_EvoListT: TypeAlias = list[_EvoDictT]
_EvoSchemaT: TypeAlias = _EvoDictT | _EvoListT

# TCC identifiers (Usr, Loc, Gwy, Sys, Zon|Dhw)
_DhwIdT: TypeAlias = int
_GatewayIdT: TypeAlias = int
_LocationIdT: TypeAlias = int
_SystemIdT: TypeAlias = int
_UserIdT: TypeAlias = int
_ZoneIdT: TypeAlias = int
_ZoneNameT: TypeAlias = str

# TCC other
_ModeT: TypeAlias = str
_SystemModeT: TypeAlias = str

_TaskIdT: TypeAlias = str  # TODO: int or str?


SZ_SESSION_ID: Final = "sessionId"  # id Id, not ID

# schema keys (start with a lower case letter)
SZ_ALLOWED_MODES: Final = "allowedModes"
SZ_CHANGEABLE_VALUES: Final = "changeableValues"
SZ_COOL_SETPOINT: Final = "coolSetpoint"
SZ_DEVICE_ID: Final = "deviceID"  # is ID, not Id
SZ_DEVICES: Final = "devices"
SZ_DOMAIN_ID: Final = "domainID"  # is ID, not Id
SZ_GATEWAY_ID: Final = "gatewayId"  # is Id, not ID
SZ_HEAT_SETPOINT: Final = "heatSetpoint"
SZ_ID: Final = "id"  # is id, not Id/ID
SZ_INDOOR_TEMPERATURE: Final = "indoorTemperature"
SZ_LOCATION_ID: Final = "locationID"  # is ID, not Id
SZ_MAC_ID: Final = "macID"  # is ID, not Id
SZ_MODE: Final = "mode"
SZ_NAME: Final = "name"
SZ_NEXT_TIME: Final = "NextTime"
SZ_QUICK_ACTION: Final = "QuickAction"
SZ_QUICK_ACTION_NEXT_TIME: Final = "QuickActionNextTime"
SZ_SETPOINT: Final = "setpoint"
SZ_SPECIAL_MODES: Final = "SpecialModes"
SZ_STATE: Final = "state"
SZ_STATUS: Final = "status"
SZ_TEMP: Final = "temp"
SZ_THERMOSTAT: Final = "thermostat"
SZ_THERMOSTAT_MODEL_TYPE: Final = "thermostatModelType"
SZ_USER_ID: Final = "userID"  # is ID, not Id
SZ_USER_INFO: Final = "userInfo"
SZ_VALUE: Final = "value"

# schema values (start with an upper case letter)
SZ_AUTO: Final = "Auto"
SZ_AUTO_WITH_ECO: Final = "AutoWithEco"
SZ_AWAY: Final = "Away"
SZ_CUSTOM: Final = "Custom"
SZ_DAY_OFF: Final = "DayOff"
SZ_HEATING_OFF: Final = "HeatingOff"
#
SZ_DHW_OFF: Final = "DHWOff"
SZ_DHW_ON: Final = "DHWOn"
#
SZ_DOMESTIC_HOT_WATER: Final = "DOMESTIC_HOT_WATER"
SZ_EMEA_ZONE: Final = "EMEA_ZONE"
#
SZ_HOLD: Final = "Hold"
SZ_SCHEDULED: Final = "Scheduled"
SZ_TEMPORARY: Final = "Temporary"
#
SZ_HEAT: Final = "Heat"
SZ_OFF: Final = "Off"
