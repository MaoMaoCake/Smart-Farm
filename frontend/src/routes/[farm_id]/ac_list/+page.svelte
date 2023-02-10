<script lang="ts">
    import type { PageData } from './$types';
    import StatPreview from "$lib/StatPreview.svelte";
    import {FarmSettings} from "$lib/SettingStores.js"
    export let data: PageData

    $FarmSettings.ac_list = [
        {name: "AC 1",status: true},
        {name: "AC 1",status: true},
        {name: "AC 1",status: false},
        {name: "AC 1",status: false},
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
                <th>Status</th>
                <th></th>
                <th></th>
            </tr>
            </thead>
            <tbody>
            <!-- row 1 -->
                {#each $FarmSettings.ac_list as ac, index}
                    <tr>
                        <th>{index}</th>
                        <td>{ac.name}</td>
                        <td>{ac.status}</td>
                        <td></td>
                        <td>ON <input type="checkbox" class="toggle" bind:checked={ac.status} /> OFF</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>