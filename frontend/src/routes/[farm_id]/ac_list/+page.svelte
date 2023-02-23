<script lang="ts">
    import type { PageData } from './$types';
    import StatPreview from "$lib/StatPreview.svelte";
    import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";
    import {FarmSettings} from "$lib/SettingStores.js"
    import ACCard from "./ACCard.svelte";
    export let data: PageData
    $FarmSettings.ac_list = [
        {name: "AC 1",status: true, temp: 25},
        {name: "AC 1",status: true, temp: 26},
        {name: "AC 1",status: false, temp: 24},
        {name: "AC 1",status: false, temp: 23},
    ]
    let table = false;
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
        <div class="flex grow flex-col items-center w-full pb-5">
            <p class="p-5">AC Automation Setting</p>
            <div class="flex justify-evenly w-full">
                <button class="btn bg-black text-white">Turn Off All</button>
                <button class="btn bg-gray-300 text-black">Turn On All</button>
            </div>
        </div>
    </div>
    <div class="flex grow flex-col md:w-2/3">
        <div class="flex grow md:w-10/12 justify-end w-full pl-5 pr-5">
            <button class="btn" on:click={()=>{table = true}}>table</button>
            <button class="btn" on:click={()=>{table = false}}>card</button>
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
                        <div class="flex grow bg-gray-400 rounded-sm m-2 pt-2 pb-2">
                            <div class="flex grow w-1/6 white justify-center">{index + 1}.</div>
                            <div class="flex grow w-1/6 white justify-center">{ac.name}</div>
                            <div class="flex grow w-1/6 white justify-center">
                                {#if ac.status}
                                    <td>ON</td>
                                {:else}
                                    <td>OFF</td>
                                {/if}
                            </div>
                            <div class="flex grow w-1/6 white justify-center">{ac.temp}</div>
                            <div class="flex grow w-1/6 white justify-center">
                                ON <input type="checkbox" class="toggle" bind:checked={ac.status} /> OFF
                            </div>
                            <div class="flex grow w-1/6 white justify-center"></div>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="flex grow mr-5 ml-5 rounded flex-col md:flex-row flex-wrap items-center justify-center">
                    {#each $FarmSettings.ac_list as ac, index}
                        <ACCard name={ac.name} status={ac.status} temp={ac.temp}></ACCard>
                    {/each}
                </div>
            {/if}
        </div>
    </div>
</div>