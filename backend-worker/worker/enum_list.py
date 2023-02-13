from enum import Enum


class HardwareType(str, Enum):
    LIGHT = "LIGHT"
    AC = "AC"
    CO2_SENSOR = "CO2_SENSOR"
    CO2_CONTROLLER = "CO2_CONTROLLER"
    DEHUMIDIFIER = "DEHUMIDIFIER"
    HUMIDITY_SENSOR = "HUMIDITY_SENSOR"
    TEMPERATURE_SENSOR = "TEMPERATURE_SENSOR"
    WATERING = "WATERING"


class ESPType(str, Enum):
    SENSOR = "SENSOR"
    CO2_CONTROLLER = "CO2_CONTROLLER"
    LIGHT_CONTROLLER = "LIGHT_CONTROLLER"
    AC_CONTROLLER = "AC_CONTROLLER"
    DEHUMIDIFIER_CONTROLLER = "DEHUMIDIFIER_CONTROLLER"
    WATERING_SYSTEM = "WATERING_SYSTEM"


class AutomationInputField(str, Enum):
    ACTIVATE = "activate"
    UV_PERCENT = "uv_percent"
    IR_PERCENT = "ir_percent"
    NATURAL_PERCENT = "natural_percent"
    CO2_THRESHOLD = "co2_threshold"
    HUMIDITY_THRESHOLD = "humidity_threshold"
    TEMPERATURE = "temperature"
