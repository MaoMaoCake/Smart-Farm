<script  lang="ts">
    import { onMount, afterUpdate } from 'svelte';
    import Icon from "@iconify/svelte";
    import {FarmSettings, changes} from "$lib/SettingStores";

    let initial_co2 = 0;
    let tooltip = false;

    $: {
        if ($FarmSettings && (initial_co2 == 0)) {
          initial_co2 = $FarmSettings.co2;
        }
  }
    async function handleCo2Change(){
        console.log(initial_co2)
        if ($FarmSettings.co2 == initial_co2) {
            $changes.co2 = false;
        } else {
            $changes.co2 = true;
        }
    }

</script>
<div class="flex mt-10 justify-start w-full flex-col md: flex-row">
    <div class="flex items-center w-full relative">
        <div on:click={() => {tooltip = true}} on:mouseenter={() => {tooltip = true}} on:mouseleave={() => {tooltip = false}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-red-900 rounded min-w-fit ml-5 pl-5 pr-5 white">CO2 Setting</p>
        <div class="divider w-full ml-2"></div>
        {#if tooltip}
            <div class="absolute left-10 top-10">
                <div class="bg-gray-300 w-56 h-64 rounded-xl relative z-30 p-5 flex justify-center items-center">
                    <div class="text-black">
                        <p>CO2 Setting</p>
                        <br>
                        <p>User can set the minimum CO2 level. Minimum CO2 level can be set by clicking</p>
                        <br>
                        <p>CO2 controller will control and maintain the set minimum CO2 level.</p>
                    </div>
                </div>
            </div>
        {/if}
    </div>
    <div class="flex justify-center items-center">
        <p class="ml-5 mr-5">Minimum CO2 Level</p>
            <input type="text"
                   class="input w-32 bg-gray-100 text-black"
                   bind:value={$FarmSettings.co2}
                   on:input={handleCo2Change}>
        <p class="ml-5">PPM</p>
    </div>
</div>