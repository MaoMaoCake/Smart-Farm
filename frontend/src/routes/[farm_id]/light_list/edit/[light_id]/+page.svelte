<script lang="ts">
    import type {PageData} from "./$types";
    import LightValueSmall from "./LightValueSmall.svelte";
    import LightValueLarge from "./LightValueLarge.svelte";
    import {page} from "$app/stores";
    import {goto} from "$app/navigation";
     import Icon from '@iconify/svelte';
    export let data: PageData;
    let natural;
    let uv;
    let ir;

    let natural_now;
    let uv_now;
    let ir_now;

    let light_name;

    let is_automation;
    let original_automation;
    let tooltip = false;

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");
    myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

    fetch(
            `http://127.0.0.1:8000/farm/${$page.params.farm_id}/light/${$page.params.light_id}`,
          {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => light_response_handler(await response.json()))
        .catch(error => console.log('error', error));

    function light_response_handler(response) {
        if (!response.successful) {
            goto(`/login`);
        } else if (response.successful) {
            natural_now = response.data.NaturalLightDensity;
            uv_now = response.data.UVLightDensity;
            ir_now = response.data.IRLightDensity;
            light_name = response.data.name;

            natural = natural_now;
            uv = uv_now;
            ir = ir_now;

            is_automation = response.data.automation;
            original_automation = is_automation;
        };
    }

    function save_light_setting(all) {
        console.log(all)
        const myHeaders = new Headers();
        myHeaders.append("Origin", "");
        myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);
        myHeaders.append('Content-Type', 'application/json');

        const input_data = {
            "automation": is_automation,
            "NaturalLightDensity": natural,
            "UVLightDensity": uv,
            "IRLightDensity": ir
        }
        console.log(input_data)
        let path;
        all ?
            path = `http://127.0.0.1:8000/farm/${$page.params.farm_id}/light/${$page.params.light_id}/update_all`
            : path =`http://127.0.0.1:8000/farm/${$page.params.farm_id}/light/${$page.params.light_id}`

        fetch(
            path,
          {
            method: 'PATCH',
            headers: myHeaders,
            body: JSON.stringify(input_data),
            redirect: 'follow'
          })
        .then(async response => save_light_response_handler(await response.json()))
        .catch(error => console.log('error', error));
    }

    function save_light_response_handler(response) {
        if (!response.successful) {
            alert(response.message);
        } else if (response.successful) {
            alert("update successfully!")
            location.reload();
        };
    }

</script>
<div class=" flex grow w-screen justify-center">
      <p class="items-center mt-5 font-bold">Light setting</p>
     <Icon icon="iconoir:light-bulb-on" class="h-5 w-5 mt-6 ml-2"/>
   </div>
