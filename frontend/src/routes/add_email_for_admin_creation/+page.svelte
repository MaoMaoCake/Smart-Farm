<script lang="ts">
    import {goto} from "$app/navigation";
    import { PUBLIC_URL_PREFIX } from '$env/static/public'


    let email = "";
    let errors = "";

    function create_new_admin() {
        errors = "";

        if (!email) {
          errors= 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(email)) {
          errors = 'Invalid email format';
        }

        if (errors) {
            return;
        }

      const myHeaders = new Headers();
      myHeaders.append("Origin", "");

       const bodyFormData = new FormData()
       bodyFormData.append('email', email);

           fetch(
              `${PUBLIC_URL_PREFIX}/api/admin/create/admin`,
            {
              method: 'POST',
              headers: myHeaders,
              body: bodyFormData,
              redirect: 'follow'
            })
          .then(async response => response_handler(await response.json()))
          .catch(error => console.log('error', error));

      function response_handler(response) {
          if (!response.successful) {
              alert(response.message);
          } else if (response.successful) {
              goto('/admin-portal/user-list');
          };
      }
    }

</script>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Enter a valid email to register new admin</span>
          </label>
          <input type="text" class="input input-bordered" bind:value={email}/>
           {#if errors}
            <p class="text-red-500 text-xs italic">{errors}</p>
          {/if}
        </div>
        <div class="form-control mt-5">
          <button class="btn btn-secondary white"
                  on:click={create_new_admin}
                  disabled={false || /^ *$/.test(email)}
          >Enter</button>
        </div>
        <div class="form-control mt-5">
            <a href='/admin-portal/user-list' class="btn btn-primary white">Cancel</a>
        </div>
      </div>
  </div>
</div>