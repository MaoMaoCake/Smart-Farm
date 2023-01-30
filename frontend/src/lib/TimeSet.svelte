<script>
    export let num;
    export let t_start;
    export let t_end;
    export let preset;

    import {TimePicker} from 'svelte-time-picker'

    let user_preset = [{name: 'preset 1', preset_id: "preset1"},
                        {name: 'preset 2', preset_id: "preset2"}]
    let selected = {name: 'preset 1', preset_id: preset};

    let s_open = false;
    let e_open = false;

    function formatTime(date) {
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var ampm = hours >= 12 ? 'pm' : 'am';
        hours = hours % 12;
        hours = hours ? hours : 12;
        minutes = minutes < 10 ? '0'+minutes : minutes;
        return hours + ':' + minutes + " " + ampm;
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
</script>
<div class="flex w-screen justify-evenly">
    <div class="flex">
        <p class="mt-4">{num}</p>
        <div class="flex flex-col pl-2 mt-2 mb-2">
            <div class="flex flex-row pt-2 pb-2">
                <p class="ml-2">ON</p>
                <p on:click={() => {s_open = true}}>{t_start}</p>
                {#if s_open}
                    <div class="flex justify-center items-center absolute top-1/2 bottom-1/2 left-1/2 right-1/2">
                        <div class="flex flex-col justify-center">
                            <TimePicker on:change={startCallback} />
                            <button class="btn btn-primary" on:click={() => {save("on")}}>Save</button>
                        </div>
                    </div>
                {/if}
            </div>
            <div class="flex flex-row pt-2 pb-2">
                <p class="pl-2">Off</p>
                <p on:click={() => {e_open = true}}>{t_end}</p>
                {#if e_open}
                    <div class="flex justify-center items-center absolute top-1/2 bottom-1/2 left-1/2 right-1/2">
                        <div class="flex flex-col justify-center">
                            <TimePicker on:change={endCallback} />
                            <button class="btn btn-primary" on:click={() => {save("off")}}>Save</button>
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    </div>
    <div class="flex flex-col mt-2">
        <div class="form-control w-full max-w-xs">
            <label class="label">
                <span class="label-text">Preset</span>
            </label>
            <select class="select select-bordered">
                {#if selected.preset_id === "" }
                    <option disabled selected>Pick one</option>
                {:else}
                    <option disabled selected>{selected.name}</option>
                {/if}
                {#each user_preset as choice}
                    <option value={choice.preset_id}>{choice.name}</option>
                {/each}
            </select>
        </div>
    </div>
</div>