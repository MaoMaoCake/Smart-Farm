from fastapi import APIRouter
import schedule
import time as t

from response.response_dto import get_response_status, ResponseDto
from database.connector import get_all_lights_automation, get_all_AC_automation, get_all_watering_automation
from response.error_codes import get_http_exception

from .utils import run_task, validate_input
from .models import AutomationInput, DeleteAutomationInput

workerRouter = APIRouter()
tasks = {}


def run_scheduler():
    while True:
        schedule.run_pending()
        t.sleep(1)


@workerRouter.get("/", response_model=ResponseDto)
async def index():
    return get_response_status(message="Welcome to the backend-worker")


@workerRouter.post("/task", response_model=ResponseDto)
async def add_task(automation_input: AutomationInput):
    validate_input(automation_input)
    if f"{automation_input.hardware_type}_{automation_input.ESP_id}" \
       f"_{automation_input.automation_id}_start" in tasks:
        await update_task(automation_input)

    job_id = schedule.every().day.at(automation_input.start_time.strftime("%H:%M")).do(run_task, automation_input, True)
    tasks[f"{automation_input.hardware_type}_{automation_input.ESP_id}" \
          f"_{automation_input.automation_id}_start"] = {"job_id": job_id}

    if automation_input.end_time:
        job_id = schedule.every().day.at(automation_input.end_time.strftime("%H:%M")).do(run_task,
                                                                                         automation_input,
                                                                                         False)
        tasks[f"{automation_input.hardware_type}_{automation_input.ESP_id}" \
          f"_{automation_input.automation_id}_end"] = {"job_id": job_id}

    return get_response_status(message=f"Task {automation_input.ESP_id} added to run at"
                                       f" {automation_input.start_time.hour}:{automation_input.start_time.minute}"
                                       f" and {automation_input.end_time.hour}:{automation_input.end_time.minute}"
                                       if automation_input.end_time else "")


@workerRouter.put("/task", response_model=ResponseDto)
async def update_task(automation_input: AutomationInput):
    validate_input(automation_input)
    if f"{automation_input.hardware_type}_{automation_input.ESP_id}" \
          f"_{automation_input.automation_id}_start" in tasks:
        schedule.cancel_job(tasks[f"{automation_input.hardware_type}_{automation_input.ESP_id}" \
                                  f"_{automation_input.automation_id}_start"]["job_id"])

        new_job_id = schedule.every().day.at(automation_input.start_time.strftime("%H:%M"))\
            .do(run_task, automation_input, True)
        tasks[f"{automation_input.hardware_type}_{automation_input.ESP_id}" \
              f"_{automation_input.automation_id}_start"] = {"job_id": new_job_id}

        if automation_input.end_time:
            schedule.cancel_job(tasks[f"{automation_input.hardware_type}_{automation_input.ESP_id}" \
                                      f"_{automation_input.automation_id}_end"]["job_id"])

            new_job_id = schedule.every().day.at(automation_input.end_time.strftime("%H:%M"))\
                .do(run_task, automation_input, False)
            tasks[f"{automation_input.hardware_type}_{automation_input.ESP_id}" \
                  f"_{automation_input.automation_id}_end"] = {"job_id": new_job_id}

        return get_response_status(message=f"Task {automation_input.ESP_id} updated to run at"
                                           f" {automation_input.start_time.hour}:{automation_input.start_time.minute}"
                                           f" and {automation_input.end_time.hour}:{automation_input.end_time.minute}"
                                           if automation_input.end_time else "")
    else:
        return get_response_status(message=f"Task {automation_input.ESP_id} not found")


@workerRouter.delete("/task", response_model=ResponseDto)
async def delete_task(delete_automation_input: DeleteAutomationInput):
    if f"{delete_automation_input.hardware_type}_{delete_automation_input.ESP_id}" \
       f"_{delete_automation_input.automation_id}_start" in tasks:
        job_id = tasks[f"{delete_automation_input.hardware_type}_{delete_automation_input.ESP_id}" \
                       f"_{delete_automation_input.automation_id}_start"]["job_id"]
        schedule.cancel_job(job_id)
        del tasks[f"{delete_automation_input.hardware_type}_{delete_automation_input.ESP_id}" \
                  f"_{delete_automation_input.automation_id}_start"]

        end_job_id = tasks[f"{delete_automation_input.hardware_type}_{delete_automation_input.ESP_id}" \
                           f"_{delete_automation_input.automation_id}_end"]["job_id"]
        if end_job_id:
            schedule.cancel_job(end_job_id)
            del tasks[f"{delete_automation_input.hardware_type}_{delete_automation_input.ESP_id}" \
                      f"_{delete_automation_input.automation_id}_end"]

        return get_response_status(message=f"Task {delete_automation_input.ESP_id} is deleted")
    else:
        return get_http_exception(error_code='03', message=f"Task {delete_automation_input.ESP_id} not found")


async def initiate_scheduler_on_start():
    lights_automations = get_all_lights_automation()
    ACs_automations = get_all_AC_automation()
    watering_automations = get_all_watering_automation()

    for light_automation in lights_automations:
        print('initiate Light scheduler')
        print(f'create task {light_automation.ESP_id}')
        await add_task(light_automation)

    for AC_automation in ACs_automations:
        print('initiate AC scheduler')
        print(f'create task {AC_automation.ESP_id}')
        await add_task(AC_automation)

    for watering_automation in watering_automations:
        print('initiate watering scheduler')
        print(f'create task {watering_automation.ESP_id}')
        await add_task(watering_automation)
