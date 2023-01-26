<script>
    export let farm_name;
    export let temp;
    export let humidity;
    export let light;
    export let ac;

</script>
<div class="grid grid-cols-7 grid-rows-4 max-w-md bg-gray-300 m-5 rounded-lg w-80 h-48">
    <div class="col-start-1 col-span-7 row-start-1 flex justify-center bg-primary rounded-t-lg white">{farm_name}</div>
    <div class="col-start-1 col-span-3 row-start-2 row-span-3 flex items-center justify-center bg-red-900 rounded-lg m-2 white">
        <p class="text-2xl"><i class="fa-solid fa-temperature-half"></i> {temp}°</p>
    </div>
    <div class="col-start-4 col-span-4 row-start-2 bg-teal-900 flex justify-center m-2 rounded-lg items-center white">
        <p> <i class="fa-solid fa-droplet"></i> {humidity} % </p>
    </div>
    <div class="col-start-4 col-span-2 row-start-3 row-span-2 bg-amber-500 flex justify-center items-center m-2 rounded-lg white">
        <p>
            {#if light}
                <i class="fa-solid fa-lightbulb"></i>
            {:else}
                <i class="fa-regular fa-lightbulb"></i>
            {/if}
             {light ? 'On' : 'Off'}</p>
    </div>
    <div class="col-start-6 col-span-2 row-start-3 row-span-2 bg-blue-900 flex justify-center items-center m-2 rounded-lg white">
        <p>{ac ? 'On' : 'Off'}</p>
    </div>
</div>

<style>
    .white {
        color: white;
    }
</style>