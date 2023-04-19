<script lang="ts">
    import StatPreview from "$lib/StatPreview.svelte";
    import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";
    import type {PageData} from "./$types";
    import {FarmSettings} from "$lib/SettingStores";
    import {page} from "$app/stores";
    import {goto} from "$app/navigation";
    import Icon from '@iconify/svelte';
    import { PUBLIC_URL_PREFIX } from '$env/static/public'


    export let data: PageData;

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

    let farm_stats: FarmData;
    let tooltip = false;

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
  `${PUBLIC_URL_PREFIX}/api/farm/${data.farm_id}`,
  {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  })
   .then(async response => get_setting_response_handler(await response.json()))
   .catch(error => console.log('error', error));


  function get_setting_response_handler(response) {
    if (!response.successful) {
      alert(response.message);
    } else if (response.successful) {
      $FarmSettings.co2 = response.data.MinCO2Level;
      $FarmSettings.humidity = response.data.MaxHumidityLevel;
      $FarmSettings.light_schedule = response.data.LightAutomations;
      $FarmSettings.light_preset = response.data.FarmLightPresets;
      $FarmSettings.ac_schedule = response.data.ACAutomations;
      $FarmSettings.watering_schedule = response.data.WateringAutomations;
      $FarmSettings.ac_temp = response.data.ACTemp;
      $FarmSettings.watering_automation = response.data.isWateringAutomation;
    }
  }

  function create_preset(){
      fetch(
              `${PUBLIC_URL_PREFIX}/api/farm/${$page.params.farm_id}/light/preset/create_from_current?is_current_setting=false`,
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
            location.reload();
        }
  }

</script>

{#if farm_stats}
    <div class=" flex grow w-screen justify-center">
      <p class="items-center mt-5 font-bold">List of presets</p>
     <Icon icon="iconoir:light-bulb-on" class="h-5 w-5 mt-6 ml-2"/>
   </div>
    <div class="flex w-full justify-center items-center flex-col md:flex-row">
        <div class="flex flex-col grow md:w-1/3 md:h-5/6 items-center justify-center">
            <div class="flex grow md:hidden">
                <StatPreview farm_name="{farm_stats.name}" temp="{farm_stats.temp}" humidity={farm_stats.humidity}
                             light={farm_stats.light} ac="{farm_stats.ac}" humidifier={farm_stats.humidifier}
                             co2={farm_stats.co2} co2_val={farm_stats.co2_val}>
                </StatPreview>
            </div>
            <div class="hidden md:flex">
              <StatPreviewLarge farm_name="{farm_stats.name}" temp="{farm_stats.temp}" humidity={farm_stats.humidity}
                           light={farm_stats.light} ac="{farm_stats.ac}" humidifier={farm_stats.humidifier}
                           co2={farm_stats.co2} co2_val={farm_stats.co2_val} farm_id={farm_stats.farm_id} type="setting">
              </StatPreviewLarge>
            </div>
            <div class="flex grow flex-col items-center w-full pb-5">
                <div class="flex justify-evenly w-full">
                    <button class="btn bg-black text-white"
                            on:click={goto(`/${$page.params.farm_id}/settings`)}>Farm setting
                    <Icon icon="icon-park-solid:setting-two" class="h-4 w-4 ml-2"/></button>
                    <button class="btn bg-gray-300 text-black"
                            on:click={goto(`/${$page.params.farm_id}/light_list`)}>Light setting
                    <Icon icon="iconoir:light-bulb-on" class="h-5 w-5 ml-2"/></button>
                </div>
            </div>
        </div>
        <div class="fixed-box overflow-x-auto">
            <table class="table w-full">
                <!-- head -->
                <thead>
                <tr>
                    <th></th>
                    <th>Name</th>
                    <th></th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                <!-- row 1 -->
                    {#each $FarmSettings.light_preset as lp, index}
                        <tr>
                            <th>{index+1}</th>
                            <td class="text-center underline-offset-2 flex mt-3">
                                {lp.name}
                                <a href="/change_preset_name?preset_name={lp.name}&farm_id={farm_stats.farm_id}&preset_id={lp.preset_id}">
                                    <Icon icon="mdi:pen" class="h-4 w-4 ml-2 mt-1" />
                                </a>
                            </td>
                            <td></td>
                            <td>
                                <a href="/{farm_stats.farm_id}/light_preset/{lp.preset_id}/light_combination_list?farm_id={farm_stats.farm_id}&preset_name={lp.name}&preset_id={lp.preset_id}"
                                   class="btn btn-primary" >Edit</a>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>

        <div class="relative flex grow justify-center items-center mt-5 mb-10 mr-10 10flex-row">
            <div on:click={() => {tooltip = true}} on:mouseenter={() => {tooltip = true;  event.target.style.cursor = "pointer";}} on:mouseleave={() => {tooltip = false}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5 mr-5" />
        </div>
            {#if tooltip}
            <div class="absolute left-10 bottom-10">
                <div class="bg-yellow-200 w-56 h-30 rounded-xl relative z-30">
                    <div class="text-black">
                        <p>This button will create new preset with default value</p>
                        <p>Light density will be set to 50%</p>
                    </div>
                </div>
            </div>
        {/if}
        <button class="btn btn-primary md:w-1/2 "
                autocomplete="off"
                on:click={create_preset}
        >Create new preset</button>
      </div>
    </div>
{/if}

<style>
  .fixed-box {
    height: 40vh;
    overflow-y: scroll;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 0.5rem;
    text-align: center;
  }
</style>