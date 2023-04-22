<script lang="ts">
  import type { PageData } from './$types';
  import StatPreview from "$lib/StatPreview.svelte";
  import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";
  import {FarmSettings, presetMap, changes} from "$lib/SettingStores.js";
  import Icon from "@iconify/svelte";
  import {beforeUpdate, onMount} from "svelte";
  import {goto, invalidateAll} from "$app/navigation"
  import LightSetting from "./LightSetting.svelte";
  import ACSetting from "./ACSetting.svelte";
  import CO2Setting from "./CO2Setting.svelte";
  import HumiditySetting from "./HumiditySetting.svelte";
  import WateringSetting from "./WateringSetting.svelte";
  import { PUBLIC_URL_PREFIX } from '$env/static/public'
  import {is_register} from "../../../lib/SettingStores";

    is_register.set(false);

  // The following fetches the data for the farm denoted by the farm id in the path
  // parameter.
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
        // ac_temp?: number
    }

  export let data: PageData;
  let light_switching, ac_switching, humidifier_switching;
  let light_switch = true;
  let ac_switch = true;
  let humidifier_switch = true;
  let settings;
  let farm_stats: FarmData;
  let ac_temp_original = 25;

  $: light_switching = light_switch;
  $: ac_switching = ac_switch;
  $: humidifier_switching = humidifier_switch;
  let isDisabled = true;
  let done = false;
  let isLoading = false;

  $: {
    const values = Object.values($changes);
    isDisabled = values.every(val => val === false);
  }

  const myHeaders = new Headers();
  myHeaders.append("Origin", "");
  myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

  onMount(() => {
   fetch(
      `${PUBLIC_URL_PREFIX}/api/farm/${data.farm_id}/stats`,
      {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
      })
    .then(async response => {
        response_handler(await response.json())
    })
    .catch(error => console.log('error', error));

  fetch(
      `${PUBLIC_URL_PREFIX}/api/farm/${data.farm_id}`,
      {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
      })
    .then(async response => get_setting_response_handler(await response.json()))
    .catch(error => console.log('error', error));
    })


  function response_handler(response) {
        if (!response.successful) {
          goto('/login');
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
                ac_temp: response.data.ACTemperature
            }

            $FarmSettings.ac_temp = response.data.ACTemperature;
            light_switch = farm_stats.light;
            ac_switch = farm_stats.ac;
            humidifier_switch = farm_stats.humidifier;
        };
  }

  // beforeUpdate(() => {
  //   // This makes the load function run again, this will update the state on our page
  //   invalidateAll();
  // })

  function control_actuators(type: string, farm_id: string, state: boolean){
    fetch(
          `${PUBLIC_URL_PREFIX}/api/farm/${data.farm_id}/${type}/control?is_turn_on=${!state}&temperature=${$FarmSettings.ac_temp}`,
          {
            method: 'POST',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => control_response_handler(await response.json(), type, state))
        .catch(error => console.log('error', error));
  }

  function convert_to_local_time(utc_time: string){
      const date = new Date(`1970-01-01T${utc_time}Z`);

    const localTimeString = date.toLocaleTimeString("en-US", {
      hour12: false,
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    });
    return localTimeString

  }

  function convert_to_utc_time(local_time: string){
    const localDate = new Date(`1970-01-01T${local_time}`);

    const utcTimeString = new Date(Date.UTC(
      1970, 0, 1,
      localDate.getUTCHours(), localDate.getUTCMinutes(), localDate.getUTCSeconds()
    )).toISOString().substr(11, 8);

    return utcTimeString
  }

  function control_response_handler(response, type: string, state: boolean) {
    if (!response.successful) {
      alert(response.message);
      switch (type){
          case "light":
              light_switch = !light_switch;
              break;
          case "ac":
              ac_switch = !ac_switch;
              break;
          case "dehumidifier":
              humidifier_switch = !humidifier_switch;
              break;
      }

    } else if (response.successful) {
      if (type == "light"){
        farm_stats.light = !state;
      }
      else if (type == "ac"){
        farm_stats.ac = !state;
      }
      else if ( type == "dehumidifier"){
        farm_stats.humidifier = !state;
      }
    }
  }

  function get_setting_response_handler(response) {
    if (!response.successful) {
      alert(response.message);
    } else if (response.successful) {
      $FarmSettings.co2 = response.data.MinCO2Level;
      $FarmSettings.humidity = response.data.MaxHumidityLevel;

      $FarmSettings.light_preset = response.data.FarmLightPresets;
      // $FarmSettings.ac_temp = response.data.ACTemp;
      $FarmSettings.watering_automation = response.data.isWateringAutomation;

      $FarmSettings.light_schedule = response.data.LightAutomations.map(object => {
          return {
              changes_type: null,
              farmLightPresetId: object.farmLightPresetId,
              lightAutomationId: object.lightAutomationId,
             startTime : convert_to_local_time(object.startTime),
              endTime : convert_to_local_time(object.endTime)
          }
      })
      $FarmSettings.ac_schedule = response.data.ACAutomations.map(object => {
         return {
              changes_type: null,
              temperature: object.temperature,
              ACAutomationId: object.ACAutomationId,
             startTime : convert_to_local_time(object.startTime),
              endTime : convert_to_local_time(object.endTime)
          }
      })
      $FarmSettings.watering_schedule =  response.data.WateringAutomations.map(object => {
           return {
               changes_type: null,
               wateringAutomationId: object.wateringAutomationId,
               wateringStartTime : convert_to_local_time(object.wateringStartTime),
               wateringEndTime: convert_to_local_time(object.wateringEndTime),
          }
      })

      response.data.FarmLightPresets.forEach(preset => {
          $presetMap[preset.preset_id] = preset.name;
      })

      ac_temp_original = $FarmSettings.ac_temp;
      done = true;
    }
  }

  async function handleACTempChange(){
        if ($FarmSettings.ac_temp != ac_temp_original) {
            fetch(
                  `${PUBLIC_URL_PREFIX}/api/farm/${data.farm_id}/AC/temperature/change?is_turn_on=${ac_switch}&temperature=${$FarmSettings.ac_temp}`,
                  {
                    method: 'PATCH',
                    headers: myHeaders,
                    redirect: 'follow'
                  })
                .then(async response => change_temp_handler(await response.json()))
                .catch(error => console.log('error', error));
                }
    }

     function change_temp_handler(response) {
        if (!response.successful) {
            $FarmSettings.ac_temp = ac_temp_original;
            alert(response.message)
            goto(`/${data.farm_id}/settings`);
        } else {
            ac_temp_original = $FarmSettings.ac_temp;
        }
  }

  function save_settings(){
      const myHeaders = new Headers();
      myHeaders.append("Origin", "");
      myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);
      myHeaders.append('Content-Type', 'application/json');
    console.log($FarmSettings.watering_schedule)
      const input_data = {
          MinCO2Level: $changes.co2 ? $FarmSettings.co2: null,
          MaxHumidityLevel: $changes.humidity ? $FarmSettings.humidity: null,
          isWateringAutomation: $FarmSettings.watering_automation,

           LightAutomations:  $FarmSettings.light_schedule.map(object => {
          return {
              changes_type: object.changes_type,
              farmLightPresetId: object.farmLightPresetId,
              lightAutomationId: object.lightAutomationId,
             startTime : convert_to_utc_time(object.startTime),
              endTime : convert_to_utc_time(object.endTime)
          }
      }),
      ACAutomations : $FarmSettings.ac_schedule.map(object => {
         return {
              changes_type: object.changes_type,
              temperature: object.temperature,
              ACAutomationId: object.ACAutomationId,
             startTime : convert_to_utc_time(object.startTime),
              endTime : convert_to_utc_time(object.endTime)
          }
      }),
      WateringAutomations:  $FarmSettings.watering_schedule.map(object => {
           return {
               changes_type: object.changes_type,
               wateringAutomationId: object.wateringAutomationId,
               wateringStartTime : convert_to_utc_time(object.wateringStartTime),
               wateringEndTime: convert_to_utc_time(object.wateringEndTime),
          }
      })

      }

      fetch(
              `${PUBLIC_URL_PREFIX}/api/farm/${data.farm_id}`,
          {
              method: 'PATCH',
              headers: myHeaders,
              body: JSON.stringify(input_data),
              redirect: 'follow'
          })
      .then(async response => change_setting_handler(await response.json()))
      .catch(error => console.log('error', error));
  }

  async function change_setting_handler(response) {
        if (!response.successful) {
            alert(response.message)
        } else {
            isLoading = true;
              setTimeout(() => {
                location.reload();
          }, 5000);
    }
  }

