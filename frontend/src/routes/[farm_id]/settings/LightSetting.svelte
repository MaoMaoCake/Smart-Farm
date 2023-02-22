<script lang="ts">
    import Icon from "@iconify/svelte";
    import LightSet from "./LightSet.svelte";
    import {FarmSettings} from "$lib/SettingStores.js";
    export let farm_id;

    $FarmSettings.light_schedule = [{time_start: "08:50", time_end: "12:00", preset: "preset1"},
                    {time_start: "12:00", time_end: "14:00", preset: "preset2"}]

    function addTime(){
        $FarmSettings.light_schedule = [...$FarmSettings.light_schedule, {time_start: "00:00", time_end: "00:00", preset: "null"}]
    }
    let tooltip = false;
</script>
<div class="flex mt-10 justify-start w-full flex-col">
    <div class="flex items-center w-full relative">
        <div on:click={() => {tooltip = true}} on:mouseenter={() => {tooltip = true}} on:mouseleave={() => {tooltip = false}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-amber-500 rounded min-w-fit ml-5 pl-5 pr-5 white">Light Setting</p>
        <div>
            <a href="/{farm_id}/light_list"><Icon icon="icon-park:setting-config" class="h-5 w-5 ml-2"/></a>
        </div>
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
        {#each $FarmSettings.light_schedule as time, i}
            <LightSet t_start={time.time_start} t_end={time.time_end} preset={time.preset} num={i} />
        {/each}
    </div>
    <button class="btn btn-secondary ml-10 mr-10 mt-5 text-white" on:click={addTime}>Add Time</button>
</div>