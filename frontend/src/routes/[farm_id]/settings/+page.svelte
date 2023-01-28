<script lang="ts">
  import type { PageData } from './$types';
  import StatPreview from "$lib/StatPreview.svelte";
  import Icon from "@iconify/svelte";
  import {beforeUpdate} from "svelte";
  import { invalidate, invalidateAll } from "$app/navigation"

  export let data: PageData;
  let light_switch, ac_switch, humidifier_switch, farm_data;
  $: light_switch = data.farm_data.light
  $: ac_switch = data.farm_data.ac
  $: humidifier_switch = data.farm_data.humidifier
  beforeUpdate(() => {
    // This makes the load function run again, this will update the state on our page
    invalidateAll()
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
</script>

<div class="flex w-screen justify-center items-center flex-col md:flex-row">
    <div>
        <StatPreview farm_name="{data.farm_data.name}" temp="{data.farm_data.temp}" humidity={data.farm_data.humidity}
                     light={data.farm_data.light} ac="{data.farm_data.ac}" humidifier={data.farm_data.humidifier}
                     co2={data.farm_data.co2} co2_val={data.farm_data.co2_val}>
        </StatPreview>
    </div>
    <div class="flex justify-evenly w-screen">
        <div class="flex justify-center grow space-between">
            {#if light_switch}
                <Icon icon="iconoir:light-bulb-on" class="h-7 w-7"/>
            {:else}
                <Icon icon="iconoir:light-bulb-off" class="h-7 w-7"/>
            {/if}
            <input type="checkbox" class="toggle toggle-success" bind:checked={light_switch} on:click={() => {toggle_switch("light", data.farm_id, light_switch)}}/>
        </div>
        <div class="flex justify-center grow">
            <Icon icon="tabler:air-conditioning" class="h-7 w-7"/>
            <input type="checkbox" class="toggle toggle-success" bind:checked={ac_switch} on:click={() => {toggle_switch("ac", data.farm_id, ac_switch)}}/>
        </div>
        <div class="flex justify-center grow">
            <Icon icon="mdi:air-humidifier" class="h-7 w-7"/>
            <input type="checkbox" class="toggle toggle-success" bind:checked={humidifier_switch} on:click={() => {toggle_switch("humidifier", data.farm_id, humidifier_switch)}}/>
        </div>
    </div>
</div>