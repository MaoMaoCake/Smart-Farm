<script lang="ts">
    import {goto} from "$app/navigation";
    import {is_admin, is_register} from "../../../lib/SettingStores";
    import { paginate, DarkPaginationNav, LightPaginationNav } from 'svelte-paginate'
    import Icon from '@iconify/svelte';

    is_admin.set(true);
    is_register.set(false);

    let users = [];
    let currentPage = 1;
    let pageSize = 5;
    let searchText = "";

     $: filteredUsers = users.filter((user) => {
        if (!searchText) return true;
        return (
            user.username.toLowerCase().includes(searchText.toLowerCase()) ||
            user.email.toString().toLowerCase().includes(searchText.toLowerCase())
        );
    });
    $: paginatedUsers = paginate({ items: filteredUsers, pageSize, currentPage });
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

    function handleSearch(e) {
        searchText = e.target.value.trim();
        currentPage = 1;
    }

</script>
<h1 class="text-1xl font-bold mb-4 mt-10 flex justify-center">Admin Portal</h1>
<div class="container mx-auto mt-12 items-center justify-center">
   <div class="tabs items-center justify-center">
    <a class="tab tab-bordered tab-active">
      <Icon icon="material-symbols:person"/>User List</a>
    <a class="tab tab-bordered" href="/admin-portal/farm-list">
      <Icon icon="mdi:farm-home"/>Farm list</a>
    <a class="tab tab-bordered" href="/admin-portal/esp-list">
      <Icon icon="material-symbols:motion-sensor-active-sharp"/>ESP list</a>
  </div>
  <h1 class="text-3xl font-bold mb-4 mt-10 flex items-center">User List <Icon icon="material-symbols:person"/></h1>
  <div class="search-wrapper mb-4 flex items-center rounded-lg border border-gray-300 px-3 py-2">
  <Icon icon="bi:search" class="mr-2 text-gray-400"/>
  <input type="text" placeholder="Search Users..." on:input={handleSearch} class="w-full bg-transparent focus:outline-none "/>
</div>

  <table class="table w-full">
    <thead>
      <tr>
        <th>Username</th>
        <th>Email</th>
        <th>Role</th>
        <th>Verified</th>
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
            {#if user.verified}
              <td><p class="bg-green-900 rounded pl-6 pr-5 white w-20">{user.verified}</p></td>
            {:else }
              <td><p class="bg-red-900 rounded pl-6 pr-5 white w-20">{user.verified}</p></td>
            {/if}
            <td>{user.createAt}</td>
            <td class="text-right">
              <a href={`users/${user.id}`} class="btn btn-primary">View Details</a>
            </td>
          </tr>
          {/each}
      </tbody>
    </table>
  {#if !users?.length}
    <div class="flex flex-col justify-center items-center p-10">
      <Icon icon="material-symbols:person-off" class="w-52 h-52"/>
      <p class="mt-10 mb-10">No user found!</p>
    </div>
  {/if}
 <div class="pagination-wrapper mt-15">
  {#if theme}
    <LightPaginationNav
    totalItems="{filteredUsers.length}"
    pageSize="{pageSize}"
    currentPage="{currentPage}"
    limit="{1}"
    showStepOptions="{true}"
    on:setPage="{(e) => currentPage = e.detail.page}"
  />
    {:else }
     <DarkPaginationNav
    totalItems="{filteredUsers.length}"
    pageSize="{pageSize}"
    currentPage="{currentPage}"
    limit="{1}"
    showStepOptions="{true}"
    on:setPage="{(e) => currentPage = e.detail.page}"
  />
    {/if}
</div>
</div>
