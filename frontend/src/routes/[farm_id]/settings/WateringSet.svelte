<script>
    export let num;
    export let t_start;
    export let t_end;


    import {TimePicker} from 'svelte-time-picker'

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
</script>
<div class="flex w-screen justify-evenly">
    <div class="flex">
        <p class="mt-4">{num}</p>
        <div class="flex flex-col pl-2 mt-2 mb-2">
            <div class="flex flex-row pt-2 pb-2 justify-center items-center">
                <p on:click={() => {s_open = true}} class="btn bg-gray-300 rounded-lg ml-2 w-24">{t_start}</p>
                {#if s_open}
                    <div class="flex justify-center items-center absolute top-1/2 bottom-1/2 left-1/2 right-1/2">
                        <div class="flex flex-col justify-center">
                            <TimePicker {options} on:change={startCallback} />
                            <button class="btn btn-primary" on:click={() => {save("on")}}>Save</button>
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>