<script lang="ts">
    import type {PageData} from "./$types";
    import LightValueSmall from "./LightValueSmall.svelte";
    export let data: PageData;
    let natural = 0;
    let uv = 0;
    let ir = 0;



</script>
<div class="flex grow flex-col justify-center items-center md:flex-row">
    <div class="flex md:hidden">
        <LightValueSmall name={"light 1"} natural={23} uv={10} ir={12}/>
    </div>
    <div class="w-full">
        <div class="flex flex-col grow ml-10 mr-10">
            <div class="flex grow">Light Automation</div>
            <div class="flex flex-col grow">
                <div class="flex items-center">
                    <p class="w-full">Natural Light</p>
                    <input type="text" bind:value={natural} class="input input-bordered w-16 max-w-xs" />
                    <p>%</p>
                </div>
                <div class="flex flex-col">
                    <input type="range" min="0" max="100" bind:value={natural} class="range range-xs amber" step="10" />
                </div>
            </div>
            <div class="flex flex-col grow">
                <div class="flex items-center">
                    <p class="w-full">UV Light</p>
                    <input type="text" bind:value={uv} class="input input-bordered w-16 max-w-xs" />
                    <p>%</p>
                </div>
                <div class="flex flex-col">
                    <input type="range" min="0" max="100" bind:value={uv} class="range range-xs blue" step="10" />
                </div>
            </div>
            <div class="flex flex-col grow">
                <div class="flex items-center">
                    <p class="w-full">Infrared Light</p>
                    <input type="text" bind:value={ir} class="input input-bordered w-16 max-w-xs" />
                    <p>%</p>
                </div>
                <div class="flex flex-col">
                    <input type="range" min="0" max="100" bind:value={ir} class="range range-xs red" step="10" />
                </div>
            </div>
            <div class="flex grow justify-center items-center flex-col pt-5">
                <button class="btn btn-secondary text-white w-10/12 m-2">Save</button>
                <button class="btn bg-gray-300 text-black w-10/12 m-2">Apply All & Save</button>
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