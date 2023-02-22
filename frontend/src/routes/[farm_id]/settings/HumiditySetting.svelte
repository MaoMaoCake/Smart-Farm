<script  lang="ts">
    import Icon from "@iconify/svelte";
    import {FarmSettings} from "$lib/SettingStores";

    function info(type: string){
        alert(type)
    }
</script>
<div class="flex mt-10 justify-start w-full flex-col md: flex-row">
    <div class="flex items-center w-full">
        <div on:click={() => {info("light")}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-teal-900 rounded min-w-fit ml-5 pl-5 pr-5 white">Humidity Setting</p>
        <div class="divider w-full ml-2"></div>

    </div>
    <div class="flex justify-center items-center">
        <p class="ml-5 mr-5">Maximum Humidity Level</p>
        <input type="text" bind:value={$FarmSettings.humidity} class="input w-32">
        <p>%</p>
    </div>
</div>
<style>
    .white {
        color: white
    }
</style>