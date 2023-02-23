from .config import create_mqtt_request
from .models import AutomationInput, LightRequest, WateringRequest, ACRequest
from .enum_list import HardwareType, AutomationInputField

from response.error_codes import get_http_exception


def run_task(automation_input: AutomationInput, is_start: bool):
    print(f"Running task {automation_input.ESP_id}")
    response = create_mqtt_request(topic=str(automation_input.ESP_id), message=str(create_payload(automation_input,
                                                                                                  is_start)))

    if response.status_code != 200:
        get_http_exception('03', message='MQTT connection failed')


def validate_input(automation_input: AutomationInput):
    missing_field = []
    match automation_input.hardware_type:
        case HardwareType.LIGHT:
            if automation_input.activate is None: missing_field.append(AutomationInputField.ACTIVATE.name)
            if automation_input.uv_percent is None: missing_field.append(AutomationInputField.UV_PERCENT.name)
            if automation_input.ir_percent is None: missing_field.append(AutomationInputField.IR_PERCENT.name)
            if automation_input.natural_percent is None: missing_field.append(AutomationInputField.NATURAL_PERCENT.name)

        case HardwareType.AC:
            if automation_input.activate is None: missing_field.append(AutomationInputField.ACTIVATE.name)
            if automation_input.temperature is None: missing_field.append(AutomationInputField.TEMPERATURE.name)

        case HardwareType.WATERING:
            if automation_input.activate is None: missing_field.append(AutomationInputField.ACTIVATE.name)

    if len(missing_field) != 0:
        get_http_exception('IP400', message=f"Missing field(s) for hardware type "
                                            f"[{automation_input.hardware_type}] --> {missing_field}")


def create_payload(automation_input: AutomationInput, is_start: bool):
    match automation_input.hardware_type:
        case HardwareType.LIGHT:
            return LightRequest(activate=is_start,
                                uv_percent=automation_input.uv_percent,
                                ir_percent=automation_input.ir_percent,
                                natural_percent=automation_input.natural_percent,
                                light_combination_id=automation_input.light_combination_id
                                )
        case HardwareType.AC:
            return ACRequest(activate=is_start,
                             temperature=automation_input.temperature
                             )
        case HardwareType.WATERING:
            return WateringRequest(activate=is_start)
