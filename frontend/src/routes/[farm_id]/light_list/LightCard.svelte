<script lang="ts">
    export let name;
    export let natural;
    export let uv;
    export let ir;

</script>
<div class="w-96 h-52 bg-gray-300 rounded-xl m-5 flex items-center justify-center bg-gray-300">
    <div class="flex flex-col grow h-52">
        <div class="flex grow white bg-secondary rounded-t-xl min-w-max h-1/6 pt-2 pb-2 items-center justify-center">
            <p>{name}</p>
        </div>
        <div class="flex grow min-w-max h-5/6 justify-evenly items-center pl-2 pr-2">
            <div class="flex flex-col items-center justify-center white text-lg bg-amber-500 w-1/3 aspect-square rounded-xl m-2 grow">
                <p>Natural</p>
                <p>Light</p>
                <p>{natural}%</p>
            </div>
            <div class="flex flex-col items-center justify-center white text-lg bg-blue-900 w-1/3 aspect-square rounded-xl m-2 grow">
                <p>UV</p>
                <p>Light</p>
                <p>{uv}%</p>
            </div>
            <div class="flex flex-col items-center justify-center white text-lg bg-red-900 w-1/3 aspect-square rounded-xl m-2 grow">
                <p>Infrared</p>
                <p>Light</p>
                <p>{ir}%</p>
            </div>
        </div>
    </div>

</div>