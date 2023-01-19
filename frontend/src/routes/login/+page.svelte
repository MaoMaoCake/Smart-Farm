<script lang="ts">
  let username = "";
  let password = "";

  function login() {
    if (username == "" || password == ""){
      alert("Username or password cannot be empty");
    } else {
      alert(`username: ${username} password: ${password}`);
    }
  }
</script>
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
          <input type="text" placeholder="password" class="input input-bordered" bind:value={password}/>
          <label class="label">
            <a href="forgot-password" class="label-text-alt link link-hover">Forgot password?</a>
          </label>
        </div>
        <div class="form-control mt-6">
          <button class="btn btn-primary" on:click={login}>Login</button>
        </div>
      </div>
</div>
</div>
