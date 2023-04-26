<script lang="ts">
    import Icon from "@iconify/svelte";
    import ACSet from "./ACSet.svelte";
    import {FarmSettings, changes} from "$lib/SettingStores.js";

    export let farm_id;

    $: {
        const values = Object.values($FarmSettings.ac_schedule);
        $changes.ac_schedule = !values.every(val => val.changes_type === null || val.changes_type === "NO_CHANGES");
    }

    let tooltip = false;

    function format_datetime(input_time){
        let timeParts = input_time.split(":");
        let hours = timeParts[0];
        let minutes = timeParts[1];

        return hours + ":" + minutes;
    }

    function addTime(){
        $FarmSettings.ac_schedule = [...$FarmSettings.ac_schedule,
            {
                startTime: "00:00",
                endTime: "00:00",
                temperature: 25,
                ACAutomationId: null,
                changes_type: "CREATE"
            }]
        $FarmSettings.ac_schedule = $FarmSettings.ac_schedule
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
                <div class="bg-gray-300 w-56 h-64 rounded-xl relative z-30 p-5 flex justify-center items-center">
                    <div class="text-black">
                        <p>AC Settings</p>
                        <br>
                        <p>User can set the turn on and off time daily. Schedule more time can be done by clicking</p>
                        <br>
                        <p>User can set temperature from</p>
                    </div>
                </div>
            </div>
        {/if}
        <div>
            <a href="/{farm_id}/ac_list">
                <Icon icon="icon-park:setting-config" class="h-6 w-6 ml-2 bg-gray-300 p-1 rounded-full"/>
            </a>
        </div>
        <div class="divider w-full ml-2"></div>
    </div>
    <div class="flex flex-col pl-5">
        {#each $FarmSettings.ac_schedule as ac, i}
            <ACSet t_start={format_datetime(ac.startTime)} t_end={format_datetime(ac.endTime)} temp={ac.temperature} num={i}/>
        {/each}
    </div>
    <button class="btn btn-secondary ml-10 mr-10 mt-5 text-white" on:click={addTime}>Add Time</button>
</div>