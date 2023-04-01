<script lang="js">
  import {is_verify} from "$lib/SettingStores";
  import { FaEye, FaEyeSlash } from "svelte-icons/fa";
  import {page} from "$app/stores";
  import {goto} from "$app/navigation";

  is_verify.set(true);
  let verification_code;
  let newPassword = "";
  let errors = {};
  let confirmPassword = "";
  let showConfirmPassword = false;
  let showNewPassword = false;
  let password_changing = false;

  const myHeaders = new Headers();
    myHeaders.append("Origin", "");

  const bodyFormData = new FormData()
    bodyFormData.append('code', $page.params.verification_code);

  let requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow',
    };

  fetch(`/api/users/password-changing/${$page.params.verification_code}`, requestOptions)
      .then(async response => changing_response_handler(await response.json()))
      .catch(error => console.log('error', error));

  function changing_response_handler(response) {
      console.log(response)
        if (!response.successful) {
            alert(response.message);
        } else if (response.successful) {
            password_changing = response.data;
        };
    }

   async function changePassword() {
    errors = {};

     if (!newPassword) {
      errors.newPassword = 'Password is required';
    } else if (newPassword.length < 6) {
      errors.newPassword = 'Password must be at least 6 characters long';
    } else if (!/(?=.*\d)(?=.*[A-Z]).{6,}/.test(newPassword)) {
      errors.newPassword = 'Password must contain at least 1 capital letter and 1 number';
    }

     if (!confirmPassword) {
      errors.confirmPassword = 'Confirm password is required';
    } else if (newPassword !== confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

     if (Object.keys(errors).length > 0) {
      return;
    }

    const bodyFormData = new FormData()
    bodyFormData.append('code', $page.params.verification_code);
    bodyFormData.append('new_password', newPassword);

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");

    let requestOptions = {
      method: 'PATCH',
      headers: myHeaders,
      body: bodyFormData,
      redirect: 'follow',
    };

    fetch("/api/users/change-password", requestOptions)
    .then(async response => response_handler(await response.json()))
    .catch(error => console.log('error', error));
  }

   function response_handler(response) {
        if (!response.successful) {
            alert(response.message)
        } else if (response.successful) {
            goto('/login')
        };
    }

   function handleKeydown (event) {
    console.log(event.key)
    if ( event.key === 'Enter') {
      changePassword();
    }
  }
</script>
<svelte:window on:keydown={handleKeydown}/>
{#if password_changing}
  <div class="flex align-center justify-center">
    <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <img src="https://cdn.discordapp.com/attachments/802176047096922175/1091638749827444736/logo.png" alt="Logo" class="w-24 h-24 mt-10">
      <div class="card-body">
        <p class="font-bold text-center text-3xl">Change Password</p>
        <div class="form-control">
          <label class="label">
            <span class="label-text">New Password</span>
          </label>
          <div class="relative">
            <input
              type={showNewPassword ? "text" : "password"}
              placeholder="new password"
              class="input input-bordered w-full py-2 px-3 pr-10"
              value={newPassword}
              autocomplete="new-password"
              on:input={(e) => (newPassword = e.target.value)}
            />
            {#if errors.newPassword}
              <p class="text-red-500 text-xs italic">{errors.newPassword}</p>
            {/if}
            <button
             class="absolute inset-y-1 right-0 pr-3 flex items-center h-10 w-10"
              on:click={() => (showNewPassword = !showNewPassword)}
            >
              {#if showNewPassword}
                <FaEyeSlash class="w-6 h-6 text-gray-400" />
              {:else}
                <FaEye class="w-6 h-6 text-gray-400" />
              {/if}
            </button>
          </div>
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text">Confirm New Password</span>
          </label>
          <div class="relative">
            <input
              type={showConfirmPassword ? "text" : "password"}
              placeholder="confirm new password"
              class="input input-bordered w-full py-2 px-3 pr-10"
              value={confirmPassword}
              autocomplete="new-password"
              on:input={(e) => (confirmPassword = e.target.value)}
            />
            {#if errors.confirmPassword}
              <p class="text-red-500 text-xs italic">{errors.confirmPassword}</p>
            {/if}
            <button
              class="absolute inset-y-1 right-0 pr-3 flex items-center h-10 w-10"
              on:click={() => (showConfirmPassword = !showConfirmPassword)}
            >
              {#if showConfirmPassword}
                <FaEyeSlash class="w-6 h-6 text-gray-400" />
              {:else}
                <FaEye class="w-6 h-6 text-gray-400" />
              {/if}
            </button>
          </div>
        </div>
        <div class="form-control mt-6">
          <button class="btn btn-primary" on:click={changePassword}>Change Password</button>
        </div>
      </div>
    </div>
  </div>
  {:else}
   <div class="flex align-center justify-center">
    <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <img src="https://cdn.discordapp.com/attachments/802176047096922175/1091638749827444736/logo.png" alt="Logo" class="w-24 h-24">
        <div class="card-body">
           <p class="font-bold text-center text-3xl">Something went wrong!</p>
           <p class="text-center text-1xl">This link is possibly invalid</p>
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
