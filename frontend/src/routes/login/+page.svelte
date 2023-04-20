<script lang="js">
  import {goto} from '$app/navigation'
  import {is_register, logged_in} from "$lib/SettingStores";
  import { FaEye, FaEyeSlash } from "svelte-icons/fa";
  import { PUBLIC_URL_PREFIX } from '$env/static/public'

  let username = "";
  let password = "";
  let showPassword = false;
  is_register.set(true);

  async function login() {
    if (username === "" || password === "") {
      alert("Username or password cannot be empty");
    }

    const bodyFormData = new FormData()
    bodyFormData.append('username', username);
    bodyFormData.append('password', password);

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");

    let requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: bodyFormData,
      redirect: 'follow',
    };

    fetch(`${PUBLIC_URL_PREFIX}/api/token`, requestOptions)
    .then(async response => response_handler(await response.json()))
    .catch(error => console.log('error', error));
  }

  async function response_handler(response) {
    console.log(response)
    if (response.status_code === 401) {
      alert(response.message);
    } else if (response.status_code  === 200) {
      localStorage.setItem('token', response.data.access_token);
      logged_in.set(true);
      is_register.set(false);
      if (response.data.role === "USER" || response.data.role === "VIEWER"){
          goto('/');
      } else {
          goto('/admin-portal/user-list');
      }
    }
  }

  function handlePasswordKeydown(event) {
    if (event.key === "Enter") {
      login();
    }
  }

  function handleKeydown (event) {
    console.log(event.key)
    if ( event.key === 'Enter') {
      login();
    }
  }

</script>
<svelte:window on:keydown={handleKeydown}/>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
    <img src="logo.png" alt="Logo" class="w-24 h-24 mt-10">
      <div class="card-body">
        <p class="font-bold text-center text-3xl">Login</p>
        <div class="form-control">
          <label class="label">
            <span class="label-text">Username or Email</span>
          </label>
          <input type="text" placeholder="username" class="input input-bordered" bind:value={username}/>
        </div>

<div class="form-control">
  <label class="label">
    <span class="label-text">Password</span>
  </label>
  <div class="relative">
    <input
      type={showPassword ? "text" : "password"}
      placeholder="password"
      class="input input-bordered"
      value={password}
      autocomplete="current-password"
      on:input={(e) => (password = e.target.value)}
      on:keydown={handlePasswordKeydown}
    />
    <button
      class="absolute inset-y-0 left-20 pr-1"
      on:click={() => (showPassword = !showPassword)}
    >
      {#if showPassword}
          <FaEyeSlash class="w-6 h-6 text-gray-400" />
      {:else}
          <FaEye class="w-6 h-6 text-gray-400" />
      {/if}
    </button>
  </div>
  <label class="label">
    <a href="/forgot-password" class="label-text-alt link link-hover"
      >Forgot password?</a
    >
  </label>
</div>

        <div class="form-control mt-6">
          <button class="btn btn-primary" on:click={login}>Login</button>
        </div>
         <div class="mt-4 text-center">
          <span>Don't have an account?</span>
          <a href="/register" class="link ml-2">Register</a>
        </div>
      </div>
</div>
</div>

<style>
  .input {
    /* set a fixed height to align with the icon */
    padding-right: 125px;
    height: 40px;
    width: 320px;
  }
  /* adjust the position of the icon */
  .input + button {
    left: 280px;
    top: 50%;
    transform: translateY(-50%);
  }

   img {
  margin-left: auto;
  margin-right: auto;
}
</style>
