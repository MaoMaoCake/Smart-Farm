<script>
    export let name;
    export let natural;
    export let uv;
    export let ir;
    export let automation;
    export let farm_id;
    export let light_id;

    import Icon from "@iconify/svelte";
</script>
<div>
    <div class="flex grow flex-col bg-gray-300 rounded-xl">
        <div class="w-full bg-secondary flex justify-center items-center white rounded-t-xl">
            <p>{name}</p>
            <a href="/change_light_name?light_name={name}&farm_id={farm_id}&light_id={light_id}">
              <Icon icon="mdi:pen" class="h-4 w-4 ml-2 mt-1" />
            </a>
        </div>
        <div class="flex flex-col">
            {#if !automation}
                <div class="flex justify-evenly items-center bg-gray-500 h-32 rounded-xl m-2">
                    <div class="flex flex-col items-center grow white">
                    <p>Natural</p>
                    <p>Light</p>
                </div>
                <div class="flex grow items-center justify-center white">
                    {natural}%
                </div>
            </div>
            {:else}
                <div class="flex justify-evenly items-center bg-amber-500 h-32 rounded-xl m-2">
                    <div class="flex flex-col items-center grow white">
                    <p>Natural</p>
                    <p>Light</p>
                </div>
                <div class="flex grow items-center justify-center white">
                    {natural}%
                </div>
            </div>
            {/if}

             {#if !automation}
                <div class="flex justify-evenly items-center bg-gray-500 h-32 rounded-xl m-2">
                <div class="flex flex-col items-center grow white">
                    <p>UV</p>
                    <p>Light</p>
                </div>
                <div class="flex grow items-center justify-center white">
                    {uv}%
                </div>
            </div>
            {:else}
                <div class="flex justify-evenly items-center bg-blue-900 h-32 rounded-xl m-2">
                <div class="flex flex-col items-center grow white">
                    <p>UV</p>
                    <p>Light</p>
                </div>
                <div class="flex grow items-center justify-center white">
                    {uv}%
                </div>
            </div>
            {/if}

             {#if !automation}
               <div class="flex justify-evenly items-center bg-gray-500 h-32 rounded-xl m-2">
                <div class="flex flex-col items-center grow white">
                    <p>Infrared</p>
                    <p>Light</p>
                </div>
                <div class="flex grow items-center justify-center white">
                    {ir}%
                </div>
            </div>
            {:else}
               <div class="flex justify-evenly items-center bg-red-900 h-32 rounded-xl m-2">
                <div class="flex flex-col items-center grow white">
                    <p>Infrared</p>
                    <p>Light</p>
                </div>
                <div class="flex grow items-center justify-center white">
                    {ir}%
                </div>
            </div>
            {/if}

        </div>
    </div>
</div>