import {writable} from "svelte/store";

export let FarmSettings = writable({
    farm_id: "",
    light_schedule: [],
    ac_schedule: [],
    co2: 0,
    humidity: 0,
    watering_schedule: [],
    light_preset: [],
    ac_preset: [],
})