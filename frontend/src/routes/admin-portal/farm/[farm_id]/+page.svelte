<script lang="ts">
    import {goto} from "$app/navigation";
    import {is_admin, is_register} from "../../../../lib/SettingStores";
    import { paginate, DarkPaginationNav, LightPaginationNav } from 'svelte-paginate'
    import Icon from '@iconify/svelte';
    import {writable} from "svelte/store";
    import {page} from "$app/stores";
    import { PUBLIC_URL_PREFIX } from '$env/static/public'


    const queryParams = new URLSearchParams(window.location.search);
    const farm_name = queryParams.get('farm_name');

    is_admin.set(true);
    is_register.set(false);

    let sensors = [];
    let currentPage = 1;
    let pageSize = 5;
    let searchText = "";
    let filter = "all";
    let sort = 'desc';
    let ESPs = [];

    $: selectedRow = writable(null);

     $: filteredFarms = sensors.filter((sensor) => {
         if (!searchText) return true;
         return (
             sensor.sensorId.toString().toLowerCase().includes(searchText.toLowerCase()) ||
             sensor.espId.toString().toLowerCase().includes(searchText.toLowerCase())
         );
    }).filter((component) => {
        if (filter === "all") return true;
        if (filter === "light") return component.sensorType == "LIGHT";
        if (filter === "ac") return component.sensorType == "AC";
        if (filter === "water") return component.sensorType == "WATERING";
        if (filter === "co2") return component.sensorType == "CO2_CONTROLLER";
        if (filter === "dehumidifier") return component.sensorType == "DEHUMIDIFIER";
        if (filter === "temp_sensor") return component.sensorType == "TEMPERATURE_SENSOR";
        if (filter === "humidity_sensor") return component.sensorType == "HUMIDITY_SENSOR";
        if (filter === "co2_sensor") return component.sensorType == "CO2_SENSOR";
    }).sort((a, b) => {
        if (sort === 'asc') {
            return a.sensorId - b.sensorId;
        } else {
            return b.sensorId - a.sensorId;
        }
    });

    $: paginatedFarms = paginate({ items: filteredFarms, pageSize, currentPage });
    $: theme = localStorage.getItem("theme") === 'sf_light';

    const myHeaders = new Headers();
    myHeaders.append("Origin", "");
    myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);

    fetch(
            `${PUBLIC_URL_PREFIX}/api/admin/farm/${$page.params.farm_id}`,
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
            sensors = response.data;
        };
    }

    fetch(
            `${PUBLIC_URL_PREFIX}/api/admin/list/ESPs`,
          {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
          })
        .then(async response => esp_handler(await response.json()))
        .catch(error => console.log('error', error));

    function esp_handler(response) {
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

    function createLight() {
      const myHeaders = new Headers();
      myHeaders.append("Origin", "");
      myHeaders.append("Authorization", `Bearer ${localStorage.getItem('token')}`);
      myHeaders.append('Content-Type', 'application/json');

      const input_data = {
          automation: false
      }

      fetch(
              `${PUBLIC_URL_PREFIX}/api/farm/${$page.params.farm_id}/light/create`,
            {
              method: 'POST',
              headers: myHeaders,
              body: JSON.stringify(input_data),
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
    }

    function createAC() {
      fetch(
              `${PUBLIC_URL_PREFIX}/api/admin/create/ac/${$page.params.farm_id}`,
            {
              method: 'POST',
              headers: myHeaders,
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
    }

    function create_handler(response) {
        if (!response.successful) {
            alert(response.message)
        } else if (response.successful) {
            location.reload();
        };
    }

    function createWatering() {
      fetch(
              `api/admin/create/watering/${$page.params.farm_id}`,
            {
              method: 'POST',
              headers: myHeaders,
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
    }

    function createCO2Controller() {
      fetch(
              `${PUBLIC_URL_PREFIX}/api/admin/create/co2_controller/${$page.params.farm_id}`,
            {
              method: 'POST',
              headers: myHeaders,
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
    }

    function createDehumidifier() {
      fetch(
              `${PUBLIC_URL_PREFIX}/api/admin/create/dehumidifier/${$page.params.farm_id}`,
            {
              method: 'POST',
              headers: myHeaders,
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
    }

    function createTemperatureSensor() {
      fetch(
              `${PUBLIC_URL_PREFIX}/api/admin/create/temperature_sensor/${$page.params.farm_id}`,
            {
              method: 'POST',
              headers: myHeaders,
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
    }

    function createHumiditySensor() {
      fetch(
              `${PUBLIC_URL_PREFIX}/api/admin/create/humidity_sensor/${$page.params.farm_id}`,
            {
              method: 'POST',
              headers: myHeaders,
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
    }

    function createCO2Sensor() {
      fetch(
              `${PUBLIC_URL_PREFIX}/api/admin/create/co2_sensor/${$page.params.farm_id}`,
            {
              method: 'POST',
              headers: myHeaders,
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
    }

    function toggleSort() {
      sort = sort === 'asc' ? 'desc' : 'asc';
    }

    function handleESPChange(original, selected, sensorType, sensorId) {
        if (original === 'Unselected'){
            fetch(
              `${PUBLIC_URL_PREFIX}/api/admin/create/ESPMap/${selected}/${sensorType}/${sensorId}`,
            {
              method: 'POST',
              headers: myHeaders,
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
        } else {
             fetch(
              `${PUBLIC_URL_PREFIX}/api/admin/update/ESPMap/${selected}/${sensorType}/${sensorId}`,
            {
              method: 'PATCH',
              headers: myHeaders,
              redirect: 'follow'
            })
          .then(async response => create_handler(await response.json()))
          .catch(error => console.log('error', error));
        }

    }


</script>
<h1 class="text-1xl font-bold mb-4 mt-10 flex justify-center">Admin Portal</h1>
<div class="container mx-auto mt-12 items-center justify-center">
   <div class="tabs items-center justify-center">
    <a class="tab tab-bordered" href="/admin-portal/user-list">
      <Icon icon="material-symbols:person"/>Back to user List</a>
     <a class="tab tab-bordered" href="/admin-portal/farm-list">
      <Icon icon="mdi:farm-home"/>Back to farm list</a>
  </div>
  <div class="mt-5  text-right">

      {#if filter === "light"}
        <a class="btn btn-primary" on:click={createLight}>createAC
          <Icon icon="iconoir:light-bulb-on"/>
          Add Light
        </a>
      {:else if filter === "ac"}
      <a class="btn btn-primary" on:click={createAC}>
          <Icon icon="tabler:air-conditioning"/>
          Add AC
        </a>
    {:else if filter === "water"}
        <a class="btn btn-primary" on:click={createWatering}>
          <Icon icon="material-symbols:water-drop"/>
          Add Watering Controller
        </a>
      {:else if filter === "co2"}
        <a class="btn btn-primary" on:click={createCO2Controller}>
          <Icon icon="material-symbols:co2"/>
          Add CO2 Controller
        </a>
      {:else if filter === "dehumidifier"}
       <a class="btn btn-primary" on:click={createDehumidifier}>
          <Icon icon="mdi:air-humidifier"/>
          Add Dehumidifier
        </a>
      {:else if filter === "temp_sensor"}
      <a class="btn btn-primary" on:click={createTemperatureSensor}>
          <Icon icon="ph:thermometer-fill"/>
          Add Temperature sensor
        </a>
    {:else if filter === "humidity_sensor"}
        <a class="btn btn-primary" on:click={createHumiditySensor}>
          <Icon icon="mdi:thermometer-water"/>
          Add Humidity Sensor
        </a>
      {:else if filter === "co2_sensor"}
      <a class="btn btn-primary" on:click={createCO2Sensor}>
          <Icon icon="material-symbols:co2"/>
          Add CO2 Sensor
        </a>
     {/if}
  </div>
  <h1 class="text-3xl font-bold mb-4 mt-5 flex items-center" style="white-space: nowrap;">
    <Icon icon="mdi:farm-home"/>
    Component list of farm:
    <p class="bg-blue-900 rounded pl-2 pr-2 white ml-2 mr-3" style="white-space: nowrap;">{farm_name}</p>
    Farm id:
    <p class="bg-blue-900 rounded pl-2 pr-2 white ml-2" style="white-space: nowrap;">{$page.params.farm_id}</p>
  </h1>
   <div class="search-wrapper mb-4 flex items-center rounded-lg border border-gray-300 px-3 py-2">
  <Icon icon="bi:search" class="mr-2 text-gray-400"/>
  <input type="text" placeholder="Search Farms..." on:input={handleSearch} class="w-full bg-transparent focus:outline-none"/>
     <button class="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded ml-2 mr-2" style="white-space: nowrap;">
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
  {#if filter === "all"}
        <button class="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded" style="white-space: nowrap;">All</button>
      {:else if filter === "light"}
        <button class="bg-yellow-600 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">Light</button>
      {:else if filter === "ac"}
      <button class="bg-blue-600 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">AC</button>
    {:else if filter === "water"}
        <button class="bg-blue-400 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">Watering</button>
      {:else if filter === "co2"}
      <button class="bg-red-900 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">CO2 Controller</button>
    {:else if filter === "dehumidifier"}
        <button class="bg-teal-800 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">Dehumidifier</button>
      {:else if filter === "temp_sensor"}
      <button class="bg-pink-500 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">Temperature sensor</button>
    {:else if filter === "humidity_sensor"}
        <button class="bg-purple-600 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">Humidity sensor</button>
      {:else if filter === "co2_sensor"}
      <button class="bg-orange-500 text-white font-bold py-2 px-4 rounded" style="white-space: nowrap;">CO2 sensor</button>
     {/if}
</div>
  <div class="flex items-center mb-5 grow md:flex-row md:flex-wrap">
    <div class="flex items-center mb-5 grow md:flex-row md:flex-wrap">
    <p class="text-1xl font-bold mr-5">Actuators: </p>
    <button on:click={() => filter="all"} class="bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded mr-4" style="white-space: nowrap;">All</button>
    <button on:click={() => filter="light"} class="bg-yellow-600 text-white font-bold py-2 px-4 rounded mr-4" style="white-space: nowrap;">Light</button>
    <button on:click={() => filter="ac"} class="bg-blue-600 text-white font-bold py-2 px-4 rounded mr-4" style="white-space: nowrap;">AC</button>
    <button on:click={() => filter="water"} class="bg-blue-400 text-white font-bold py-2 px-4 rounded mr-4" style="white-space: nowrap;">Watering</button>
    <button on:click={() => filter="co2"} class="bg-red-900 text-white font-bold py-2 px-4 rounded mr-4" style="white-space: nowrap;">CO2 Controller</button>
    <button on:click={() => filter="dehumidifier"} class="bg-teal-800 text-white font-bold py-2 px-4 rounded mr-4" style="white-space: nowrap;">Dehumidifier</button>
  </div>

  <div class="flex items-center mb-5 grow md:flex-row md:flex-wrap">
    <p class="text-1xl font-bold mr-5">Sensors: </p>
    <button on:click={() => filter="temp_sensor"} class="bg-pink-500 text-white font-bold py-2 px-4 rounded mr-4" style="white-space: nowrap;">Temperature sensor</button>
  <button on:click={() => filter="humidity_sensor"} class="bg-purple-600 text-white font-bold py-2 px-4 rounded mr-4" style="white-space: nowrap;">Humidity sensor</button>
  <button on:click={() => filter="co2_sensor"} class="bg-orange-500 text-white font-bold py-2 px-4 rounded mr-4" style="white-space: nowrap;">CO2 sensor</button>
  </div>
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
        <th>Sensor type</th>
        <th>Sensor ID</th>
        <th>ESP ID</th>
        <th></th>
      </tr>
    </thead>
      <tbody>
        {#each paginatedFarms as sensor}
          <tr >
            {#if sensor.sensorType === "LIGHT"}
              <td><p class="bg-yellow-600 rounded pl-4 pr-5 white w-20">{sensor.sensorType}</p></td>
              {:else if sensor.sensorType === "AC"}
              <td><p class="bg-blue-600 rounded pl-7 pr-5 white w-20">{sensor.sensorType}</p></td>
            {:else if sensor.sensorType === "WATERING"}
              <td><p class="bg-blue-400 rounded pl-8 pr-5 white w-36">{sensor.sensorType}</p></td>
              {:else if sensor.sensorType === "CO2_CONTROLLER"}
              <td><p class="bg-red-900 rounded pl-6 pr-5 white w-48">CO2 CONTROLLER</p></td>
            {:else if sensor.sensorType === "DEHUMIDIFIER"}
              <td><p class="bg-teal-800 rounded pl-6 pr-5 white w-40">{sensor.sensorType}</p></td>
              {:else if sensor.sensorType === "TEMPERATURE_SENSOR"}
              <td><p class="bg-pink-500 rounded pl-6 pr-5 white w-56">TEMPERATURE SENSOR</p></td>
            {:else if sensor.sensorType === "HUMIDITY_SENSOR"}
              <td><p class="bg-purple-600 rounded pl-6 pr-5 white w-48">HUMIDITY SENSOR</p></td>
              {:else if sensor.sensorType === "CO2_SENSOR"}
              <td><p class="bg-orange-500 rounded pl-5 pr-5 white w-36">CO2 SENSOR</p></td>
             {/if}
            <td>{sensor.sensorId}</td>
            <select class="select select-sm bg-blue-900 rounded-lg white pr-7 mr-1 max-height-3 w-13"
              on:change={(event) => handleESPChange(sensor.espId, event.target.value, sensor.sensorType, sensor.sensorId)}>
              <option disabled selected>{sensor.espId}</option>
              {#each ESPs as choice}
                  <option value={choice.id}>{choice.id}</option>
              {/each}
            </select>
          </tr>
          {/each}
      </tbody>
    </table>
  {#if !filteredFarms?.length}
    <div class="flex flex-col justify-center items-center p-10">
      <Icon icon="ri:tools-fill" class="w-52 h-52"/>
      <p class="mt-10 mb-10">No component found!</p>
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
