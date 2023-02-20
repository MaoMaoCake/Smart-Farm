<script lang="ts">
  import type { PageData } from './$types';
  import "@carbon/styles/css/styles.css";
  import "@carbon/charts/styles.css";
  import { LineChart } from "@carbon/charts-svelte";

  export let data: PageData;
</script>

<p>This is the stats for {data.farm_id}</p>

<LineChart
        data={[
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
]}
        options={{
	"title": "Line (dense time series)",
	"axes": {
		"bottom": {
			"title": "2019 Annual Sales Figures",
			"mapsTo": "date",
			"scaleType": "time"
		},
		"left": {
			"mapsTo": "value",
			"title": "Conversion rate",
			"scaleType": "linear"
		}
	},
	"curve": "curveMonotoneX",
	"height": "400px"
}}
/>
