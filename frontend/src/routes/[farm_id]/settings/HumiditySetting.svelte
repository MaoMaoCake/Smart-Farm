<script  lang="ts">
    import Icon from "@iconify/svelte";
    import {FarmSettings, changes} from "$lib/SettingStores";

    let initial_humidity = 0;
    let tooltip = false;

    $: {
        if ($FarmSettings && (initial_humidity == 0)) {
          initial_humidity = $FarmSettings.humidity;
        }
  }

    async function handleHumidityChange(){
        if ($FarmSettings.humidity == initial_humidity) {
            $changes.humidity = false;
        } else {
            $changes.humidity = true;
        }
    }
</script>
<div class="flex mt-10 justify-start w-full flex-col md: flex-row">
    <div class="flex items-center w-full relative">
        <div on:click={() => {tooltip = true}} on:mouseenter={() => {tooltip = true}} on:mouseleave={() => {tooltip = false}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-teal-900 rounded min-w-fit ml-5 pl-5 pr-5 white">Humidity Setting</p>
        <div class="divider w-full ml-2"></div>
        {#if tooltip}
            <div class="absolute left-10 top-10">
                <div class="bg-gray-300 w-56 h-64 rounded-xl relative z-30 p-5 flex justify-center items-center">
                    <div class="text-black">
                        <p>Humidity Setting</p>
                        <br>
                        <p>User can set the Maximum humidity level. Maximum humidity level can be set by clicking </p>
                        <br>
                        <p>Dehumidifier will control and maintain the set Maximum humidity level.</p>
                    </div>
                </div>
            </div>
        {/if}
    </div>
    <div class="flex justify-center items-center">
        <p class="ml-5 mr-5">Maximum Humidity Level</p>
        <input type="text"
               bind:value={$FarmSettings.humidity}
               on:input={handleHumidityChange}
               class="input w-32 bg-gray-100 text-black">
        <p class="ml-5 ">%</p>
    </div>
</div>
