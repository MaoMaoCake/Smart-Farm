<script lang="ts">
    import StatPreview from "$lib/StatPreview.svelte";
    import AddFarm from "$lib/AddFarm.svelte";

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

    let data: FarmData[] = [
        {name:"farm 1", temp: 25, humidity: 2, light: true, ac: false, humidifier: true, co2_val: 900, co2: true, farm_id: 1},
        {name:"farm 2", temp: 24, humidity: 5, light: false, ac: true, humidifier: false, co2_val: 1000, co2: false, farm_id: 2},
        {name:"farm 3", temp: 16, humidity: 5, light: false, ac: true, humidifier: false, co2_val: 800, co2: false, farm_id: 3},
    ]
    // let data = null;

</script>
{#if data}
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