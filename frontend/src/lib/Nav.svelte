<script lang="ts">
    import { onMount } from 'svelte'
    import {logged_in, is_register, is_verify, is_admin} from "./SettingStores";
    import { themeChange } from 'theme-change'
    import {goto} from '$app/navigation'
    let checked = localStorage.getItem("theme") === 'sf_light'

    onMount(() => {
      themeChange(false);
    })

    function logout(){
        localStorage.removeItem("token")
        $logged_in = false
        goto("/login")
    }
</script>
<div class="h-16"> <!-- This is to make the navbar spacing -->
</div>
<div class="navbar bg-primary h-16 fixed top-0 left-0 right-0"  style="z-index: 999;">
    <div class="flex-1">
      {#if !$is_verify && !$is_admin}
        <a class="m-5 font-bold white" href="/">AUTO FARM</a>
        {:else }
        <a class="m-5 font-bold white" >AUTO FARM</a>
        {/if}
    </div>
    <div class="flex-none" >
         <ul class="menu menu-horizontal px-1">
             <li>
                <label class="swap swap-rotate">

                  <!-- this hidden checkbox controls the state -->
                  <input type="checkbox" data-toggle-theme="sf_dark,sf_light" data-act-class="ACTIVECLASS" bind:checked/>

                  <!-- sun icon -->
                  <svg class="swap-on fill-current w-5 h-5 white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"/></svg>

                  <!-- moon icon -->
                  <svg class="swap-off fill-current w-5 h-5 white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"/></svg>

                </label>
             </li>
             <li>
               {#if !$is_verify}
                 {#if $is_register}
                      <a class="btn btn-secondary sm:m-2 text-white bg-black border-black" href="/register">Register</a>
                   {:else}
                     {#if $logged_in}
                        <a class="btn btn-secondary sm:m-2 text-white" on:click={logout}>Logout</a>
                    {:else}
                        <a class="btn btn-secondary sm:m-2 text-white" href="/login">Login</a>
                    {/if}
                 {/if}
               {/if}
             </li>
         </ul>
    </div>
</div>