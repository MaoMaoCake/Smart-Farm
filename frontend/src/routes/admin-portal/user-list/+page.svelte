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
    let filter = "all";
    let sort = 'desc';

     $: filteredUsers = users.filter((user) => {
        if (!searchText) return true;
        return (
            user.username.toLowerCase().includes(searchText.toLowerCase()) ||
            user.email.toString().toLowerCase().includes(searchText.toLowerCase())
        );
        }).filter((esp) => {
        if (filter === "all") return true;
        if (filter === "verified") return esp.verified == true;
        if (filter === "unverified") return esp.verified == false;
    }).sort((a, b) => {
        if (sort === 'asc') {
            return new Date(a.createAt) - new Date(b.createAt);
        } else {
            return new Date(b.createAt) - new Date(a.createAt);
        }
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

      function showAll() {
    filter = "all"
    }

    function showVerified() {
      filter = "verified"
    }

    function showUnverified() {
      filter = "unverified"
    }

    function toggleSort() {
      sort = sort === 'asc' ? 'desc' : 'asc';
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
  <div class="mt-5  text-right">
    <a class="btn btn-primary" href="/add_email_for_admin_creation">
      <Icon icon="material-symbols:person"/>
      Add New Admin
    </a>
  </div>
  <h1 class="text-3xl font-bold mb-4 mt-5 flex items-center">User List <Icon icon="material-symbols:person"/></h1>
  <div class="search-wrapper mb-4 flex items-center rounded-lg border border-gray-300 px-3 py-2">
  <Icon icon="bi:search" class="mr-2 text-gray-400"/>
  <input type="text" placeholder="Search Users..." on:input={handleSearch} class="w-full bg-transparent focus:outline-none "/>
    {#if filter === "all"}
        <button class="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded" style="white-space: nowrap;">All</button>
      {:else if filter === "verified"}
        <button class="bg-green-600 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">Verified</button>
      {:else if filter === "unverified"}
      <button class="bg-red-600 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">Unverified</button>
     {/if}

        <button class="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded ml-2" style="white-space: nowrap;">
   {#if sort === 'asc'}
     <span class="flex items-center">
       Sort: Old to New
       <Icon icon="material-symbols:arrow-circle-up-outline" class="w-5 h-5"/>
     </span>
    {:else }
     <span class="flex items-center">
       Sort: New to Old
       <Icon icon="material-symbols:arrow-circle-down-outline" class="w-5 h-5"/>
     </span>
    {/if}
</button>
</div>

    <button on:click={showAll} class="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded mr-4">All</button>
    <button on:click={showVerified} class="bg-green-600 text-white font-bold py-2 px-4 rounded mr-4">Verified</button>
    <button on:click={showUnverified} class="bg-red-600 text-white font-bold py-2 px-4 rounded mr-4">Unverified</button>
    <button on:click={toggleSort} class="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded mr-4">
       {#if sort === 'asc'}
         <span class="flex items-center">
           Sort: Old to New
           <Icon icon="material-symbols:arrow-circle-up-outline" class="w-5 h-5"/>
         </span>
        {:else }
         <span class="flex items-center">
           Sort: New to Old
           <Icon icon="material-symbols:arrow-circle-down-outline" class="w-5 h-5"/>
         </span>
        {/if}
    </button>

  <table class="table table-auto w-full mt-5">
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
            {#if user.role != 'ADMIN'}
             <td class="text-right">
              <a href={`users/${user.id}`} class="btn btn-primary">View Details</a>
            </td>
            {/if}
          </tr>
          {/each}
      </tbody>
    </table>
  {#if !filteredUsers?.length}
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
