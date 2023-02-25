<script lang="ts">
    import type { PageData } from './$types';
    import StatPreview from "$lib/StatPreview.svelte";
    import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";
    import {FarmSettings} from "$lib/SettingStores.js"
    import LightCard from "./LightCard.svelte";
    export let data: PageData

    $FarmSettings.light_list = [
        {name: "Light 1", natural: 100, uv: 20, ir: 50},
        {name: "Light 2", natural: 20, uv: 50, ir: 40},
        {name: "Light 2", natural: 80, uv: 20, ir: 30},
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
                        <div class="flex grow w-1/5"></div>
                        <div class="flex grow w-1/5 white justify-center">Name</div>
                        <div class="flex grow w-1/5 white justify-center flex-col items-center"><p>Natural</p><p>Light</p></div>
                        <div class="flex grow w-1/5 white justify-center flex-col items-center"><p>UV</p><p>Light</p></div>
                        <div class="flex grow w-1/5 white justify-center flex-col items-center"><p>Infrared</p><p>Light</p></div>
                    </div>
                    {#each $FarmSettings.light_list as ll, index}
                        <div class="flex grow bg-gray-400 rounded-sm m-2 pt-2 pb-2">
                            <div class="flex grow w-1/5 white justify-center">{index + 1}.</div>
                            <div class="flex grow w-1/5 white justify-center">{ll.name}</div>
                            <div class="flex grow w-1/5 white justify-center"><p class="bg-amber-500 rounded p-2">{ll.natural}%</p></div>
                            <div class="flex grow w-1/5 white justify-center"><p class="bg-blue-900 rounded p-2">{ll.uv}%</p></div>
                            <div class="flex grow w-1/5 white justify-center"><p class="bg-red-900 rounded p-2">{ll.ir}%</p></div>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="flex grow mr-5 ml-5 rounded flex-col md:flex-row flex-wrap items-center justify-center">
                    {#each $FarmSettings.light_list as ll, index}
                        <LightCard name={ll.name} natural={ll.natural} uv={ll.uv} ir={ll.ir}/>
                    {/each}
                </div>
            {/if}
        </div>
    </div>
    <div class="flex justify-center fixed left-0 right-0 bottom-5">
        <div class="flex justify-center flex-col">
            <p class="bg-gray-900 text-white pb-2 pt-2 text-center rounded mb-2 pr-3 pl-3">Create Preset From Current Settings</p>
            <button class="btn btn-secondary text-white">Preset List</button>
        </div>
    </div>
    <div class="h-36 md:hidden"></div>
</div>