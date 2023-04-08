<script lang="ts">
  import type { PageData } from './$types';
  import "@carbon/styles/css/styles.css";
  import "@carbon/charts/styles.css";
  import { LineChart } from "@carbon/charts-svelte";
  import StatPreview from "$lib/StatPreview.svelte";
  import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";
  import {page} from "$app/stores";
  import {goto} from "$app/navigation";
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
    let table = "day";

  let chart_data_day = []
  let chart_data_week = []
  let chart_data_month = []

  const myHeaders = new Headers();
  myHeaders.append("Origin", "");
  myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

   fetch(
          `/api/farm/${$page.params.farm_id}/stats`,
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
          `api/farm/${$page.params.farm_id}/statsGraph`,
        {
          method: 'GET',
          headers: myHeaders,
          redirect: 'follow'
        })
      .then(async response => graph_handler(await response.json()))
      .catch(error => console.log('error', error));

  function graph_handler(response) {
      if (!response.successful) {
          goto(`/login`);
      } else if (response.successful) {
          chart_data_day = response.data.day;
          chart_data_day.sort((a, b) => new Date(a.date) - new Date(b.date));
          chart_data_week = response.data.week;
          chart_data_week.sort((a, b) => new Date(a.date) - new Date(b.date));
          chart_data_month = response.data.month;
          chart_data_month.sort((a, b) => new Date(a.date) - new Date(b.date));
      };
  }

</script>
{#if farm_stats}
  <div class="flex w-full justify-center items-center flex-col md:flex-row">
    <div class="flex flex-col grow md:w-1/3 md:h-5/6 items-center justify-center">
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
         <div class="flex grow flex-col items-center w-full pb-5">
                <div class="flex justify-evenly w-full">
                    <button class="btn bg-black text-white"
                            on:click={goto(`/${$page.params.farm_id}/settings`)}>Farm setting
                    <Icon icon="icon-park-solid:setting-two" class="h-4 w-4 ml-2"/></button>
                </div>
            </div>
<!--        <div class="flex grow">-->
<!--            <button class="btn btn-secondary white">Download Report</button>-->
<!--        </div>-->
    </div>
    <div class="flex flex-col grow w-10/12">
       <div class="flex grow justify-center w-full pl-5 pr-5">
                <button class="btn {table === 'day' ? 'selected' : ''} mr-1"
                        on:click={()=>{table = "day"}}> Last 24 Hours</button>
                <button class="btn {table === 'week' ? 'selected' : ''} mr-1"
                        on:click={()=>{table = "week"}}>Last week</button>
         <button class="btn {table === 'month' ? 'selected' : ''} mr-1"
                        on:click={()=>{table = "month"}}> Last month</button>
            </div>
      {#if table === 'day'}
        <div class="flex grow mt-2 mb-2">
            <LineChart
                    data={chart_data_day}
                    options={{
        	"title": "Last 24 hours",
        	"axes": {
        		"bottom": {
        			"mapsTo": "date",
        			"scaleType": "time",
        			"format": "%H:%M:%S"
        		},
        		"left": {
        			"mapsTo": "value",
        			"title": "Level of Humidity",
        			"scaleType": "linear"
        		}
        	},
        	"curve": "curveMonotoneX",
        	"height": "400px"
        }}
            />
        </div>
        {/if}
{#if table === 'week'}
        <div class="flex grow mt-2 mb-2">
            <LineChart
                    data={chart_data_week}
                    options={{
        	"title": "Last week",
        	"axes": {
        		"bottom": {
        			"mapsTo": "date",
        			"scaleType": "time",
        		},
        		"left": {
        			"mapsTo": "value",
        			"title": "Level of Humidity",
        			"scaleType": "linear"
        		}
        	},
        	"curve": "curveMonotoneX",
        	"height": "400px"
        }}
            />
        </div>
        {/if}
      {#if table === 'month'}
        <div class="flex grow mt-2 mb-2">
            <LineChart
                    data={chart_data_month}
                    options={{
        	"title": "Last month",
        	"axes": {
        		"bottom": {
        			"mapsTo": "date",
        			"scaleType": "time",
        		},
        		"left": {
        			"mapsTo": "value",
        			"title": "Level of Humidity",
        			"scaleType": "linear"
        		}
        	},
        	"curve": "curveMonotoneX",
        	"height": "400px"
        }}
            />
        </div>
        {/if}
    </div>
  </div>
{/if}

<style>
  .selected {
    background-color: green;
    border-color: green;
    color: white;
  }
  .btn:hover {
  background-color: grey;
      border-color: grey;
}
</style>