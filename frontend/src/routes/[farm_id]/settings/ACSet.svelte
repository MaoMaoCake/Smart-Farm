<script lang="ts">
    import {FarmSettings} from "$lib/SettingStores";
    import {TimePicker} from 'svelte-time-picker'
    import { dialogs } from "svelte-dialogs";

    export let num;
    export let t_start;
    export let t_end;
    export let temp;

    const initial_changes_type = $FarmSettings.ac_schedule[num].changes_type;
    const initial_option = $FarmSettings.ac_schedule[num].temperature;
    let preset_change = false;
    let time_change = false;

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
        $FarmSettings.ac_schedule[num].startTime = t_start;
        switch ($FarmSettings.ac_schedule[num].changes_type) {
            case "NO_CHANGES":
            case null:
                $FarmSettings.ac_schedule[num].changes_type = "UPDATE";
                time_change = true;
                break
        }
    }

    let endCallback = (event) => {
        t_end = formatTime(event.detail)
        $FarmSettings.ac_schedule[num].endTime = t_end;
        switch ($FarmSettings.ac_schedule[num].changes_type) {
            case "NO_CHANGES":
            case null:
                $FarmSettings.ac_schedule[num].changes_type = "UPDATE";
                time_change = true;
                break
        }
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
        if ($FarmSettings.ac_schedule[num].changes_type == "DELETE") {
            if (preset_change || time_change) {
                $FarmSettings.ac_schedule[num].changes_type = "UPDATE";
            } else {
                $FarmSettings.ac_schedule[num].changes_type = initial_changes_type;
            }
        } else if ($FarmSettings.ac_schedule[num].changes_type == "CREATE") {
            $FarmSettings.ac_schedule.splice(index, 1);
            $FarmSettings.ac_schedule = $FarmSettings.ac_schedule;
        } else {
            $FarmSettings.ac_schedule[num].changes_type = "DELETE";
        }
    }

    async function remove(){
        if ($FarmSettings.ac_schedule[num].changes_type == "DELETE") {
            rmTime(num)
        } else {
            if (await dialogs.confirm("Are You sure you want to delete this automation?")){
                rmTime(num)
            }
        }
    }

    async function handleOptionChange(){
        if ($FarmSettings.ac_schedule[num].temperature == initial_option) {
            $FarmSettings.ac_schedule[num].changes_type = initial_changes_type;
            preset_change = false;
        } else {
            $FarmSettings.ac_schedule[num].changes_type = "UPDATE";
            preset_change = true;
        }
    }

</script>

<div class="flex justify-evenly">
    <div class="flex flex-row justify-evenly grow">
        <div class="flex items-start pt-2">
            <p class="text-bold pt-1">{num + 1}.</p>
        </div>
        <div class="flex flex-col grow pl-2">
            <div class="flex items-center">
                <p class="ml-2 pr-0.5">On</p>
                <button on:click={() => {s_open = true}} class="btn bg-gray-300 rounded-lg ml-2 w-24 text-black hover:text-white"
                disabled={$FarmSettings.ac_schedule[num].changes_type == "DELETE"}>{t_start}</button>
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
                <button on:click={() => {e_open = true}} class="btn bg-gray-300 rounded-lg ml-2 w-24 text-black hover:text-white"
                disabled={$FarmSettings.ac_schedule[num].changes_type == "DELETE"}>{t_end}</button>
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
                    <span class="label-text bg-base-100 ">Temperature</span>
                    <select class="select bg-blue-900 rounded-lg white"
                            disabled={$FarmSettings.ac_schedule[num].changes_type == "DELETE"}
                            bind:value={$FarmSettings.ac_schedule[num].temperature}
                            on:change={() => handleOptionChange()}>
                        {#if temp.preset_id === "" }
                            <option disabled selected>Pick one</option>
                        {:else}
                            <option disabled selected>{temp}°</option>
                        {/if}
                        {#each $FarmSettings.ac_preset as choice}
                            <option value={choice}>{choice}°</option>
                        {/each}
                    </select>
                </label>
            </div>
        </div>
        <div class="flex grow items-center pl-5">
            {#if $FarmSettings.ac_schedule[num].changes_type != "DELETE"}
                <button class="btn btn-error rounded-xl" on:click={remove}>X</button>
              {:else}
                 <button class="btn rounded-xl bg-gray-300 text-black hover:text-white" on:click={remove}>Undo</button>
             {/if}
        </div>
    </div>
</div>
