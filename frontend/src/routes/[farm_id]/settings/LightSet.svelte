<script lang="ts">
    import {FarmSettings} from "$lib/SettingStores.js";

    export let num;
    export let t_start;
    export let t_end;
    export let preset;
    export let rm_num;

    import {TimePicker} from 'svelte-time-picker'

    let user_preset = [{name: 'preset 1', preset_id: "preset1"},
                        {name: 'preset 2', preset_id: "preset2"}]
    let selected = {name: 'preset 1', preset_id: preset};

    let s_open = false;
    let e_open = false;
    let confirm_delete = false;

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
        $FarmSettings.light_schedule.splice(index, 1)
        $FarmSettings.light_schedule = $FarmSettings.light_schedule
    }

    function remove(){
        //alert remove

        if (ok){
            rmTime(num);
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
                <p on:click={() => {s_open = true}} class="btn bg-gray-300 rounded-lg ml-2 w-24">{t_start}</p>
                {#if s_open}
                    <div class="bg-gray-300 blur w-screen h-screen fixed top-0 left-0">
                    </div>
                    <div class="flex justify-center items-center fixed top-1/2 bottom-1/2 left-1/2 right-1/2">
                            <div class="flex flex-col justify-center">
                                <TimePicker {options} on:change={startCallback} />
                                <button class="btn btn-primary" on:click={() => {save("on")}}>Save</button>
                            </div>
                        </div>
                {/if}
            </div>
            <div class="flex items-center">
                <p class="pl-2">Off</p>
                <p on:click={() => {e_open = true}} class="btn bg-gray-300 rounded-lg ml-2 w-24">{t_end}</p>
                {#if e_open}
                    <div class="flex justify-center items-center fixed top-1/2 bottom-1/2 left-1/2 right-1/2">
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
            <select class="select bg-amber-500 rounded-lg white">
                {#if selected.preset_id === "" }
                    <option disabled selected>Pick one</option>
                {:else}
                    <option disabled selected>{selected.name}</option>
                {/if}
                {#each user_preset as choice}
                    <option value={choice.preset_id}>{choice.name}</option>
                {/each}
            </select>`
            </label>
        </div>
        </div>
        <div class="flex grow items-center pl-5">
            <button class="btn btn-error rounded-xl" on:click={() => {rmTime(num)}}>X</button>
        </div>
    </div>
</div>
<style>
    .white {
        color: white;
    }
</style>