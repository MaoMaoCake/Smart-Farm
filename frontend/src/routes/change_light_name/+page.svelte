<script lang="ts">
    import {goto} from "$app/navigation";
    import { onMount } from 'svelte';
    import { PUBLIC_URL_PREFIX } from '$env/static/public'
    import {is_register} from "../../lib/SettingStores";

    is_register.set(false);
    let light_name = null;
    let farm_id;
    let light_id;
    let initial_name = null;

    onMount(() => {
      const urlParams = new URLSearchParams(window.location.search);
      light_name = urlParams.get('light_name');
      farm_id = urlParams.get('farm_id');
      light_id = urlParams.get('light_id');
    });

    $: {
        if (light_name && initial_name == null) {
          initial_name = light_name;
        }
    }

    function change_name(){
      if (/^ *$/.test(light_name)){
        alert("Farm name cannot be empty or solely spaces");
      }

      const myHeaders = new Headers();
      myHeaders.append("Origin", "");
      myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

      fetch(
          `${PUBLIC_URL_PREFIX}/api/farm/${farm_id}/light/${light_id}?name=${light_name}`,
          {
            method: 'PUT',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => response_handler(await response.json()))
        .catch(error => console.log('error', error));
    }

     function response_handler(response) {
        if (!response.successful) {
            alert(response.message);
        } else if (response.successful) {
            alert('Name has been changed successfully!');
            goto(`/${farm_id}/light_list/edit/${light_id}`);
        };
    }
</script>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Enter new light name</span>
          </label>
          <input type="text" class="input input-bordered" bind:value={light_name}/>
        </div>
        <div class="form-control mt-5">
          <button class="btn btn-secondary white"
                  on:click={change_name}
                  disabled={light_name == initial_name || /^ *$/.test(light_name)}
          >Enter</button>
        </div>
        <div class="form-control mt-5">
            <a href="/{farm_id}/light_preset" class="btn btn-primary white">Cancel</a>
        </div>
      </div>
  </div>
</div>