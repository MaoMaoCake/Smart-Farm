<script>
    export let farm_name;
    export let temp;
    export let humidity;
    export let light;
    export let ac;
    export let humidifier;
    export let co2_val;
    export let co2;

    export let farm_id;
    export let type;

    import Icon from '@iconify/svelte';

</script>

<div class="hidden md:flex justify-center">
    <div class="grid grid-cols-4 grid-rows-8 bg-gray-300 m-5 rounded-lg w-96">
        <div class="col-start-1 col-span-4 row-start-1 flex justify-center bg-primary rounded-t-lg white items-center h-14 pl-3">
            {farm_name}
            {#if !type}
                <a href="{farm_id}/settings">
                    <Icon icon="icon-park-solid:setting-two" class="h-5 w-5 ml-2 pt-1"/>
                </a>
                {:else}
                <a href="/change_farm_name?farm_name={farm_name}&farm_id={farm_id}">
                    <Icon icon="mdi:pen" class="h-4 w-4 ml-2 "/>
                </a>
            {/if}
        </div>
        <div class="col-start-1 col-span-4 row-start-2 row-span-4 bg-blue-900 aspect-square flex items-center justify-evenly flex-col white rounded-xl m-2">
            <div class="flex justify-evenly items-center">
                <Icon icon="fa-solid:thermometer-half" class="h-20 w-20"/>
                <p class="text-4xl">{temp}°</p>
            </div>
            <div class="flex justify-evenly items-center">
                {#if ac}
                    <Icon icon="tabler:air-conditioning" class="h-20 w-20"/>
                {:else}
                    <Icon icon="tabler:air-conditioning-disabled" class="h-20 w-20"/>
                {/if}
                <p class="text-4xl">
                    {ac ? 'On' : 'Off'}
                </p>
            </div>
        </div>
        <div class="col-start-1 col-span-4 row-start-6 bg-teal-900 flex flex-row white rounded-xl justify-evenly items-center ml-2 mr-2">
            <div class="flex justify-evenly items-center">
                <Icon icon="wi:humidity" class="h-14 w-14"/>
                <p class="text-2xl">{humidity} % </p>
            </div>
            <div class="flex justify-evenly items-center">
                {#if humidifier}
                    <Icon icon="mdi:air-humidifier" class="h-10 w-10"/>
                {:else}
                    <Icon icon="mdi:air-humidifier-off" class="h-10 w-10"/>
                {/if}
                <p class="text-2xl">{humidifier ? 'On' : 'Off'}</p>
            </div>
        </div>
        <div class="col-start-1 col-span-2 row-start-7 row-span-8 bg-amber-500 aspect-square flex justify-center items-center rounded-xl m-2">
            <div class="flex flex-col white">
                {#if light}
                    <Icon icon="iconoir:light-bulb-on" class="h-20 w-20"/>
                {:else}
                    <Icon icon="iconoir:light-bulb-off" class="h-20 w-20"/>
                {/if}
                <p class="text-center text-2xl">{light ? 'On' : 'Off'}</p>
            </div>
        </div>
        <div class="col-start-3 col-span-4 row-start-7 row-span-8 bg-red-900 aspect-square flex justify-center items-center rounded-xl m-2">
            <div class='flex flex-col justify-evenly white'>
                <Icon icon="material-symbols:co2" class="h-14 w-14"/>
                <p class="text-center text-2xl">{co2_val}</p>
                <p class="text-center text-2xl">{co2 ? 'On' : 'Off'}</p>

            </div>
        </div>
    </div>
</div>