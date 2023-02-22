<script lang="ts">
    import {FarmSettings} from "$lib/SettingStores";
    import {TimePicker} from 'svelte-time-picker'
    import { dialogs } from "svelte-dialogs";

    export let num;
    export let t_start;
    export let t_end;
    export let temp;

    $FarmSettings.ac_preset = [25, 26, 27, 28]
    let selected = temp


    let s_open = false;
    let e_open = false;

    let options = {
        /* Minutes increment */
        minutesIncrement: 5,
    }

    function formatTime(date) {
        var hours = date.getHours();
        var minutes = date.getMinutes();
        minutes = minutes < 10 ? '0'+minutes : minutes;
        return hours + ':' + minutes;
    }
    let startCallback = (event) => {
        t_start = formatTime(event.detail)
    }

    let endCallback = (event) => {
        t_end = formatTime(event.detail)
    }
    function save(state){
        if (state === 'on'){
            s_open = false
        }
        else if (state === "off"){
            e_open = false
        }
    }
    function rmTime(index: number){
        $FarmSettings.ac_schedule.splice(index, 1)
        $FarmSettings.ac_schedule = $FarmSettings.ac_schedule
    }

    async function remove(){
        //alert remove
        if (await dialogs.confirm("Are You sure you want to delete this time?")){
            rmTime(num)
        }
    }

</script>

<div class="flex justify-evenly">
    <div class="flex flex-row justify-evenly grow">
        <div class="flex items-start pt-2">
            <p class="text-bold">{num + 1}.</p>
        </div>
        <div class="flex flex-col grow">
            <div class="flex items-center">
                <p class="ml-2">ON</p>
                <button on:click={() => {s_open = true}} class="btn bg-gray-300 rounded-lg ml-2 w-24">{t_start}</button>
                {#if s_open}
                    <div class="bg-gray-300 blur w-screen h-screen fixed top-0 left-0 z-30">
                    </div>
                    <div class="flex justify-center items-center fixed top-1/2 bottom-1/2 left-1/2 right-1/2 z-30">
                        <div class="flex flex-col justify-center">
                            <TimePicker {options} on:change={startCallback} />
                            <button class="btn btn-primary" on:click={() => {save("on")}}>Save</button>
                        </div>
                    </div>
                {/if}
            </div>
            <div class="flex items-center">
                <p class="pl-2">Off</p>
                <button on:click={() => {e_open = true}} class="btn bg-gray-300 rounded-lg ml-2 w-24">{t_end}</button>
                {#if e_open}
                    <div class="bg-gray-300 blur w-screen h-screen fixed top-0 left-0 z-30">
                    </div>
                    <div class="flex justify-center items-center fixed top-1/2 bottom-1/2 left-1/2 right-1/2 z-30">
                        <div class="flex flex-col justify-center">
                            <TimePicker {options} on:change={endCallback} />
                            <button class="btn btn-primary" on:click={() => {save("off")}}>Save</button>
                        </div>
                    </div>
                {/if}
            </div>
        </div>
        <div class="flex flex-col grow justify-evenly">
            <div class="form-control w-full max-w-xs">
                <label class="label input-group input-group-vertical">
                    <span class="label-text bg-base-100 ">Preset</span>
                    <select class="select bg-blue-900 rounded-lg white">
                        {#if selected.preset_id === "" }
                            <option disabled selected>Pick one</option>
                        {:else}
                            <option disabled selected>{selected}°</option>
                        {/if}
                        {#each $FarmSettings.ac_preset as choice}
                            <option value={choice}>{choice}°</option>
                        {/each}
                    </select>
                </label>
            </div>
        </div>
        <div class="flex grow items-center pl-5">
            <button class="btn btn-error rounded-xl" on:click={remove}>X</button>
        </div>
    </div>
</div>
<style>
    .white {
        color: white;
    }
</style>