<script lang="ts">
    import type { PageData } from '../../../../../../.svelte-kit/types/src/routes';
    import StatPreview from "$lib/StatPreview.svelte";
    import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";
    import {goto} from "$app/navigation";
    import { page } from '$app/stores';
    import Icon from '@iconify/svelte';
    import {onMount} from "svelte";
    import {dialogs} from "svelte-dialogs";

    let preset_name = null;
    let farm_id;
    let preset_id;

    onMount(() => {
      const urlParams = new URLSearchParams(window.location.search);
      preset_name = urlParams.get('preset_name');
      farm_id = urlParams.get('farm_id');
      preset_id = urlParams.get('preset_id');
    });
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
    let light_combinations;

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");
    myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

    fetch(
            `http://127.0.0.1:8000/farm/${$page.params.farm_id}/stats`,
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
            `http://127.0.0.1:8000/farm/${$page.params.farm_id}/light/preset/${$page.params.preset_id}`,
          {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => light_response_handler(await response.json()))
        .catch(error => console.log('error', error));

    function light_response_handler(response) {
        if (!response.successful) {
            goto(`/${$page.params.farm_id}/light_preset`);
        } else {
            light_combinations = response.data;
        }
    }

   async function remove(){
    if (await dialogs.confirm("Are You sure you want to delete this automation?")){
        fetch(
            `http://127.0.0.1:8000/farm/${$page.params.farm_id}/${$page.params.preset_id}`,
          {
            method: 'DELETE',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => delete_handler(await response.json()))
        .catch(error => console.log('error', error));
    }
  }

  function delete_handler(response) {
        if (!response.successful) {
            alert(response.message);
        } else {
          goto(`/${$page.params.farm_id}/light_preset`);
        }
    }

</script>
{#if farm_stats && light_combinations}
   <div class=" flex grow w-screen justify-center">
      <p class="items-center mt-5 font-bold">Preset</p>
   </div>
  <div class=" flex grow w-screen justify-center">
  <p class="items-center mt-3">{preset_name}</p>
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
              {#if light_combinations?.length}
                 {#each light_combinations as ll, index}
                  <tr >
                      <th>{index+1}</th>
                      <a href="/{$page.params.farm_id}/light_preset/{$page.params.preset_id}/light_combination_list/edit/{ll.lightCombinationId}">
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
        <button class="btn btn-primary w-10/12 md:w-1/2 mt-3"
                autocomplete="off"
                on:click={goto(`/${$page.params.farm_id}/light_preset`)}
        >Preset list</button>
        <button class="btn btn-error w-10/12 md:w-1/2 mt-3 bg-red-500 border-red-500 text-white hover:bg-red-600 hover:border-red-600"
                autocomplete="off"
                on:click={remove}
        >Delete this preset</button>
      </div>
  </div>

  </div>

{/if}