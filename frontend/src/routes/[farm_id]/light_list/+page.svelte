<script lang="ts">
    import type { PageData } from './$types';
    import StatPreview from "$lib/StatPreview.svelte";
    import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";
    import {FarmSettings} from "$lib/SettingStores.js"
    import {goto} from "$app/navigation";
    import { page } from '$app/stores';
    import Icon from '@iconify/svelte';
    import { PUBLIC_URL_PREFIX } from '$env/static/public'
    import {is_register} from "../../../lib/SettingStores";

    is_register.set(false);
    interface FarmData {
        name: string,
        temp: number,
        humidity: number,
        light: boolean,
        ac: boolean,
        humidifier: boolean,
        co2_val: number,
        co2: boolean,
        farm_id: number
    }

    export let data: PageData
    let farm_stats: FarmData;

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");
    myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

    fetch(
            `${PUBLIC_URL_PREFIX}/api/farm/${$page.params.farm_id}/stats`,
          {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => response_handler(await response.json()))
        .catch(error => console.log('error', error));

    function response_handler(response) {
        if (!response.successful) {
            goto(`/login`);
        } else if (response.successful) {
            farm_stats = {
                name: response.data.farmName,
                temp: response.data.temperature,
                humidity: response.data.humidityLevel,
                light: response.data.lightStatus,
                ac: response.data.ACStatus,
                humidifier: response.data.dehumidifierStatus,
                co2_val: response.data.CO2Level,
                co2: response.data.CO2controllerStatus,
                farm_id: response.data.farmId,
            }
        };
  }

  fetch(
            `${PUBLIC_URL_PREFIX}/api/farm/${$page.params.farm_id}/light/list`,
          {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => light_response_handler(await response.json()))
        .catch(error => console.log('error', error));

    function light_response_handler(response) {
        if (!response.successful) {
            goto(`/${$page.params.farm_id}/settings`);
        } else if (response.successful) {
            $FarmSettings.light_list = response.data;
        };
    }

  function create_preset(){
      fetch(
              `${PUBLIC_URL_PREFIX}/api/farm/${$page.params.farm_id}/light/preset/create_from_current?is_current_setting=true`,
          {
              method: 'POST',
              headers: myHeaders,
              redirect: 'follow'
          })
      .then(async response => create_preset_handler(await response.json()))
      .catch(error => console.log('error', error));
  }

  function create_preset_handler(response) {
        if (!response.successful) {
            alert(response.message);
        } else if (response.successful) {
            goto(`/${$page.params.farm_id}/light_preset`);
        };
  }

</script>
{#if farm_stats}
   <div class=" flex grow w-screen justify-center">
      <p class="items-center mt-5 font-bold">Light list</p>
     <Icon icon="iconoir:light-bulb-on" class="h-5 w-5 mt-6 ml-2"/>
   </div>
   <div class="flex w-full justify-center items-center flex-col md:flex-row md:flex-wrap">

  <div class="md:w-1/3 items-center justify-center">
    <div class="flex grow md:hidden">
     <StatPreview farm_name="{farm_stats.name}" temp="{farm_stats.temp}" humidity={farm_stats.humidity}
                 light={farm_stats.light} ac="{farm_stats.ac}" humidifier={farm_stats.humidifier}
                 co2={farm_stats.co2} co2_val={farm_stats.co2_val} farm_id={farm_stats.farm_id} type="setting">
     </StatPreview>
    </div>
   <div class="hidden md:flex">
      <StatPreviewLarge farm_name="{farm_stats.name}" temp="{farm_stats.temp}" humidity={farm_stats.humidity}
                   light={farm_stats.light} ac="{farm_stats.ac}" humidifier={farm_stats.humidifier}
                   co2={farm_stats.co2} co2_val={farm_stats.co2_val} farm_id={farm_stats.farm_id} type="setting">
      </StatPreviewLarge>
    </div>
    </div>
    <div class="overflow-x-auto w-full md:w-1/2 md:w-1/3">
      <table class="table w-full">
          <!-- head -->
          <thead>
          <tr>
              <th></th>
              <th class="text-center">Name</th>
              <th class="text-center">natural Light</th>
              <th class="text-center">UV Light</th>
              <th class="text-center">Infrared Light</th>
          </tr>
          </thead>
          <tbody>
          <!-- row 1 -->
              {#if $FarmSettings.light_list?.length}
                 {#each $FarmSettings.light_list as ll, index}
                  <tr >
                      <th>{index+1}</th>
                      <a href="/{$page.params.farm_id}/light_list/edit/{$FarmSettings.light_list[index].lightId}">
                        <td class="underline text-center underline-offset-2 flex">{ll.lightName}
                          <Icon icon="icon-park-solid:setting-two" class="h-4 w-4 ml-2 mt-1"/>
                        </td>
                      </a>
                      <td class="text-center"> {ll.naturalLightDensity} %</td>
                      <td class="text-center">{ll.UVLightDensity} %</td>
                      <td class="text-center ">{ll.IRLightDensity} %</td>
                  </tr>
              {/each}
              {/if}
          </tbody>
      </table>

      <div class="relative flex grow justify-center items-center mt-10 flex-col">
        <button class="btn btn-primary w-10/12 md:w-1/2 bg-black border-black text-white hover:bg-gray-500  hover:border-gray-500 hover:text-black"
                autocomplete="off"
                on:click={create_preset}
        >Create preset from current setting</button>
        <button class="btn btn-primary w-10/12 md:w-1/2 mt-3"
                autocomplete="off"
                on:click={goto(`/${$page.params.farm_id}/light_preset`)}
        >Preset list</button>
      </div>


  </div>

  </div>

{/if}