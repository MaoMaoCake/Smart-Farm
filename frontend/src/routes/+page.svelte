<script lang="ts">
    import StatPreview from "$lib/StatPreview.svelte";
    import AddFarm from "$lib/AddFarm.svelte";
    import {onMount} from "svelte";
    import {goto} from '$app/navigation'
    import {logged_in} from "$lib/SettingStores";
    import {is_register} from "../lib/SettingStores";
    import { PUBLIC_URL_PREFIX } from '$env/static/public'

    is_register.set(false);

    onMount(() => {
        if (!$logged_in) {
            goto("/login")
        }
    })
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

    let data: FarmData[]

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");
    myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

    fetch(
        `${PUBLIC_URL_PREFIX}/api/list`,
        {
          method: 'GET',
          headers: myHeaders,
          redirect: 'follow'
        })
      .then(async response => response_handler(await response.json()))
      .catch(error => console.log('error', error));

    function response_handler(response) {
        if (response.status_code === 401) {
          alert(response.message);
          goto("/login")
        } else if (response.status_code  === 200) {
          data = response.data?.map((farm_data) => {
            return{
                name: farm_data.farmName,
                temp: farm_data.temperature,
                humidity: farm_data.humidityLevel,
                light: farm_data.lightStatus,
                ac: farm_data.ACStatus,
                humidifier: farm_data.dehumidifierStatus,
                co2_val: farm_data.CO2Level,
                co2: farm_data.CO2controllerStatus,
                farm_id: farm_data.farmId
            }
          });
        };
    }

</script>
{#if data?.length}
    <div class="w-screen ">
        <div class="flex flex-col items-center justify-center grow md:flex-row md:flex-wrap">

                {#each data as farm}
                    <StatPreview farm_name="{farm.name}" temp="{farm.temp}" humidity={farm.humidity} light={farm.light}
                                 ac="{farm.ac}" humidifier={farm.humidifier} co2={farm.co2} co2_val={farm.co2_val}
                                 farm_id={farm.farm_id}></StatPreview>
                {/each}
        </div>
        <div class="mb-24"></div> <!-- Spacing so we can see the stats of the last farm -->
    </div>
    <div class="flex justify-center items-center fixed bottom-10 left-1/2 right-1/2">
        <a href="/add-farm" class="btn btn-secondary w-56 text-white">Add Farm</a>
    </div>
{:else}
    <div class="flex items-center justify-center">
        <AddFarm/>
    </div>
{/if}