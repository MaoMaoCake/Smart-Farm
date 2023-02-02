import {writable} from "svelte/store";

export let FarmSettings = writable({
    light_schedule: [],
    ac_schedule: [],
    co2: 0,
    humidity: 0,
    watering_schedule: []
})