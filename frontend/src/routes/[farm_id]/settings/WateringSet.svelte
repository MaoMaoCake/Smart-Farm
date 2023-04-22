<script lang="ts">
    import {dialogs} from "svelte-dialogs";
    import {FarmSettings} from "$lib/SettingStores"
    import {TimePicker} from 'svelte-time-picker'

    export let num;
    export let t_start;

    const initial_changes_type = $FarmSettings.watering_schedule[num].changes_type;
    let s_open = false;
    let time_change = false;

    let options = {
        /* Minutes increment */
        minutesIncrement: 5,
        hasButtons: true,
    }

    function formatTime(date) {
        var hours = date.getHours();
        var minutes = date.getMinutes();
        minutes = minutes < 10 ? '0'+minutes : minutes;
        return hours + ':' + minutes;
    }
    let okCallback = (event) => {
        t_start = formatTime(event.detail);
        $FarmSettings.watering_schedule[num].wateringStartTime = t_start;
        switch ($FarmSettings.watering_schedule[num].changes_type) {
            case "NO_CHANGES":
            case null:
                $FarmSettings.watering_schedule[num].changes_type = "UPDATE";
                time_change = true;
                break
        }
        s_open = false;
    }

    let cancelCallback = () => {
        s_open = false;
    }


    function rmTime(index: number) {
        if ($FarmSettings.watering_schedule[num].changes_type == "DELETE") {
            if (time_change) {
                $FarmSettings.watering_schedule[num].changes_type = "UPDATE";
            } else {
                $FarmSettings.watering_schedule[num].changes_type = initial_changes_type;
            }
        } else if ($FarmSettings.watering_schedule[num].changes_type == "CREATE") {
            $FarmSettings.watering_schedule.splice(index, 1);
            $FarmSettings.watering_schedule = $FarmSettings.watering_schedule;
        } else {
            $FarmSettings.watering_schedule[num].changes_type = "DELETE";
        }
    }

    async function remove(){
        // if ($FarmSettings.watering_schedule[num].changes_type == "DELETE") {
        //     rmTime(num)
        // } else {
        //     if (await dialogs.confirm("Are You sure you want to delete this automation?")){
        //         rmTime(num)
        //     }
        // }
        rmTime(num)
    }
</script>
<div class="flex justify-evenly grow">
    <div class="flex flex-col grow items-center">
        <div class="flex justify-evenly grow">
            <div>
            <p class="text-bold pt-3.5">{num + 1}.</p>
            </div>
            <div>
                <button on:click={() => {s_open = true}}
                        class="btn bg-gray-300 rounded-lg ml-2 w-24 text-black hover:text-white"
                        disabled={$FarmSettings.watering_schedule[num].changes_type === "DELETE"}>{t_start}</button>
            {#if s_open}
                <div class="bg-gray-300 blur w-screen h-screen fixed top-0 left-0 z-30">
                </div>
                <div class="flex justify-center items-center fixed top-1/2 bottom-1/2 left-1/2 right-1/2 z-30">
                    <div class="flex flex-col justify-center">
                        <TimePicker {options} on:cancel={cancelCallback} on:ok={okCallback}/>
                    </div>
                </div>
            {/if}
            </div>
            <div class="flex grow items-center pl-5">
                {#if $FarmSettings.watering_schedule[num].changes_type !== "DELETE"}
                    <button class="btn btn-error rounded-xl" on:click={remove}>X</button>
                {:else}
                     <button class="btn rounded-xl bg-gray-300 text-black hover:text-white" on:click={remove}>Undo</button>
                {/if}
            </div>
        </div>
    </div>
</div>