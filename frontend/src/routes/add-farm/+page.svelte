<script lang="ts">
    import {goto} from "$app/navigation";
    import { PUBLIC_URL_PREFIX } from '$env/static/public'
    import {is_register} from "../../lib/SettingStores";

    is_register.set(false);
    let farm_key = "";
    function register_fk(){
      if (farm_key===""){
        alert("Please enter farm key");
      }

      const myHeaders = new Headers();
      myHeaders.append("Origin", "");
      myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

      fetch(
          `${PUBLIC_URL_PREFIX}/api/add?farm_key=${farm_key}`,
          {
            method: 'POST',
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
          goto('/');
        };
    }
</script>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Enter The Key of the farm</span>
          </label>
          <input type="text" class="input input-bordered" bind:value={farm_key}/>
        </div>
        <div class="form-control mt-5">
          <button class="btn btn-secondary white"
                  on:click={register_fk}
                  disabled={farm_key.length == 0}
          >Enter</button>
        </div>
        <div class="form-control mt-5">
            <a href="/" class="btn btn-primary white">Cancel</a>
        </div>
      </div>
  </div>
</div>