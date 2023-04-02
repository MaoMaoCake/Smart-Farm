<script lang="ts">
    import {goto} from "$app/navigation";
    import {is_admin, is_register} from "../../../lib/SettingStores";
    import { paginate, DarkPaginationNav, LightPaginationNav } from 'svelte-paginate'

    is_admin.set(true);
    is_register.set(false);

    let users = [];
    let currentPage = 1;
    let pageSize = 7;

    $: paginatedUsers = paginate({ items: users, pageSize, currentPage });
    $: theme = localStorage.getItem("theme") === 'sf_light';

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");
    myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

    fetch(
            `http://127.0.0.1:8000/api/admin/list/users`,
          {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => response_handler(await response.json()))
        .catch(error => console.log('error', error));

    function response_handler(response) {
        if (!response.successful) {
            goto(`/login`);
        } else if (response.successful) {
            users = response.data;
        };
    }

</script>
<div class="container mx-auto mt-12 items-center justify-center">
   <div class="tabs items-center justify-center">
    <a class="tab tab-bordered tab-active">User List</a>
    <a class="tab tab-bordered">Farm list</a>
    <a class="tab tab-bordered">ESP list</a>
  </div>
  <h1 class="text-3xl font-bold mb-4 mt-10">User List</h1>
  <table class="table w-full">
    <thead>
      <tr>
        <th>Username</th>
        <th>Email</th>
        <th>Role</th>
        <th>Joined At</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
        {#each paginatedUsers as user}
      <tr>
        <td>{user.username}</td>
        <td>{user.email}</td>
        <td>{user.role}</td>
        <td>{user.createAt}</td>
        <td class="text-right">
          <a href={`users/${user.id}`} class="btn btn-primary">View Details</a>
        </td>
      </tr>
    {/each}

    </tbody>
  </table>
  <div class="pagination-wrapper mt-15">
    {#if theme}
      <LightPaginationNav
      totalItems="{users.length}"
      pageSize="{pageSize}"
      currentPage="{currentPage}"
      limit="{1}"
      showStepOptions="{true}"
      on:setPage="{(e) => currentPage = e.detail.page}"
    />
      {:else }
       <DarkPaginationNav
      totalItems="{users.length}"
      pageSize="{pageSize}"
      currentPage="{currentPage}"
      limit="{1}"
      showStepOptions="{true}"
      on:setPage="{(e) => currentPage = e.detail.page}"
    />
      {/if}

</div>
</div>
