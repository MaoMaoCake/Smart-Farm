<script lang="ts">
    import Icon from "@iconify/svelte";
    import TimeSet from "$lib/TimeSet.svelte";
    export let farm_id;

    let timeset = [{time_start: "08:50", time_end: "12:00", preset: "preset1"},
                    {time_start: "12:00", time_end: "14:00", preset: "preset2"}]
    function info(type: string){
        alert(type)
    }
    function addTime(){
        timeset = [...timeset, {time_start: "00:00", time_end: "00:00", preset: null}]
    }
    function rmTime(index: number){
        // timeset timeset.findIndex(i => i.time_id === id)
        timeset.splice(index, 1)
        // console.log(timeset.findIndex(i => i.time_id === time_id))
        timeset = timeset
    }
</script>
<div class="flex mt-10 justify-start w-full flex-col md: flex-row">
    <div class="flex items-center w-full">
        <div on:click={() => {info("light")}}>
            <Icon icon="mdi:information" class="h-5 w-5 ml-5" />
        </div>
        <p class="bg-amber-500 rounded min-w-fit ml-5 pl-5 pr-5">Light Setting</p>
        <div>
            <Icon icon="icon-park:setting-config" class="h-5 w-5 ml-2"/>
        </div>
        <div class="divider w-full ml-2"></div>
    </div>
    <div class="flex flex-col pl-5">
        {#each timeset as time, i}
            <TimeSet t_start={time.time_start} t_end={time.time_end} preset={time.preset} num={i + 1}/>
            <button class="btn" on:click={() => {rmTime(i)}}> remove</button>
        {/each}
    </div>
    <button class="btn btn-secondary ml-10 mr-10" on:click={addTime}>Add Time</button>
</div>