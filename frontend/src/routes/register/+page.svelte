<script lang="js">
  import {goto} from '$app/navigation'
  import {is_register, logged_in} from "$lib/SettingStores";
  import { FaEye, FaEyeSlash } from "svelte-icons/fa";

  let username = "";
  let password = "";
  let confirmPassword = "";
  let email = "";
  let showPassword = false;
  let errors = {};

  is_register.set(false);
  logged_in.set(false);

  async function register() {
    errors = {};

    // Validate username
    if (!username) {
      errors.username = 'Username is required';
    } else if (username.length < 3) {
      errors.username = 'Username must be at least 3 characters long';
    }

    // Validate password
    if (!password) {
      errors.password = 'Password is required';
    } else if (password.length < 6) {
      errors.password = 'Password must be at least 6 characters long';
    } else if (!/(?=.*\d)(?=.*[A-Z]).{6,}/.test(password)) {
      errors.password = 'Password must contain at least 1 capital letter and 1 number';
    }

    // Validate confirm password
    if (!confirmPassword) {
      errors.confirmPassword = 'Confirm password is required';
    } else if (password !== confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    // Validate email
    if (!email) {
      errors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      errors.email = 'Invalid email format';
    }

    if (Object.keys(errors).length > 0) {
      return;
    }

    const bodyFormData = new FormData()
    bodyFormData.append('username', username);
    bodyFormData.append('password', password);
    bodyFormData.append('email', email);
    bodyFormData.append('role', 'USER');

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");

    let requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: bodyFormData,
      redirect: 'follow',
    };

    fetch("/api/users/create", requestOptions)
    .then(async response => response_handler(await response.json()))
    .catch(error => console.log('error', error));
  }

  async function response_handler(response) {
    console.log(response)
    if (response.status_code === 400) {
      alert(response.message);
    } else if (response.status_code  === 200) {
      goto('/login');
    }
  }

  function handleKeydown (event) {
    console.log(event.key)
    if ( event.key === 'Enter') {
      register();
    }
  }

</script>
<svelte:window on:keydown={handleKeydown}/>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
    <img src="logo.png" alt="Logo" class="w-24 h-24">
      <div class="card-body">
         <p class="font-bold text-center text-3xl">Register</p>
        <div class="form-control">
          <label class="label">
            <span class="label-text">Username</span>
          </label>
          <input type="text" placeholder="username" class="input input-bordered" bind:value={username} autofocus/>
          {#if errors.username}
            <p class="text-red-500 text-xs italic">{errors.username}</p>
          {/if}
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text">Email</span>
          </label>
          <input type="email" placeholder="email" class="input input-bordered" bind:value={email}/>
          {#if errors.email}
            <p class="text-red-500 text-xs italic">{errors.email}</p>
          {/if}
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text">Password</span>
          </label>
          <div class="relative">
            {#if showPassword}
              <input type="text" name="password" class="input input-bordered w-full py-2 px-3 pr-10" bind:value={password} placeholder="Password">
            {:else}
              <input type="password" name="password" class="input input-bordered w-full py-2 px-3 pr-10" bind:value={password} placeholder="Password">
            {/if}
              <button class="absolute inset-y-1 right-0 pr-3 flex items-center h-10 w-10" on:click={() => showPassword = !showPassword}>
                {#if showPassword}
                <FaEyeSlash class="text-gray-700 cursor-pointer"/>
                {:else}
                <FaEye class="text-gray-700 cursor-pointer"/>
                {/if}
              </button>
          </div>
              {#if errors.password}
              <p class="text-red-500 text-xs italic">{errors.password}</p>
              {/if}
          </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text">Confirm Password</span>
          </label>
          <input type="password"
                 placeholder="confirm password"
                 class="input input-bordered"
                 bind:value={confirmPassword}/>
          {#if errors.confirmPassword}
            <p class="text-red-500 text-xs italic">{errors.confirmPassword}</p>
          {/if}
        </div>
        <button class="btn btn-primary mt-10" on:click={register}>Register</button>
        <div class="mt-4 text-center">
          <span>Already have an account?</span>
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
