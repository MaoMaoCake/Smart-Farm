export type LightScheduleType = {
    time_start: string,
    time_end: string,
    preset: string
}

export type ACScheduleType = {
    time_start: string,
    time_end: string,
    temperature: string
}

export type WateringScheduleType ={
    time_start: string
}

export type FarmSettingType = {
    light_schedule: LightScheduleType[],
    ac_schedule: ACScheduleType[],
    co2: number,
    humidity: number,
    watering_schedule: WateringScheduleType[]
}