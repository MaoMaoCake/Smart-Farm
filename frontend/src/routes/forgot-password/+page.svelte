<script lang="js">
  import {is_verify} from "$lib/SettingStores";
  import {goto} from '$app/navigation'

  is_verify.set(true);
  let verification_code;
  let verify_success = null;
  let email = "";
  let errors = {};


   async function sendResetPasswordEmail() {
    errors = {};

    if (!email) {
      errors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      errors.email = 'Invalid email format';
    }

     if (Object.keys(errors).length > 0) {
      return;
    }

    const bodyFormData = new FormData()
    bodyFormData.append('email', email);

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");

    let requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: bodyFormData,
      redirect: 'follow',
    };

    fetch("/api/users/forget-password", requestOptions)
    .then(async response => response_handler(await response.json()))
    .catch(error => console.log('error', error));
  }

   function response_handler(response) {
        if (!response.successful) {
            alert(response.message);
        } else if (response.successful) {
           goto('/login');
        };
    }

   function handleKeydown (event) {
    console.log(event.key)
    if ( event.key === 'Enter') {
      sendResetPasswordEmail();
    }
  }
</script>
<svelte:window on:keydown={handleKeydown}/>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
    <img src="logo.png" alt="Logo" class="w-24 h-24 mt-10">
    <div class="card-body">
      <p class="font-bold text-center text-3xl">Forgot Password</p>
      <div class="form-control">
        <label class="label">
          <span class="label-text">Email</span>
        </label>
        <input type="email" placeholder="email" class="input input-bordered" bind:value={email}/>
               <div>
              {#if errors.email}
              <p class="text-red-500 text-xs italic">{errors.email}</p>
              {/if}
          </div>
      </div>
      <div class="form-control mt-6">
        <button class="btn btn-primary" on:click={sendResetPasswordEmail}>Send Reset Password Email</button>
      </div>
      <div class="mt-4 text-center">
        <span>Remembered your password?</span>
        <a href="/login" class="link ml-2">Login</a>
      </div>
    </div>
  </div>
</div>
<style>
  .card {
    margin-top: 50px;
  }

  img {
  margin-left: auto;
  margin-right: auto;
}
</style>