</script>
{#if farm_stats && done}
    {#if isLoading}
      <div class="loading-ring-overlay">
        <div class="loading-ring"></div>
      </div>
    {/if}
    <div class="flex w-full justify-center items-center flex-col md:flex-row">
        <div class="flex flex-col grow md:w-1/3 md:h-5/6 items-center justify-center">
            <div class="flex grow md:hidden">
                <StatPreview farm_name="{farm_stats.name}" temp="{farm_stats.temp}" humidity={farm_stats.humidity}
                             light={farm_stats.light} ac="{farm_stats.ac}" humidifier={farm_stats.humidifier} show_stats={true}
                             co2={farm_stats.co2} co2_val={farm_stats.co2_val} farm_id={farm_stats.farm_id} type="setting">
                </StatPreview>
            </div>
            <div class="hidden md:flex">
                <StatPreviewLarge farm_name="{farm_stats.name}" temp="{farm_stats.temp}" humidity={farm_stats.humidity}
                             light={farm_stats.light} ac="{farm_stats.ac}" humidifier={farm_stats.humidifier} show_stats={true}
                             co2={farm_stats.co2} co2_val={farm_stats.co2_val} farm_id={farm_stats.farm_id} type="setting">
                </StatPreviewLarge>
            </div>
            <div class="flex justify-evenly w-full grow">
                <div class="flex justify-center grow items-center white ">
                    {#if light_switching}
                        <Icon icon="iconoir:light-bulb-on" class="h-9 w-9 bg-amber-500 p-2 mr-1 rounded-lg"/>
                    {:else}
                        <Icon icon="iconoir:light-bulb-off" class="h-9 w-9 bg-amber-500 p-2 mr-1 rounded-lg"/>
                    {/if}
                    <input type="checkbox" class="toggle toggle-success" bind:checked={light_switch} on:click={() => {control_actuators("light", data.farm_id, light_switching)}}/>
                </div>
                <div class="flex justify-center grow items-center white">
                    {#if ac_switching}
                        <Icon icon="tabler:air-conditioning" class="h-9 w-9 bg-blue-900 p-2 mr-1 rounded-lg"/>
                    {:else}
                        <Icon icon="tabler:air-conditioning-disabled" class="h-9 w-9 bg-blue-900 p-2 mr-1 rounded-lg"/>
                    {/if}
                     <select class="select select-sm bg-blue-900 rounded-lg white pr-7 mr-1 max-height-3 w-13"
                            bind:value={$FarmSettings.ac_temp}
                            on:change={() => handleACTempChange()}
                     disabled={!farm_stats.ac}>
                        <option disabled selected>{$FarmSettings.ac_temp}°</option>
                        {#each $FarmSettings.ac_preset as choice}
                            <option value={choice}>{choice}°</option>
                        {/each}
                    </select>
                    <input type="checkbox" class="toggle toggle-success" bind:checked={ac_switch} on:click={() => {control_actuators("ac", data.farm_id, ac_switching)}}/>
                </div>
                <div class="flex justify-center grow items-center white">
                    {#if humidifier_switching}
                        <Icon icon="mdi:air-humidifier" class="h-9 w-9 bg-teal-900 p-2 mr-1 rounded-lg"/>
                    {:else}
                        <Icon icon="mdi:air-humidifier" class="h-9 w-9 bg-teal-900 p-2 mr-1 rounded-lg"/>
                    {/if}
                    <input type="checkbox" class="toggle toggle-success" bind:checked={humidifier_switch} on:click={() => {control_actuators("dehumidifier", data.farm_id, humidifier_switching)}}/>
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
        <button class="btn btn-primary w-10/12 md:w-1/2"
                on:click={save_settings}
                disabled={isDisabled}
                autocomplete="off"
        >Save</button>
    </div>
{/if}

<style>
  .select-sm {
  height: 2rem;
}

  .loading-ring-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  }

  .loading-ring {
    display: inline-block;
    width: 80px;
    height: 80px;
  }

  .loading-ring:after {
    content: " ";
    display: block;
    width: 64px;
    height: 64px;
    margin: 8px;
    border-radius: 50%;
    border: 6px solid #fff;
    border-color: #fff transparent #fff transparent;
    animation: loading-ring 1.2s linear infinite;
  }

  @keyframes loading-ring {
    0% {
      transform: rotate(0deg);
    }

    100% {
      transform: rotate(360deg);
    }
  }
</style>
