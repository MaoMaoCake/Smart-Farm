<script lang="ts">
    import type { PageData } from './$types';
    import StatPreview from "$lib/StatPreview.svelte";
    import {FarmSettings} from "$lib/SettingStores.js"
    export let data: PageData

    $FarmSettings.light_list = [
        {name: "Light 1", natural: 100, uv: 20, ir: 50},
        {name: "Light 2", natural: 20, uv: 50, ir: 40},
        {name: "Light 2", natural: 80, uv: 20, ir: 30},
    ]
</script>
<StatPreview></StatPreview>

<div class="overflow-x-auto bg-gray-500">
        <table class="table w-full">
            <!-- head -->
            <thead>
            <tr>
                <th></th>
                <th>Name</th>
                <th>natural Light</th>
                <th>UV Light</th>
                <th>Infrared Light</th>
            </tr>
            </thead>
            <tbody>
            <!-- row 1 -->
                {#each $FarmSettings.light_list as ll, index}
                    <tr>
                        <th>{index}</th>
                        <td>{ll.name}</td>
                        <td>{ll.natural}</td>
                        <td>{ll.uv}</td>
                        <td>{ll.ir}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>