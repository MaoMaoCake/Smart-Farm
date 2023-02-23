<script lang="ts">
    export let name;
    export let temp;
    export let status;
</script>
<div class="w-96 h-52 bg-gray-300 rounded-xl m-5 flex items-center justify-center">
    <div class="flex flex-col grow h-52">
        <div class="flex grow white bg-secondary rounded-t-xl min-w-max h-1/6 pt-2 pb-2 items-center justify-center">
            <p>{name}</p>
        </div>
        <div class="flex grow min-w-max h-5/6 justify-evenly items-center">
            <div class="flex aspect-square bg-blue-900 h-24 w-24 white">
                <p>{status}</p>
            </div>
            <div class="flex">
                <p>ON</p>
                <input type="checkbox" class="toggle" bind:checked={status} />
                <p>OFF</p>
            </div>
        </div>
    </div>
</div>