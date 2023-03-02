<script lang="ts">
    import Icon from "@iconify/svelte";
    import ACSet from "./ACSet.svelte";
    import {FarmSettings} from "$lib/SettingStores.js";

    export let farm_id;

    let tooltip = false;
    $FarmSettings.ac_schedule = [{time_start: "09:50", time_end: "12:00", temp: 25},
        {time_start: "12:00", time_end: "14:00", temp: 26}]

    function addTime(){
        $FarmSettings.ac_schedule = [...$FarmSettings.ac_schedule, {time_start: "00:00", time_end: "00:00", temp: 0}]
    }
</script>
<div class="flex mt-10 justify-start w-full flex-col md: flex-row">
    <div class="flex items-center w-full relative">
        <div on:click={() => {tooltip = true}} on:mouseenter={() => {tooltip = true}} on:mouseleave={() => {tooltip = false}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-blue-900 rounded min-w-fit ml-5 pl-5 pr-5 white">AC Setting</p>
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
        <div>
            <a href="/{farm_id}/ac_list">
                <Icon icon="icon-park:setting-config" class="h-5 w-5 ml-2"/>
            </a>
        </div>
        <div class="divider w-full ml-2"></div>
    </div>
    <div class="flex flex-col pl-5">
        {#each $FarmSettings.ac_schedule as ac, i}
            <ACSet t_start={ac.time_start} t_end={ac.time_end} temp={ac.temp} num={i}/>
        {/each}
    </div>
    <button class="btn btn-secondary ml-10 mr-10 mt-5 text-white" on:click={addTime}>Add Time</button>
</div>