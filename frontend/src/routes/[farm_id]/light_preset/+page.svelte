<script lang="ts">
    import StatPreview from "$lib/StatPreview.svelte";
    import type {PageData} from "./$types";
    import {FarmSettings} from "$lib/SettingStores";

    export let data: PageData;
    let light_switch, ac_switch, humidifier_switch;
    $: light_switch = data.farm_data.light
    $: ac_switch = data.farm_data.ac
    $: humidifier_switch = data.farm_data.humidifier

    $FarmSettings.light_preset = [{name: "Preset 1", natural: 10, uv: 10, infrared:20},
        {name: "Preset 2", natural: 20, uv: 30, infrared:20}]
</script>
<div class="flex w-full justify-center items-center flex-col md:flex-row">
    <div>
        <StatPreview farm_name="{data.farm_data.name}" temp="{data.farm_data.temp}" humidity={data.farm_data.humidity}
                     light={data.farm_data.light} ac="{data.farm_data.ac}" humidifier={data.farm_data.humidifier}
                     co2={data.farm_data.co2} co2_val={data.farm_data.co2_val}>
        </StatPreview>
    </div>
    <div class="overflow-x-auto bg-gray-500">
        <table class="table w-full">
            <!-- head -->
            <thead>
            <tr>
                <th></th>
                <th>Name</th>
                <th></th>
                <th></th>
            </tr>
            </thead>
            <tbody>
            <!-- row 1 -->
                {#each $FarmSettings.light_preset as lp, index}
                    <tr>
                        <th>{index}</th>
                        <td>{lp.name}</td>
                        <td></td>
                        <td><a href="/{$FarmSettings.farm_id}/light_preset/edit/{index}" class="btn btn-primary" >Edit</a></td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>