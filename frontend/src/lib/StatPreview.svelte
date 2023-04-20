<script>
    export let farm_name;
    export let temp;
    export let humidity;
    export let light;
    export let ac;
    export let humidifier;
    export let co2_val;
    export let co2;

    export let farm_id
    export let type
    export let show_stats = false;

    import Icon from '@iconify/svelte';

</script>
<div class="grid grid-cols-7 grid-rows-4 max-w-md bg-gray-300 m-5 rounded-lg w-80 h-48">
    <div class="col-start-1 col-span-7 row-start-1 flex justify-center bg-primary rounded-t-lg white item-center pt-3 pl-4 static">
        <p>{farm_name}</p>

        {#if !type}
            <a href="/{farm_id}/settings">
                <Icon icon="icon-park-solid:setting-two" class="h-4 w-4 ml-2 mt-1"/>
            </a>
        {:else}
            <a href="/change_farm_name?farm_name={farm_name}&farm_id={farm_id}">
                <Icon icon="mdi:pen" class="h-4 w-4 ml-2 mt-1" />
            </a>
        {/if}
        <div class="relative right-0">
            {#if show_stats}
                <a class="btn btn-secondary btn-xs ml-2 text-white" href="/{farm_id}/stats">Stats</a>
            {/if}
        </div>
    </div>
    <div class="col-start-1 col-span-3 row-start-2 row-span-3 flex items-center justify-evenly bg-blue-900 rounded-lg m-2 white flex-col">
        <div class="flex justify-evenly items-center">
            <Icon icon="fa-solid:thermometer-half" class="h-10 w-10"/>
            <p class="text-xl">{temp}°</p>
        </div>
        <div class="flex justify-evenly items-center">
            {#if ac}
                <Icon icon="tabler:air-conditioning" class="h-10 w-10"/>
            {:else}
                <Icon icon="tabler:air-conditioning-disabled" class="h-10 w-10"/>
            {/if}
            <p class="text-xl">
                {ac ? 'On' : 'Off'}
            </p>
        </div>
    </div>
    <div class="col-start-4 col-span-4 row-start-2 bg-teal-900 flex justify-evenly m-2 rounded-lg items-center white">
        <div class="flex justify-evenly items-center">
            <Icon icon="wi:humidity" class="h-10 w-10"/>
            <p>  {humidity} % </p>
        </div>
        <div class="flex justify-evenly items-center">
            {#if humidifier}
                <Icon icon="mdi:air-humidifier" class="h-7 w-7"/>
            {:else}
                <Icon icon="mdi:air-humidifier-off" class="h-7 w-7"/>
            {/if}
            <p>{humidifier ? 'On' : 'Off'}</p>
        </div>
    </div>
    <div class="col-start-4 col-span-2 row-start-3 row-span-2 bg-amber-500 flex justify-center items-center m-2 rounded-lg white">
        <div>
            {#if light}
                <Icon icon="iconoir:light-bulb-on" class="h-10 w-10"/>
            {:else}
                <Icon icon="iconoir:light-bulb-off" class="h-10 w-10"/>
            {/if}
            <p class="text-center">{light ? 'On' : 'Off'}</p>
        </div>
    </div>
    <div class="col-start-6 col-span-2 row-start-3 row-span-2 bg-red-900 flex justify-center items-center m-2 rounded-lg white">
        <div class='flex flex-col justify-evenly'>
            <Icon icon="material-symbols:co2" class="h-10 w-10"/>
            <p class="text-center">{co2_val}</p>
            <p class="text-center">{co2 ? 'On' : 'Off'}</p>

        </div>
    </div>
</div>