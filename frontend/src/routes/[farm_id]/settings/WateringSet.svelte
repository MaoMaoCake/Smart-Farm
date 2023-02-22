<script lang="ts">
    import {dialogs} from "svelte-dialogs";
    import {FarmSettings} from "$lib/SettingStores"
    import {TimePicker} from 'svelte-time-picker'

    export let num;
    export let t_start;

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

    function save(state){
        if (state === 'on'){
            s_open = false
        }
        else if (state === "off"){
            e_open = false
        }
    }

    function rmTime(index: number) {
        $FarmSettings.watering_schedule.splice(index, 1)
        $FarmSettings.watering_schedule = $FarmSettings.watering_schedule
    }

    async function remove(){
        //alert remove
        if (await dialogs.confirm("Are You sure you want to delete this time?")){
            rmTime(num)
        }
    }
</script>
<div class="flex justify-evenly grow">
    <div class="flex flex-col grow items-center">
        <div class="flex justify-evenly grow">
            <div>
            <p class="text-bold">{num + 1}.</p>
            </div>
            <div>
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
            <div class="flex grow items-center pl-5">
                <button class="btn btn-error rounded-xl" on:click={remove}>X</button>
            </div>
        </div>
    </div>
</div>