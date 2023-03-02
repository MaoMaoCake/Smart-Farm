import {writable} from "svelte/store";

export let FarmSettings = writable({
    farm_id: "1",
    light_schedule: [],
    ac_schedule: [],
    co2: 0,
    humidity: 0,
    watering_schedule: [],
    light_preset: [],
    ac_preset: [],
    light_list: [],
    ac_list: []
})

export let logged_in = writable(!(localStorage.getItem("token") == null || localStorage.getItem("token") === undefined))