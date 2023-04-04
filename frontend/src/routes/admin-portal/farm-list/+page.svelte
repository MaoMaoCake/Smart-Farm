<script lang="ts">
    import {goto} from "$app/navigation";
    import {is_admin, is_register} from "../../../lib/SettingStores";
    import { paginate, DarkPaginationNav, LightPaginationNav } from 'svelte-paginate'
    import Icon from '@iconify/svelte';
    import {writable} from "svelte/store";

    is_admin.set(true);
    is_register.set(false);

    let farms = [];
    let currentPage = 1;
    let pageSize = 5;
    let searchText = "";
    let sort = 'desc';

    $: selectedRow = writable(null);

     $: filteredFarms = farms.filter((farm) => {
        if (!searchText) return true;
        return (
            farm.name.toLowerCase().includes(searchText.toLowerCase()) ||
            farm.id.toString().toLowerCase().includes(searchText.toLowerCase()) ||
            farm.farmKey.toLowerCase().includes(searchText.toLowerCase())
        );
    }).sort((a, b) => {
        if (sort === 'asc') {
            return new Date(a.createAt) - new Date(b.createAt);
        } else {
            return new Date(b.createAt) - new Date(a.createAt);
        }
    });

    $: paginatedFarms = paginate({ items: filteredFarms, pageSize, currentPage });
    $: theme = localStorage.getItem("theme") === 'sf_light';

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");
    myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

    fetch(
            `http://127.0.0.1:8000/api/admin/list/farms`,
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
            farms = response.data;
        };
    }

    function copyToClipboard(text, index) {
        navigator.clipboard.writeText(text);
        selectedRow = index;
        setTimeout(() => { selectedRow = null; }, 1000);
    }

    function handleSearch(e) {
        searchText = e.target.value.trim();
        currentPage = 1;
    }

    function toggleSort() {
      sort = sort === 'asc' ? 'desc' : 'asc';
    }

    function create_new_farm() {
         fetch(
            `http://127.0.0.1:8000/api/admin/create/farm`,
          {
            method: 'POST',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => response_handler(await response.json()))
        .catch(error => console.log('error', error));

    function response_handler(response) {
        if (!response.successful) {
            alert(response.message);
        } else if (response.successful) {
            location.reload();
        };
    }
    }

</script>
<h1 class="text-1xl font-bold mb-4 mt-10 flex justify-center">Admin Portal</h1>
<div class="container mx-auto mt-12 items-center justify-center">
   <div class="tabs items-center justify-center">
    <a class="tab tab-bordered" href="/admin-portal/user-list">
      <Icon icon="material-symbols:person"/>User List</a>
    <a class="tab tab-bordered  tab-active">
      <Icon icon="mdi:farm-home"/>Farm list</a>
    <a class="tab tab-bordered" href="/admin-portal/esp-list">
      <Icon icon="material-symbols:motion-sensor-active-sharp"/>ESP list</a>
  </div>
  <div class="mt-5  text-right">
    <button on:click ={create_new_farm} class="btn btn-primary">
      <Icon icon="mdi:box-add"/>
      Add New Farm
    </button>
  </div>


  <h1 class="text-3xl font-bold mb-4 mt-5 flex items-center">Farm List<Icon icon="mdi:farm-home"/></h1>
   <div class="search-wrapper mb-4 flex items-center rounded-lg border border-gray-300 px-3 py-2">
  <Icon icon="bi:search" class="mr-2 text-gray-400"/>
  <input type="text" placeholder="Search Farms..." on:input={handleSearch} class="w-full bg-transparent focus:outline-none"/>
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
        <th>Farm ID</th>
        <th>Farm Name</th>
        <th>Farm Key</th>
        <th>Created At</th>
        <th></th>
      </tr>
    </thead>
      <tbody>
        {#each paginatedFarms as farm, i}
          <tr >
            <td>{farm.id}</td>
            <td>{farm.name}</td>
            <td class="flex items-center">
              {farm.farmKey}
              <button class="copy" on:click={() =>
              copyToClipboard(farm.farmKey, i)}>
                {#if i === selectedRow}
                  <Icon icon="material-symbols:check-small" class="ml-1"/>
                {:else}
                  <Icon icon="material-symbols:content-copy" class="ml-1"/>
                {/if}
              </button>
            </td>
            <td>{farm.createAt}</td>
            <td class="text-right">
              <a href={`/admin-portal/farm/${farm.id}?farm_name=${farm.name}`} class="btn btn-primary">View Details</a>
            </td>
          </tr>
          {/each}
      </tbody>
    </table>
  {#if !filteredFarms?.length}
    <div class="flex flex-col justify-center items-center p-10">
      <Icon icon="mdi:farm" class="w-52 h-52"/>
      <p class="mt-10 mb-10">No farm found!</p>
    </div>
  {/if}
 <div class="pagination-wrapper mt-15">
  {#if theme}
    <LightPaginationNav
    totalItems="{filteredFarms.length}"
    pageSize="{pageSize}"
    currentPage="{currentPage}"
    limit="{1}"
    showStepOptions="{true}"
    on:setPage="{(e) => currentPage = e.detail.page}"
  />
    {:else }
     <DarkPaginationNav
    totalItems="{filteredFarms.length}"
    pageSize="{pageSize}"
    currentPage="{currentPage}"
    limit="{1}"
    showStepOptions="{true}"
    on:setPage="{(e) => currentPage = e.detail.page}"
  />
    {/if}
</div>
</div>

<style>
  .copy:hover {
    color: gray;
  }
</style>
