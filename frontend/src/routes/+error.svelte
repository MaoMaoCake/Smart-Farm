<script>
  import { page } from '$app/stores';
  import {is_verify} from "$lib/SettingStores.js";

    is_verify.set(true);
</script>

{#if $page.error.message === "Not Found"}
  <div class="flex align-center justify-center">
      <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
        <img src="https://cdn.discordapp.com/attachments/802176047096922175/1091638749827444736/logo.png" alt="Logo" class="w-24 h-24">
          <div class="card-body">
             <p class="font-bold text-center text-3xl">Page Not found!</p>
             <p class="text-center text-1xl">404 Error: This link is invalid</p>
          </div>
        </div>
  </div>
  {/if}

<style>
  .card {
    margin-top: 50px;
  }

  img {
  margin-left: auto;
  margin-right: auto;
}
</style>