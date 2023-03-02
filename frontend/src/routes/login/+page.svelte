<script lang="js">
  import {goto} from '$app/navigation'
  let username = "gnnchya3";
  let password = "gunn";
  const endpoint = "http://127.0.0.1:8000/token";


  async function login() {
    if (username == "" || password == "") {
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
      console.log(response.message)
      alert(response.message);
    } else if (response.status_code  === 200) {
      localStorage.setItem('token', response.access_token);
      goto('/');
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
