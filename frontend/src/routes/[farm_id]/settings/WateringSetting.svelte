<script lang="ts">
    import Icon from "@iconify/svelte";
    import WateringSet from "./WateringSet.svelte";
    import {FarmSettings} from "$lib/SettingStores.js";

    export let farm_id;

    $FarmSettings.watering_schedule = [{time_start: "09:50"},
        {time_start: "12:00"}]

    function addTime(){
        $FarmSettings.watering_schedule = [...$FarmSettings.watering_schedule, {time_start: "00:00"}]
    }

    let tooltip = false;
</script>
<div class="flex mt-10 justify-start w-full flex-col md: flex-row">
    <div class="flex items-center w-full relative">
        <div on:click={() => {tooltip = true}} on:mouseenter={() => {tooltip = true}} on:mouseleave={() => {tooltip = false}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-blue-400 rounded min-w-fit ml-5 pl-5 pr-5 white">Watering Setting</p>
        <div class="divider w-full ml-2"></div>
        {#if tooltip}
            <div class="absolute left-10 top-10">
                <div class="bg-yellow-200 w-56 h-52 rounded-xl relative z-30">
                    <div class="text-black">
                        <p>This is a button</p>
                        <p>this button is very very cool</p>
                    </div>
                </div>
            </div>
        {/if}
    </div>
    <div class="flex flex-col pl-5">
        {#each $FarmSettings.watering_schedule as water, i}
            <WateringSet t_start={water.time_start} num={i}/>
        {/each}
    </div>
    <button class="btn btn-secondary ml-10 mr-10 mt-5 text-white" on:click={addTime}>Add Time</button>
</div>