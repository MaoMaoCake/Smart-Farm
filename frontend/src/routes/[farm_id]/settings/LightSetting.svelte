<script lang="ts">
    import Icon from "@iconify/svelte";
    import LightSet from "./LightSet.svelte";
    import {FarmSettings, presetMap, changes} from "$lib/SettingStores.js";
    export let farm_id;

    $: {
        const values = Object.values($FarmSettings.light_schedule);
        $changes.light_schedule = !values.every(val => val.changes_type === null || val.changes_type === "NO_CHANGES");
    }

    function format_datetime(input_time){
        let timeParts = input_time.split(":");
        let hours = timeParts[0];
        let minutes = timeParts[1];

        return hours + ":" + minutes;
    }
    function addTime(){
        $FarmSettings.light_schedule = [...$FarmSettings.light_schedule,
            {
                startTime: "00:00",
                endTime: "00:00",
                farmLightPresetId: 1,
                lightAutomationId: null,
                changes_type: "CREATE"
            }]
        $FarmSettings.light_schedule = $FarmSettings.light_schedule
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
            <a href="/{farm_id}/light_list">
                <Icon icon="icon-park:setting-config" class="h-6 w-6 ml-2 bg-gray-300 p-1 rounded-full"/>
            </a>
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
            <LightSet t_start={format_datetime(time.startTime)} t_end={format_datetime(time.endTime)} preset={{name: $presetMap[time.farmLightPresetId],
                                                                    preset_id: time.farmLightPresetId}} num={i} />
        {/each}
    </div>
    <button class="btn btn-secondary ml-10 mr-10 mt-5 text-white" on:click={addTime}>Add Time</button>
</div>
