<script lang="ts">
    import {goto} from "$app/navigation";
    import { onMount } from 'svelte';
    import { PUBLIC_URL_PREFIX } from '$env/static/public'


    let preset_name = null;
    let farm_id;
    let preset_id;
    let initial_name = null;

    onMount(() => {
      const urlParams = new URLSearchParams(window.location.search);
      preset_name = urlParams.get('preset_name');
      farm_id = urlParams.get('farm_id');
      preset_id = urlParams.get('preset_id');
    });

    $: {
        if (preset_name && initial_name == null) {
          initial_name = preset_name;
        }
    }

    function change_name(){
      if (/^ *$/.test(preset_name)){
        alert("Farm name cannot be empty or solely spaces");
      }

      const myHeaders = new Headers();
      myHeaders.append("Origin", "");
      myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

      fetch(
          `${PUBLIC_URL_PREFIX}/api/farm/${farm_id}/${preset_id}?name=${preset_name}`,
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
            goto(`/${farm_id}/light_preset`);
        };
    }
</script>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Enter preset name</span>
          </label>
          <input type="text" class="input input-bordered" bind:value={preset_name}/>
        </div>
        <div class="form-control mt-5">
          <button class="btn btn-secondary white"
                  on:click={change_name}
                  disabled={preset_name == initial_name || /^ *$/.test(preset_name)}
          >Enter</button>
        </div>
        <div class="form-control mt-5">
            <a href="/{farm_id}/light_preset" class="btn btn-primary white">Cancel</a>
        </div>
      </div>
  </div>
</div>