from enum import Enum


class HardwareType(str, Enum):
    LIGHT = "light"
    AC = "AC"
    CO2_SENSOR = "CO2Sensor"
    CO2_CONTROLLER = "CO2Controller"
    DEHUMIDIFIER = "dehumidifier"
    HUMIDITY_SENSOR = "humiditySensor"
    TEMPERATURE_SENSOR = "temperatureSensor"
    WATERING = "watering"


class ESPType(str, Enum):
    SENSOR = "sensor"
    CO2_CONTROLLER = "co2_controller"
    LIGHT_CONTROLLER = "light_controller"
    AC_CONTROLLER = "ac_controller"
    DEHUMIDIFIER_CONTROLLER = "dehumidifier_controller"
    WATERING_SYSTEM = "watering_system"


class AutomationInputField(str, Enum):
    ACTIVATE = "activate"
    UV_PERCENT = "uv_percent"
    IR_PERCENT = "ir_percent"
    NATURAL_PERCENT = "natural_percent"
    CO2_THRESHOLD = "co2_threshold"
    HUMIDITY_THRESHOLD = "humidity_threshold"
    TEMPERATURE = "temperature"
