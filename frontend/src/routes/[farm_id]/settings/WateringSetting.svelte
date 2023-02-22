<script lang="ts">
    import Icon from "@iconify/svelte";
    import WateringSet from "./WateringSet.svelte";
    import {FarmSettings} from "$lib/SettingStores.js";

    export let farm_id;

    $FarmSettings.watering_schedule = [{time_start: "09:50"},
        {time_start: "12:00"}]

    function info(type: string){
        alert(type)
    }
    function addTime(){
        $FarmSettings.watering_schedule = [...$FarmSettings.watering_schedule, {time_start: "00:00"}]
    }
</script>
<div class="flex mt-10 justify-start w-full flex-col md: flex-row">
    <div class="flex items-center w-full">
        <div on:click={() => {info("light")}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-blue-400 rounded min-w-fit ml-5 pl-5 pr-5 white">Watering Setting</p>
        <div class="divider w-full ml-2"></div>
    </div>
    <div class="flex flex-col pl-5">
        {#each $FarmSettings.watering_schedule as water, i}
            <WateringSet t_start={water.time_start} num={i}/>
        {/each}
    </div>
    <button class="btn btn-secondary ml-10 mr-10 mt-5" on:click={addTime}>Add Time</button>
</div>

<style>
    .white {
        color: white
    }
</style>