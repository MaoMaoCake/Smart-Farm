<script lang="ts">
    import {goto} from "$app/navigation";
    import {is_admin, is_register} from "../../../lib/SettingStores";
    import { paginate, DarkPaginationNav, LightPaginationNav } from 'svelte-paginate'
    import Icon from '@iconify/svelte';

    is_admin.set(true);
    is_register.set(false);

    let ESPs = [];
    let currentPage = 1;
    let pageSize = 5;
    let searchText = "";
    let filter = "all";

     $: filteredESPs = ESPs.filter((esp) => {
        if (!searchText) return true;
        return (
            esp.id.toString().includes(searchText.toLowerCase())
        );
        }).filter((esp) => {
        if (filter === "all") return true;
        if (filter === "InUse") return esp.isUsed == true;
        if (filter === "NotInUse") return esp.isUsed == false;
      });

    $: paginatedUsers = paginate({ items: filteredESPs, pageSize, currentPage });
    $: theme = localStorage.getItem("theme") === 'sf_light';

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");
    myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

    fetch(
            `http://127.0.0.1:8000/api/admin/list/ESPs`,
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
            ESPs = response.data;
        };
    }

    function handleSearch(e) {
        searchText = e.target.value.trim();
        currentPage = 1;
    }

    function showAll() {
    filter = "all"
    }

function showInUse() {
  filter = "InUse"
}

function showNotInUse() {
  filter = "NotInUse"
}


</script>
<h1 class="text-1xl font-bold mb-4 mt-10 flex justify-center">Admin Portal</h1>
<div class="container mx-auto mt-12 items-center justify-center">
   <div class="tabs items-center justify-center">
    <a class="tab tab-bordered" href="/admin-portal/user-list">
      <Icon icon="material-symbols:person"/>User List</a>
    <a class="tab tab-bordered" href="/admin-portal/farm-list">
      <Icon icon="mdi:farm-home"/>Farm list</a>
    <a class="tab tab-bordered tab-active">
      <Icon icon="material-symbols:motion-sensor-active-sharp"/>ESP list</a>
  </div>
  <h1 class="text-3xl font-bold mb-4 mt-10 flex items-center">ESP List <Icon icon="material-symbols:motion-sensor-active-sharp"/></h1>
  <div class="search-wrapper mb-4 flex items-center rounded-lg border border-gray-300 px-3 py-2">
  <Icon icon="bi:search" class="mr-2 text-gray-400"/>
  <input type="text" placeholder="Search ESPs..." on:input={handleSearch} class="w-full bg-transparent focus:outline-none "/>
     {#if filter === "all"}
        <button class="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded" style="white-space: nowrap;">All</button>
      {:else if filter === "InUse"}
        <button class="bg-green-600 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">In Use</button>
      {:else if filter === "NotInUse"}
      <button class="bg-red-600 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">Not In Use</button>
     {/if}
</div>

  <button on:click={showAll} class="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded mr-4">All</button>
<button on:click={showInUse} class="bg-green-600 text-white font-bold py-2 px-4 rounded mr-4">In Use</button>
<button on:click={showNotInUse} class="bg-red-600 text-white font-bold py-2 px-4 rounded mr-4">Not In Use</button>

  <table class="table table-auto w-full">
    <thead>
      <tr>
        <th>ESP ID</th>
        <th>In use</th>
        <th>Available</th>
        <th>Registered At</th>
      </tr>
    </thead>
      <tbody>
        {#each paginatedUsers as esp}
          <tr>
            <td>{esp.id}</td>
            {#if esp.isUsed}
              <td><p class="bg-green-900 rounded pl-6 pr-5 white w-20">{esp.isUsed}</p></td>
            {:else }
              <td><p class="bg-red-900 rounded pl-6 pr-5 white w-20">{esp.isUsed}</p></td>
            {/if}
             {#if esp.isAvailable}
              <td><p class="bg-green-900 rounded pl-6 pr-5 white w-20">{esp.isAvailable}</p></td>
            {:else }
              <td><p class="bg-red-900 rounded pl-6 pr-5 white w-20">{esp.isAvailable}</p></td>
            {/if}
            <td>{esp.createAt}</td>
          </tr>
          {/each}
      </tbody>
    </table>
  {#if !ESPs?.length}
    <div class="flex flex-col justify-center items-center p-10">
      <Icon icon="tabler:tools-off" class="w-52 h-52"/>
      <p class="mt-10 mb-10">No ESP found!</p>
    </div>
  {/if}
 <div class="pagination-wrapper mt-15">
  {#if theme}
    <LightPaginationNav
    totalItems="{filteredESPs.length}"
    pageSize="{pageSize}"
    currentPage="{currentPage}"
    limit="{1}"
    showStepOptions="{true}"
    on:setPage="{(e) => currentPage = e.detail.page}"
  />
    {:else }
     <DarkPaginationNav
    totalItems="{filteredESPs.length}"
    pageSize="{pageSize}"
    currentPage="{currentPage}"
    limit="{1}"
    showStepOptions="{true}"
    on:setPage="{(e) => currentPage = e.detail.page}"
  />
    {/if}
</div>
</div>
