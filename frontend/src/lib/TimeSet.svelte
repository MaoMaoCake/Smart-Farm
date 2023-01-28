<script>
    export let num;
    export let t_start;
    export let t_end;
    export let preset;

    let t_start_h, t_start_m, t_end_h, t_end_m;
    t_start_h = t_start.split(":")[0];
    t_start_m = t_start.split(":")[1];

    t_end_h = t_end.split(":")[0];
    t_end_m = t_end.split(":")[1];

    let user_preset = [{name: 'preset 1', preset_id: "preset1"},
                        {name: 'preset 2', preset_id: "preset2"}]
    let selected = {name: 'preset 1', preset_id: "preset1"};

</script>
<div class="flex w-screen justify-evenly">
    <div class="flex">
        <p class="mt-4">{num} {preset}</p>
        <div class="flex flex-col pl-2 mt-2 mb-2">
            <div class="flex flex-row pt-2 pb-2">
                <p class="ml-2">ON</p>
                <input class="bg-gray-200 ml-2 pt-1 pb-1 pl-2 pr-2 rounded-lg w-9" bind:value={t_start_h}/>
                <p>:</p>
                <input class="bg-gray-200 pt-1 pb-1 pl-2 pr-2 rounded-lg w-9" bind:value={t_start_m}/>
            </div>
            <div class="flex flex-row pt-2 pb-2">
                <p class="pl-2">Off</p>
                <input class="bg-gray-200 ml-2 pt-1 pb-1 pl-2 pr-2 rounded-lg w-9" bind:value={t_end_h}/>
                <p>:</p>
                <input class="bg-gray-200 pt-1 pb-1 pl-2 pr-2 rounded-lg w-9" bind:value={t_end_m}/>
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