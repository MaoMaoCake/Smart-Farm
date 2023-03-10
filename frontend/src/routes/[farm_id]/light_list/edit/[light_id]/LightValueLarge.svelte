<script>
    export let name;
    export let natural;
    export let uv;
    export let ir;
</script>
<div>
    <div class="flex grow flex-col bg-gray-300 rounded-xl">
        <div class="w-full bg-secondary flex justify-center items-center white rounded-t-xl">
            <p>{name}</p>
        </div>
        <div class="flex flex-col">
            <div class="flex justify-evenly items-center bg-amber-500 h-32 rounded-xl m-2">
                <div class="flex flex-col items-center grow white">
                    <p>Natural</p>
                    <p>Light</p>
                </div>
                <div class="flex grow items-center justify-center white">
                    {natural}%
                </div>
            </div>
            <div class="flex justify-evenly items-center bg-blue-900 h-32 rounded-xl m-2">
                <div class="flex flex-col items-center grow white">
                    <p>UV</p>
                    <p>Light</p>
                </div>
                <div class="flex grow items-center justify-center white">
                    {uv}%
                </div>
            </div>
            <div class="flex justify-evenly items-center bg-red-900 h-32 rounded-xl m-2">
                <div class="flex flex-col items-center grow white">
                    <p>Infrared</p>
                    <p>Light</p>
                </div>
                <div class="flex grow items-center justify-center white">
                    {ir}%
                </div>
            </div>
        </div>
    </div>
</div>