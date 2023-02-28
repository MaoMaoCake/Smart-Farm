<script lang="ts">
  import type { PageData } from './$types';
  import StatPreview from "$lib/StatPreview.svelte";
  import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";
  import Icon from "@iconify/svelte";
  import {beforeUpdate, onMount} from "svelte";
  import { invalidateAll } from "$app/navigation"
  import LightSetting from "./LightSetting.svelte";
  import ACSetting from "./ACSetting.svelte";
  import CO2Setting from "./CO2Setting.svelte";
  import HumiditySetting from "./HumiditySetting.svelte";
  import WateringSetting from "./WateringSetting.svelte";

  // The following fetches the data for the farm denoted by the farm id in the path
  // parameter.
  export let data: PageData;
  let light_switch, ac_switch, humidifier_switch;
  $: light_switch = data.farm_data.light
  $: ac_switch = data.farm_data.ac
  $: humidifier_switch = data.farm_data.humidifier
  let settings
  // This makes our app respond to changes
  onMount(() => {
      // get the farm's current settings:
      // let settings;
      // await fetch (something)
      // set settings = the thing we fetched
  })
  beforeUpdate(() => {
    // This makes the load function run again, this will update the state on our page
    invalidateAll();
  })
  function toggle_switch(type: string, farm_id: string, state: boolean){
      // integration to the api to turn on and off the lights goes here
    if (type == "light"){
        data.farm_data.light = !state;
    }
    else if (type == "ac"){
        data.farm_data.ac = !state
    }
    else if ( type == "humidifier"){
        data.farm_data.humidifier = !state
    }
  }

  function save_settings(){
      // check if data in settings var == FarmSettings Store
      // if equal do nothing
      // else write changes to DB
  }
</script>

<div class="flex w-full justify-center items-center flex-col md:flex-row">
    <div class="flex flex-col grow md:w-1/3 md:h-5/6 items-center justify-center">
        <div class="flex grow md:hidden">
            <StatPreview farm_name="{data.farm_data.name}" temp="{data.farm_data.temp}" humidity={data.farm_data.humidity}
                         light={data.farm_data.light} ac="{data.farm_data.ac}" humidifier={data.farm_data.humidifier}
                         co2={data.farm_data.co2} co2_val={data.farm_data.co2_val}>
            </StatPreview>
        </div>
        <div class="hidden md:flex">
            <StatPreviewLarge farm_name="{data.farm_data.name}" temp="{data.farm_data.temp}" humidity={data.farm_data.humidity}
                         light={data.farm_data.light} ac="{data.farm_data.ac}" humidifier={data.farm_data.humidifier}
                         co2={data.farm_data.co2} co2_val={data.farm_data.co2_val}>
            </StatPreviewLarge>
        </div>
        <div class="flex justify-evenly w-full grow">
            <div class="flex justify-center grow items-center white ">
                {#if light_switch}
                    <Icon icon="iconoir:light-bulb-on" class="h-9 w-9 bg-amber-500 p-2 mr-1 rounded-lg"/>
                {:else}
                    <Icon icon="iconoir:light-bulb-off" class="h-9 w-9 bg-amber-500 p-2 mr-1 rounded-lg"/>
                {/if}
                <input type="checkbox" class="toggle toggle-success" bind:checked={light_switch} on:click={() => {toggle_switch("light", data.farm_id, light_switch)}}/>
            </div>
            <div class="flex justify-center grow items-center white">
                {#if ac_switch}
                    <Icon icon="tabler:air-conditioning" class="h-9 w-9 bg-blue-900 p-2 mr-1 rounded-lg"/>
                {:else}
                    <Icon icon="tabler:air-conditioning-disabled" class="h-9 w-9 bg-blue-900 p-2 mr-1 rounded-lg"/>
                {/if}
                <input type="checkbox" class="toggle toggle-success" bind:checked={ac_switch} on:click={() => {toggle_switch("ac", data.farm_id, ac_switch)}}/>
            </div>
            <div class="flex justify-center grow items-center white">
                {#if humidifier_switch}
                    <Icon icon="mdi:air-humidifier" class="h-9 w-9 bg-teal-900 p-2 mr-1 rounded-lg"/>
                {:else}
                    <Icon icon="mdi:air-humidifier" class="h-9 w-9 bg-teal-900 p-2 mr-1 rounded-lg"/>
                {/if}
                <input type="checkbox" class="toggle toggle-success" bind:checked={humidifier_switch} on:click={() => {toggle_switch("humidifier", data.farm_id, humidifier_switch)}}/>
            </div>
        </div>
    </div>
    <div class="flex w-full flex-col md:flex-row md:flex-wrap grow md:pl-10 md:pr-10">
        <div class="flex flex-col grow">
            <div class="flex">
                <LightSetting farm_id={data.farm_id}/>
            </div>
            <div class="flex">
                <ACSetting farm_id={data.farm_id}/>
            </div>
            <div class="pb-44 hidden md:block"></div> <!-- spacer for save button in desktop -->
        </div>
        <div class="flex flex-col grow">
            <div class="flex">
                <CO2Setting farm_id={data.farm_id}/>
            </div>
            <div class="flex">
                <HumiditySetting farm_id={data.farm_id}/>
            </div>
            <div class="flex">
                <WateringSetting farm_id={data.farm_id}/>
            </div>
        </div>
        <div class="pb-40 md:hidden"></div> <!-- spacer for bottom -->
    </div>
</div>
<div class=" flex grow w-screen justify-center fixed bottom-10">
    <button class="btn btn-primary w-10/12 md:w-1/2" on:click={save_settings}>Save</button>
</div>