<script lang="ts">
    import type { PageData } from './$types';
    import StatPreview from "$lib/StatPreview.svelte";
    import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";
    import {FarmSettings} from "$lib/SettingStores.js"
    import ACCard from "./ACCard.svelte";
    import {goto} from "$app/navigation";
    import { page } from '$app/stores';
    import Icon from '@iconify/svelte';

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

    const gray = 'gray-400';
    const blue = 'blue-900'

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
            `http://127.0.0.1:8000/farm/${$page.params.farm_id}/AC/list/`,
          {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => ac_response_handler(await response.json()))
        .catch(error => console.log('error', error));

    function ac_response_handler(response) {
        if (!response.successful) {
            goto(`/${$page.params.farm_id}/settings`);
        } else if (response.successful) {
            $FarmSettings.ac_list = response.data;
        };
    }

    let table;
    let state = localStorage.getItem('isTable');
    if (state == null) {
        localStorage.setItem('isTable', 'false');
        table = false;
    } else {
        table = (state === 'true');
    }

    $: {
        if (table) {
            localStorage.setItem('isTable', 'true');
        } else if (table == false) {
            localStorage.setItem('isTable', 'false');
        }
    }

    function update_ac_status(ac_id: number, ac_status: boolean){
      fetch(
              `http://127.0.0.1:8000/farm/${$page.params.farm_id}/AC/${ac_id}/automation?is_turn_on=${ac_status}`,
          {
              method: 'PATCH',
              headers: myHeaders,
              redirect: 'follow'
          })
      .then(async response => update_ac_status_handler(await response.json()))
      .catch(error => console.log('error', error));
  }

  function update_ac_status_handler(response) {
        if (!response.successful) {
            alert(response.message);
            location.reload();
        } else if (response.successful) {
            location.reload();
        };
  }

    function update_all_ac_status(ac_status: boolean){
      fetch(
              `http://127.0.0.1:8000/farm/${$page.params.farm_id}/AC/automation?is_turn_on=${ac_status}`,
          {
              method: 'PATCH',
              headers: myHeaders,
              redirect: 'follow'
          })
      .then(async response => update_ac_status_handler(await response.json()))
      .catch(error => console.log('error', error));
  }

</script>
{#if farm_stats}
    <div class=" flex grow w-screen justify-center">
      <p class="items-center mt-5 font-bold">AC list</p>
     <Icon icon="tabler:air-conditioning" class="h-5 w-5 mt-6 ml-2"/>
   </div>
    <div class="flex w-full justify-center items-center flex-col md:flex-row">
        <div class="flex flex-col grow md:w-1/3 md:h-5/6 items-center justify-center">
            <div class="flex grow md:hidden">
                <StatPreview farm_name="{farm_stats.name}" temp="{farm_stats.temp}" humidity={farm_stats.humidity}
                             light={farm_stats.light} ac="{farm_stats.ac}" humidifier={farm_stats.humidifier}
                             co2={farm_stats.co2} co2_val={farm_stats.co2_val} type="setting">
                </StatPreview>
            </div>
            <div class="hidden md:flex">
                <StatPreviewLarge farm_name="{farm_stats.name}" temp="{farm_stats.temp}" humidity={farm_stats.humidity}
                                  light={farm_stats.light} ac="{farm_stats.ac}" humidifier={farm_stats.humidifier}
                                  co2={farm_stats.co2} co2_val={farm_stats.co2_val} type="setting">
                </StatPreviewLarge>
            </div>
            <div class="flex grow flex-col items-center w-full pb-5">
                <p class="p-5">AC Automation Setting</p>
                <div class="flex justify-evenly w-full">
                    <button class="btn bg-black text-white"
                            on:click={() => {update_all_ac_status(false)}}>Turn Off All</button>
                    <button class="btn bg-gray-300 text-black hover:text-white"
                            on:click={() => {update_all_ac_status(true)}}>Turn On All</button>
                </div>
            </div>
        </div>
        <div class="flex grow flex-col md:w-2/3">
            <div class="flex grow md:w-10/12 justify-end w-full pl-5 pr-5">
                <button class="btn"
                        on:click={()=>{table = true}}>table</button>
                <button class="btn"
                        on:click={()=>{table = false}}>card</button>
            </div>
            <div class="flex grow w-screen md:w-10/12 items-center justify-center pt-5">
                {#if table}
                    <div class="flex grow mr-5 ml-5 rounded flex-col bg-gray-300">
                        <div class="flex grow bg-black rounded-t-md pt-2 pb-2">
                            <div class="flex grow w-1/6"></div>
                            <div class="flex grow w-1/6 white justify-center">Title</div>
                            <div class="flex grow w-1/6 white justify-center">Status</div>
                            <div class="flex grow w-1/6 white justify-center">Temperature</div>
                            <div class="flex grow w-1/6"></div>
                            <div class="flex grow w-1/6"></div>
                        </div>
                        {#each $FarmSettings.ac_list as ac, index}
                            <div class="flex grow bg-{ac.ACStatus ? blue : gray} rounded m-2 pt-2 pb-2">
                                <div class="flex grow w-1/6 white justify-center">{index + 1}.</div>
                                <div class="flex grow w-1/6 white justify-center">
                                    {ac.ACName}
                                     <a href="/change_ac_name?ac_name={ac.ACName}&farm_id={$page.params.farm_id}&ac_id={ac.ACId}">
                                        <Icon icon="mdi:pen" class="h-4 w-4 ml-2 mt-1" />
                                    </a>
                                </div>
                                <div class="flex grow w-1/6 white justify-center items-center">
                                    {#if ac.ACStatus}
                                        <td>ON</td>
                                        <span class="flex w-3 h-3 bg-green-500 rounded-full pl-3 pt-1 ml-1"></span>
                                    {:else}
                                        <td>OFF</td>
                                        <span class="flex w-3 h-3 bg-red-500 rounded-full pl-3 pt-1 ml-1"></span>
                                    {/if}
                                </div>
                                <div class="flex grow w-1/6 white justify-center">{ac.ACTemperature}</div>
                                <div class="flex grow w-1/6 white justify-center">
                                    OFF
                                    <input type="checkbox"
                                           class="toggle ml-1 mr-1"
                                           bind:checked={ac.ACStatus}
                                           on:click={() => {update_ac_status(ac.ACId, !ac.ACStatus)}}
                                    />
                                    ON
                                </div>
                                <div class="flex grow w-1/6 white justify-center"></div>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <div class="flex grow mr-5 ml-5 rounded flex-col md:flex-row flex-wrap items-center justify-center">
                        {#each $FarmSettings.ac_list as ac, index}
                            <ACCard name={ac.ACName} status={ac.ACStatus} temp={ac.ACTemperature} ac_id={ac.ACId} farm_id={$page.params.farm_id}></ACCard>
                        {/each}
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}