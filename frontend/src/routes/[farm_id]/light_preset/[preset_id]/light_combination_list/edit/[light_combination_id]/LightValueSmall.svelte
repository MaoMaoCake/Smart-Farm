<script lang="ts">
    export let name;
    export let natural
    export let ir;
    export let uv
</script>
<div class="flex grow flex-col bg-gray-300 rounded-xl m-5">
    <div class="white flex bg-secondary grow h-10 items-center rounded-t-xl justify-center">
        <p class="min-w-max">{name}</p>
    </div>
    <div class="flex grow justify-evenly">
        <div class="flex bg-amber-500 flex-col white justify-center items-center rounded-xl w-24 grow aspect-square m-3 min-w-max">
            <div class="flex">
                <p>Natural</p>
            </div>
            <div class="flex">
                <p>Light</p>
            </div>
            <div class="flex">
                <p>{natural}%</p>
            </div>
        </div>
        <div class="flex bg-blue-900 flex-col white justify-center items-center rounded-xl w-24 grow aspect-square m-3 min-w-max">
            <div class="flex">
                <p>UV</p>
            </div>
            <div class="flex">
                <p>Light</p>
            </div>
            <div class="flex">
                <p>{uv}%</p>
            </div>
        </div>
        <div class="flex bg-red-900 flex-col white justify-center items-center rounded-xl w-24 grow aspect-square m-3 min-w-max">
            <div class="flex">
                <p>Infrared</p>
            </div>
            <div class="flex">
                <p>Light</p>
            </div>
            <div class="flex">
                <p>{ir}%</p>
            </div>
        </div>
    </div>
</div>