<script lang="js">
  import {goto} from '$app/navigation'
  import {logged_in} from "$lib/SettingStores";
  import { FaEye, FaEyeSlash } from "svelte-icons/fa";

  let username = "";
  let password = "";
  let showPassword = false;

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

    fetch("http://127.0.0.1:8000/token", requestOptions)
    .then(async response => response_handler(await response.json()))
    .catch(error => console.log('error', error));
  }

  async function response_handler(response) {
    console.log(response)
    if (response.status_code === 401) {
      alert(response.message);
    } else if (response.status_code  === 200) {
      localStorage.setItem('token', response.data.access_token);
      logged_in.set(true)
      goto('/');
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
      <div class="card-body">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Username</span>
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
    <a href="forgot-password" class="label-text-alt link link-hover"
      >Forgot password?</a
    >
  </label>
</div>

        <div class="form-control mt-6">
          <button class="btn btn-primary" on:click={login}>Login</button>
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
</style>
