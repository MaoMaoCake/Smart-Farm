<script lang="ts">
    export let name;
    export let temp;
    export let status;
    export let ac_id;
    export let farm_id;

    import Icon from '@iconify/svelte';

</script>
<div class="w-96 h-52 bg-gray-300 rounded-xl m-5 flex items-center justify-center">
    <div class="flex flex-col grow h-52">
        <div class="flex grow white bg-secondary rounded-t-xl min-w-max h-1/6 pt-2 pb-2 items-center justify-center">
            <p class="ml-6">{name}</p>
             <a href="/change_ac_name?ac_name={name}&farm_id={farm_id}&ac_id={ac_id}">
                <Icon icon="mdi:pen" class="h-4 w-4 ml-2 " />
            </a>
        </div>
        <div class="flex grow min-w-max h-5/6 justify-evenly items-center">
            {#if status}
                <div class="flex aspect-square bg-blue-900 h-24 w-24 white flex-col justify-center items-center rounded-xl">
                    <Icon icon="tabler:air-conditioning" class="h-10 w-10"/>
                    <p class="text-xl">On</p>
                </div>
            {:else}
                <div class="flex aspect-square bg-gray-500 h-24 w-24 white flex-col justify-center items-center rounded-xl">
                    <Icon icon="tabler:air-conditioning-disabled" class="h-10 w-10"/>
                    <p class="text-xl">Off</p>
                </div>

            {/if}
            <div class="flex flex-col items-center">
                <div class="flex p-2 min-w-fit">
                    {#if status}
                        <p class="badge bg-blue-900 text-white text-2xl p-4">{temp}°</p>
                    {:else}
                        <p class="badge bg-gray-500 border-gray-500 text-white text-2xl p-4">{temp}°</p>
                    {/if}
                </div>
                <div class="flex p-2">
                    <p>ON</p>
                    <input type="checkbox" class="toggle" bind:checked={status} />
                    <p>OFF</p>
                </div>
            </div>

        </div>
    </div>
</div>