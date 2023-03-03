<script lang="ts">
    import type {PageData} from "./$types";
    import LightValueSmall from "./LightValueSmall.svelte";
    export let data: PageData;
    let natural;
    let uv;
    let ir;

</script>
<div class="flex grow flex-col justify-center items-center md:flex-row">
    <div class="flex md:hidden">
        <LightValueSmall name={"light 1"} natural={23} uv={10} ir={12}/>
    </div>
    <div class="flex flex-col grow">
        <div class="flex grow">Light Automation</div>
        <div class="flex flex-col grow">
            <div class="flex">
                <p>Natural Light</p>
                <input type="text" bind:value={natural} class="input input-bordered w-full max-w-xs" />
            </div>
            <div class="flex flex-col">
                <input type="range" min="0" max="100" bind:value={natural} class="range" step="10" />
            </div>
        </div>
        <div class="flex"></div>
        <div class="flex"></div>
        <div class="flex"></div>
    </div>
</div>