<div class="flex grow flex-col justify-center items-center md:flex-row  top-1/2 bottom-1/2 left-0 right-0 mt-5">
    <div class="flex flex-col md:hidden">
        <LightValueSmall name={light_name} natural={natural_now} uv={uv_now} ir={ir_now} automation={is_automation}/>
        <div class="flex grow flex-col items-center w-full pb-5">
            <div class="flex justify-evenly w-full">
                <button class="btn bg-black text-white"
                        on:click={goto(`/${$page.params.farm_id}/settings`)}>Farm setting
                <Icon icon="icon-park-solid:setting-two" class="h-4 w-4 ml-2"/></button>
                <button class="btn bg-gray-300 text-black"
                        on:click={goto(`/${$page.params.farm_id}/light_list`)}>Light list
                <Icon icon="iconoir:light-bulb-on" class="h-5 w-5 ml-2"/></button>
            </div>
        </div>
    </div>
    <div class="flex hidden md:block w-2/3 mr-10 ml-10 justify-center items-center">
        <LightValueLarge name={light_name} natural={natural_now} uv={uv_now} ir={ir_now} automation={is_automation}/>
        <div class="flex grow flex-col items-center w-full pb-5 pt-10">
            <div class="flex justify-evenly w-full">
                <button class="btn bg-black text-white"
                        on:click={goto(`/${$page.params.farm_id}/settings`)}>Farm setting
                <Icon icon="icon-park-solid:setting-two" class="h-4 w-4 ml-2"/></button>
                <button class="btn bg-gray-300 text-black"
                        on:click={goto(`/${$page.params.farm_id}/light_list`)}>Light list
                <Icon icon="iconoir:light-bulb-on" class="h-5 w-5 ml-2"/></button>
            </div>
        </div>
    </div>
    <div class="w-full">
        <div class="flex flex-rowgrow mb-5 items-center justify-center">
         <input type="checkbox" class="toggle toggle-success ml-2 mr-1"
               bind:checked={is_automation}>
        <p class="ml-1 mr-1">Automation:</p>
        {#if is_automation}
            <span class="flex w-3 h-3 bg-green-500 rounded-full pl-3 pt-1"></span>
             <p class="ml-1 mr-1">ON</p>
        {:else}
            <span class="flex w-3 h-3 bg-red-500 rounded-full pl-3 pt-1"></span>
             <p class="ml-1 mr-1">OFF</p>
        {/if}
            </div>
        <div class="flex flex-col grow ml-10 mr-10">
            <div class="flex grow">Light Automation</div>
            <div class="flex flex-col grow">
                <div class="flex items-center">
                    <p class="w-full">Natural Light</p>
                    <input type="text" bind:value={natural} class="input input-bordered w-16 max-w-xs" />
                    <p class="ml-1">%</p>
                </div>
                <div class="flex flex-col">
                    <input type="range" min="0" max="100" bind:value={natural} class="range range-xs amber" step="10" />
                </div>
            </div>
            <div class="flex flex-col grow">
                <div class="flex items-center">
                    <p class="w-full">UV Light</p>
                    <input type="text" bind:value={uv} class="input input-bordered w-16 max-w-xs" />
                    <p class="ml-1">%</p>
                </div>
                <div class="flex flex-col">
                    <input type="range" min="0" max="100" bind:value={uv} class="range range-xs blue" step="10" />
                </div>
            </div>
            <div class="flex flex-col grow">
                <div class="flex items-center">
                    <p class="w-full">Infrared Light</p>
                    <input type="text" bind:value={ir} class="input input-bordered w-16 max-w-xs" />
                    <p class="ml-1">%</p>
                </div>
                <div class="flex flex-col">
                    <input type="range" min="0" max="100" bind:value={ir} class="range range-xs red" step="10" />
                </div>
            </div>
            <div class="flex grow justify-center items-center flex-col pt-5">
                <button class="btn btn-secondary text-white w-10/12 m-2"
                        on:click={() => save_light_setting(false)}
                        disabled={natural==natural_now && ir==ir_now && uv==uv_now && original_automation==is_automation}>Save</button>
                <div class="relative flex grow justify-center items-center mt-5 mb-10 mr-10 10flex-row">
                    <div on:click={() => {tooltip = true}} on:mouseenter={() => {tooltip = true;  event.target.style.cursor = "pointer";}} on:mouseleave={() => {tooltip = false}}>
                        <Icon icon="mdi:information" class="h-5 w-5 ml-5 mr-5" />
                    </div>
                    {#if tooltip}
                    <div class="absolute left-10 bottom-10">
                        <div class="bg-yellow-200 w-56 h-30 rounded-xl relative z-30">
                            <div class="text-black">
                                <p>This button will apply the current setting to all light in the farm</p>
                            </div>
                        </div>
                    </div>
                {/if}
                <button class="btn bg-gray-300 text-black w-10/12 m-2 hover:text-white"
                        on:click={() => save_light_setting(true)}>Apply All & Save</button>
            </div>
            </div>
        </div>
    </div>
</div>

<style>
    .amber::-webkit-slider-thumb {
        background: #f59e0b;
        --range-shdw: 0,0,0;
    }
    .amber::-moz-range-thumb {
        background: #f59e0b;
        --range-shdw: 0,0,0;
    }

    .blue::-webkit-slider-thumb {
        background: #1e3a8a;
        --range-shdw: 0,0,0;
    }
    .blue::-moz-range-thumb {
        background: #1e3a8a;
        --range-shdw: 0,0,0;
    }

    .red::-webkit-slider-thumb {
        background: #7f1d1d;
        --range-shdw: 0,0,0%;
    }
    .red::-moz-range-thumb {
        background: #7f1d1d;
        --range-shdw: 0,0,0%;
    }

</style>