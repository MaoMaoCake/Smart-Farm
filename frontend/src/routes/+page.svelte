<script lang="ts">
    import StatPreview from "$lib/StatPreview.svelte";
    import AddFarm from "$lib/AddFarm.svelte";
    //import { FarmData } from "$lib/SF_types.d.ts"

    interface FarmData {
        name: string,
        temp: number,
        humidity: number,
        light: boolean,
        ac: boolean,
        humidifier: boolean,
        co2_val: number,
        co2: boolean
    }

    let data: FarmData[] = [
        {name:"farm 1", temp: 25, humidity: 2, light: true, ac: false, humidifier: true, co2_val: 900, co2: true},
        {name:"farm 2", temp: 24, humidity: 5, light: false, ac: true, humidifier: false, co2_val: 1000, co2: false},
        {name:"farm 3", temp: 16, humidity: 5, light: false, ac: true, humidifier: false, co2_val: 800, co2: false},
    ]
    // let data = null;

</script>
{#if data}
    <div class="w-screen h-screen flex">
        <div class="flex flex-col md:flex-row">

                {#each data as farm}
                    <StatPreview farm_name="{farm.name}" temp="{farm.temp}" humidity={farm.humidity} light={farm.light}
                                 ac="{farm.ac}" humidifier={farm.humidifier} co2={farm.co2} co2_val={farm.co2_val}></StatPreview>
                {/each}
        </div>

    </div>
{:else}
    <div class="flex items-center justify-center">
        <AddFarm/>
    </div>
{/if}