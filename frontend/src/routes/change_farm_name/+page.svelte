<script lang="ts">
    import {goto} from "$app/navigation";
    import { onMount } from 'svelte';

    let farm_name = null;
    let farm_id;
    let initial_name = null;

    onMount(() => {
      const urlParams = new URLSearchParams(window.location.search);
      farm_name = urlParams.get('farm_name');
      farm_id = urlParams.get('farm_id');
    });

    $: {
        if (farm_name && initial_name == null) {
          initial_name = farm_name;
        }
    }

    function change_name(){
      if (/^ *$/.test(farm_name)){
        alert("Farm name cannot be empty or solely spaces");
      }

      const myHeaders = new Headers();
      myHeaders.append("Origin", "");
      myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

      fetch(
          `http://127.0.0.1:8000/farm/${farm_id}?name=${farm_name}`,
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
            goto(`${farm_id}/settings`);
        };
    }
</script>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Enter farm name</span>
          </label>
          <input type="text" class="input input-bordered" bind:value={farm_name}/>
        </div>
        <div class="form-control mt-5">
          <button class="btn btn-secondary white"
                  on:click={change_name}
                  disabled={farm_name == initial_name || /^ *$/.test(farm_name)}
          >Enter</button>
        </div>
        <div class="form-control mt-5">
            <a href="{farm_id}/settings" class="btn btn-primary white">Cancel</a>
        </div>
      </div>
  </div>
</div>