<script lang="ts">
  import type { PageData } from './$types';
  import "@carbon/styles/css/styles.css";
  import "@carbon/charts/styles.css";
  import { LineChart } from "@carbon/charts-svelte";
  import StatPreview from "$lib/StatPreview.svelte";
  import StatPreviewLarge from "$lib/StatPreviewLarge.svelte";

  export let data: PageData;
  let chart_data = [
      {
          "group": "Dataset 1",
          "date": "2018-12-31T17:00:00.000Z",
          "value": -10000
      },
      {
          "group": "Dataset 1",
          "date": "2018-12-31T22:00:00.000Z",
          "value": -12000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-01T03:00:00.000Z",
          "value": -14000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-01T17:00:00.000Z",
          "value": -25000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-01T19:00:00.000Z",
          "value": -26000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-02T17:00:00.000Z",
          "value": -10000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-02T22:00:00.000Z",
          "value": 10000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-03T03:00:00.000Z",
          "value": 12000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-04T17:00:00.000Z",
          "value": 45000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-06T17:00:00.000Z",
          "value": 49000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-07T08:00:00.000Z",
          "value": 45000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-08T17:00:00.000Z",
          "value": 50000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-08T22:00:00.000Z",
          "value": 52000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-09T08:00:00.000Z",
          "value": 55000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-09T17:00:00.000Z",
          "value": 50000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-11T17:00:00.000Z",
          "value": 65000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-12T17:00:00.000Z",
          "value": 80000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-14T03:00:00.000Z",
          "value": 85000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-15T00:00:00.000Z",
          "value": 90000
      },
      {
          "group": "Dataset 1",
          "date": "2019-01-15T11:00:00.000Z",
          "value": 70000
      },
      {
          "group": "Dataset 2",
          "date": "2018-12-31T17:00:00.000Z",
          "value": 20000
      },
      {
          "group": "Dataset 2",
          "date": "2018-12-31T20:00:00.000Z",
          "value": 22000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-01T09:00:00.000Z",
          "value": 24000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-01T17:00:00.000Z",
          "value": 35000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-02T00:00:00.000Z",
          "value": 36000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-02T17:00:00.000Z",
          "value": 20000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-02T23:00:00.000Z",
          "value": 20000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-03T11:00:00.000Z",
          "value": 22000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-04T17:00:00.000Z",
          "value": 62000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-05T17:00:00.000Z",
          "value": 52000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-06T17:00:00.000Z",
          "value": 52000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-07T08:00:00.000Z",
          "value": 52000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-08T17:00:00.000Z",
          "value": 60000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-08T22:00:00.000Z",
          "value": 62000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-09T03:00:00.000Z",
          "value": 62000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-11T17:00:00.000Z",
          "value": 65000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-13T17:00:00.000Z",
          "value": 40000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-14T22:00:00.000Z",
          "value": 45000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-15T03:00:00.000Z",
          "value": 35000
      },
      {
          "group": "Dataset 2",
          "date": "2019-01-15T11:00:00.000Z",
          "value": 30000
      }
  ]
</script>

<div class="flex w-full justify-center items-center flex-col md:flex-row">
    <div class="flex flex-col grow md:w-1/3 md:h-5/6 items-center justify-center">
        <div class="flex grow md:hidden">
            <StatPreview farm_name="{data.farm_data.name}" temp="{data.farm_data.temp}" humidity={data.farm_data.humidity}
                         light={data.farm_data.light} ac="{data.farm_data.ac}" humidifier={data.farm_data.humidifier}
                         co2={data.farm_data.co2} co2_val={data.farm_data.co2_val}>
            </StatPreview>
        </div>
        <div class="hidden md:flex">
            <StatPreviewLarge farm_name="{data.farm_data.name}" temp="{data.farm_data.temp}" humidity={data.farm_data.humidity}
                              light={data.farm_data.light} ac="{data.farm_data.ac}" humidifier={data.farm_data.humidifier}
                              co2={data.farm_data.co2} co2_val={data.farm_data.co2_val}>
            </StatPreviewLarge>
        </div>
        <div class="flex grow">
            <button class="btn btn-secondary white">Download Report</button>
        </div>
    </div>
    <div class="flex flex-col grow w-10/12">
        <div class="flex grow mt-2 mb-2">
            <LineChart
                    data={chart_data}
                    options={{
        	"title": "Humidity Levels",
        	"axes": {
        		"bottom": {
        			"mapsTo": "date",
        			"scaleType": "time"
        		},
        		"left": {
        			"mapsTo": "value",
        			"title": "Level of Humidity",
        			"scaleType": "linear"
        		}
        	},
        	"curve": "curveMonotoneX",
        	"height": "350px"
        }}
            />
        </div>
        <div class="flex grow mt-2 mb-2">
            <div class="flex grow">
                <LineChart
                        data={chart_data}
                        options={{
        	"title": "CO2 Levels",
        	"axes": {
        		"bottom": {
        			"mapsTo": "date",
        			"scaleType": "time"
        		},
        		"left": {
        			"mapsTo": "value",
        			"title": "Level of CO2",
        			"scaleType": "linear"
        		}
        	},
        	"curve": "curveMonotoneX",
        	"height": "350px"
        }}
                />
            </div>
        </div>
    </div>
</div>
<style>
    .white {
        color: white
    }
</style>