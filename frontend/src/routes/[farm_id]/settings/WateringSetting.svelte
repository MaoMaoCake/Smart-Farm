<script lang="ts">
    import Icon from "@iconify/svelte";
    import WateringSet from "./WateringSet.svelte";
    import {FarmSettings, changes} from "$lib/SettingStores.js";

    export let farm_id;
    const initial_watering_automation = $FarmSettings.watering_automation;
    let watering_automation_switch = $FarmSettings.watering_automation;

    $: {
        const values = Object.values($FarmSettings.watering_schedule);
        $changes.watering_schedule = !values.every(val => val.changes_type === null || val.changes_type === "NO_CHANGES");
    }

    function format_datetime(input_time){
        let timeParts = input_time.split(":");
        let hours = timeParts[0];
        let minutes = timeParts[1];

         return hours + ":" + minutes;
    }

    function addTime(){
        $FarmSettings.watering_schedule = [...$FarmSettings.watering_schedule,
            {
                wateringStartTime: "00:00",
                wateringEndTime: "00:00",
                wateringAutomationId: null,
                changes_type: "CREATE"
            }]
        $FarmSettings.watering_schedule = $FarmSettings.watering_schedule
    }

    async function handleWateringAutomationChange(){
        if ($FarmSettings.watering_automation == initial_watering_automation) {
            $changes.watering_automation = false;
        } else {
            $changes.watering_automation = true;
        }
    }

    let tooltip = false;
</script>
<div class="flex mt-10 justify-start w-full flex-col md: flex-row">
    <div class="flex items-center w-full relative">
        <div on:click={() => {tooltip = true}} on:mouseenter={() => {tooltip = true}} on:mouseleave={() => {tooltip = false}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-blue-400 rounded min-w-fit ml-5 pl-5 pr-5 white">Watering Setting</p>
        <input type="checkbox" class="toggle toggle-success ml-2 mr-1"
               bind:checked={watering_automation_switch}
               on:click={() => {
                   $FarmSettings.watering_automation = !watering_automation_switch;
                   watering_automation_switch = !watering_automation_switch;
                   handleWateringAutomationChange();
               }}/>
        <p class="ml-1 mr-1">Automation:</p>
        {#if watering_automation_switch}
            <span class="flex w-3 h-3 bg-green-500 rounded-full pl-3 pt-1"></span>
             <p class="ml-1 mr-1">ON</p>
        {:else}
            <span class="flex w-3 h-3 bg-red-500 rounded-full pl-3 pt-1"></span>
             <p class="ml-1 mr-1">OFF</p>
        {/if}
        <div class="divider w-full ml-2"></div>
        {#if tooltip}
            <div class="absolute left-10 top-10">
                <div class="bg-gray-300 w-56 h-52 rounded-xl relative z-30">
                    <div class="text-black">
                        <p>Watering Setting</p>
                        <br>
                        <p>User can set the turn on and off Automation from</p>
                        <br>
                        <p>User can set the turn on and off time daily. Schedule more time can be done by clicking </p>
                    </div>
                </div>
            </div>
        {/if}
    </div>
    <div class="flex flex-col pl-5">
        {#each $FarmSettings.watering_schedule as water, i}
            <WateringSet t_start={format_datetime(water.wateringStartTime)} num={i}/>
        {/each}
    </div>
    <button class="btn btn-secondary ml-10 mr-10 mt-5 text-white" on:click={addTime}>Add Time</button>
</div>
