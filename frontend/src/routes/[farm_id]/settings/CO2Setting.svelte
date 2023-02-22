<script  lang="ts">
    import Icon from "@iconify/svelte";
    import {FarmSettings} from "$lib/SettingStores";

    let tooltip = false;

</script>
<div class="flex mt-10 justify-start w-full flex-col md: flex-row">
    <div class="flex items-center w-full relative">
        <div on:click={() => {tooltip = true}} on:mouseenter={() => {tooltip = true}} on:mouseleave={() => {tooltip = false}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-red-900 rounded min-w-fit ml-5 pl-5 pr-5 white">CO2 Setting</p>
        <div class="divider w-full ml-2"></div>
        {#if tooltip}
            <div class="absolute left-10 top-10">
                <div class="bg-yellow-200 w-56 h-52 rounded-xl relative z-30">
                    <div class="text-black">
                        <p>This is a button</p>
                        <p>this button is very very cool</p>
                    </div>
                </div>
            </div>
        {/if}
    </div>
    <div class="flex justify-center items-center">
        <p class="ml-5 mr-5">Minimum CO2 Level</p>
        <input type="text" bind:value={$FarmSettings.co2} class="input w-32">
        <p>PPM</p>
    </div>
</div>