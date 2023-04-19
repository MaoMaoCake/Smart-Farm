<script lang="js">
  import {is_verify} from "$lib/SettingStores";
  import {onMount} from "svelte";
  import {page} from "$app/stores";
  import { PUBLIC_URL_PREFIX } from '$env/static/public'


  is_verify.set(true);
  let verification_code;
  let verify_success = null;

  onMount(() => {
      const urlParams = new URLSearchParams(window.location.search);
      verification_code = urlParams.get('verification_code');
    });

  const myHeaders = new Headers();
      myHeaders.append("Origin", "");

   fetch(`${PUBLIC_URL_PREFIX}/api/users/verify/${$page.params.verification_code}`, {
            method: 'POST',
            headers: myHeaders,
            redirect: 'follow'
          })
    .then(async response => response_handler(await response.json()))
    .catch(error => console.log('error', error));

   function response_handler(response) {
        if (!response.successful) {
            verify_success = false;
        } else if (response.successful) {
            verify_success = true;
        };
    }

</script>
{#if verify_success != null}
  <div class="flex align-center justify-center">
    <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <img src="https://cdn.discordapp.com/attachments/802176047096922175/1091638749827444736/logo.png" alt="Logo" class="w-24 h-24">
        <div class="card-body">
          {#if verify_success}
           <p class="font-bold text-center text-3xl">Email verified!</p>
           <p class="text-center text-1xl">You can now login</p>
            {:else }
            <p class="font-bold text-center text-3xl">Something went wrong!</p>
           <p class="text-center text-1xl">Please contact the admin</p>
            {/if}
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
