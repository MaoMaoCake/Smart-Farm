<script>
    import StatPreview from "$lib/StatPreview.svelte";
    import AddFarm from "$lib/AddFarm.svelte";
    let data = [
        {name:"farm 1", temp: 25, humidity: 2, light: true, ac: false},
        {name:"farm 2", temp: 24, humidity: 5, light: false, ac: false}
    ]
    // let data = null;

</script>
{#if data}
    <div class="w-screen h-screen flex">
        <div class="flex flex-col md:flex-row">

                {#each data as farm}
                    <StatPreview farm_name="{farm.name}" temp="{farm.temp}" humidity={farm.humidity} light={farm.light} ac="{farm.ac}"></StatPreview>
                {/each}
        </div>

    </div>
{:else}
    <div class="flex align-center justify-center">
        <AddFarm/>
    </div>
{/if}