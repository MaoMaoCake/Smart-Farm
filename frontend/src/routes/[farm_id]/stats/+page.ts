export const load = (({ params }: any) => {
  if (params.farm_id == "farm1") {
    return {
      farm_id: params.farm_id,
      farm_data: {
        name: "farm 1",
        temp: 25,
        humidity: 2,
        light: true,
        ac: false,
        humidifier: true,
        co2_val: 900,
        co2: true
      }
    };
  }
  else{
    return {
      farm_id: params.farm_id,
      farm_data: {
        name: "placeholder",
        temp: 25,
        humidity: 2,
        light: true,
        ac: false,
        humidifier: true,
        co2_val: 900,
        co2: true
      }
    };
  }
})