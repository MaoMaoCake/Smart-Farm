<script lang="ts">
    import {goto} from "$app/navigation";
    import { onMount } from 'svelte';

    let ac_name = null;
    let farm_id;
    let ac_id;
    let initial_name = null;

    onMount(() => {
      const urlParams = new URLSearchParams(window.location.search);
      ac_name = urlParams.get('ac_name');
      farm_id = urlParams.get('farm_id');
      ac_id = urlParams.get('ac_id');
    });

    $: {
        if (ac_name && initial_name == null) {
          initial_name = ac_name;
        }
    }

    function change_name(){
      if (/^ *$/.test(ac_name)){
        alert("Farm name cannot be empty or solely spaces");
      }

      const myHeaders = new Headers();
      myHeaders.append("Origin", "");
      myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

      fetch(
          `/api/farm/${farm_id}/AC/${ac_id}?name=${ac_name}`,
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
            goto(`/${farm_id}/ac_list`);
        };
    }
</script>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Enter new AC name</span>
          </label>
          <input type="text" class="input input-bordered" bind:value={ac_name}/>
        </div>
        <div class="form-control mt-5">
          <button class="btn btn-secondary white"
                  on:click={change_name}
                  disabled={ac_name == initial_name || /^ *$/.test(ac_name)}
          >Enter</button>
        </div>
        <div class="form-control mt-5">
            <a href="{farm_id}/light_preset" class="btn btn-primary white">Cancel</a>
        </div>
      </div>
  </div>
</div>