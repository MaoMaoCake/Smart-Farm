import {writable} from "svelte/store";

export let FarmSettings = writable({
    farm_id: "1",
    light_schedule: [],
    ac_schedule: [],
    co2: 0,
    humidity: 0,
    watering_schedule: [],
    light_preset: [],
    ac_preset: [15, 16, 17, 18, 19 ,20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    light_list: [],
    ac_list: [],
    ac_temp: 0,
    watering_automation: true
})

export let presetMap = writable({})

export let changes = writable({
    water_automation: false,
    ac_schedule: false,
    light_schedule: false,
    watering_schedule: false,
    humidity: false,
    co2: false
})


export let default_changes = writable({
    water_automation: false,
    ac_schedule: false,
    light_schedule: false,
    watering_schedule: false,
    humidity: false,
    co2: false
})

export let logged_in = writable(!(localStorage.getItem("token") == null || localStorage.getItem("token") === undefined))
export let is_register = writable(true)
export let is_verify = writable(false)