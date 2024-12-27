<script setup>
import { defineProps, watch, onMounted } from 'vue';


const props = defineProps({
  station: {
    type: Object,
    required: true,
    default: () => {}
  }
});

let options = {
      chart: {
        type: 'area'
      },
      xaxis: {
        type: 'datetime',
        labels: {
          show: false
        }
      }
    }
let series = [{
      name: '',
      data: []
    }]

const updateChart = () => {
  const seriesData = {
    name: 'AQI',  
    data: props.station.parameters.map(
      (param) => {return [new Date(param.datetime).getTime(), param.aqi]}
    ),
 }
  console.log(seriesData);
  
  series = seriesData;
  options = {
    ...options,
    chart: {
              id: 'area-datetime',
              type: 'area',
              height: 350,
              zoom: {
                autoScaleYaxis: true
              }
            },
            annotations: {
              yaxis: [{
                y: 30,
                borderColor: '#999',
                label: {
                  show: true,
                  text: 'Support',
                  style: {
                    color: "#fff",
                    background: '#00E396'
                  }
                }
              }],
              xaxis: [{
                x: new Date('14 Nov 2012').getTime(),
                borderColor: '#999',
                yAxisIndex: 0,
                label: {
                  show: true,
                  text: 'Rally',
                  style: {
                    color: "#fff",
                    background: '#775DD0'
                  }
                }
              }]
            },
            dataLabels: {
              enabled: false
            },
            markers: {
              size: 0,
              style: 'hollow',
            },
            xaxis: {
              type: 'datetime',
              min: new Date('01 Mar 2012').getTime(),
              tickAmount: 6,
            },
            tooltip: {
              x: {
                format: 'dd MMM yyyy'
              }
            },
            fill: {
              type: 'gradient',
              gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.7,
                opacityTo: 0.9,
                stops: [0, 100]
              }
            },
    title: {
      text: `AQI`,
      align: 'center',
      style: {
        color: '#444'
      }
    },
  };
};

onMounted(() => {
  updateChart();
});

watch([() => props.station], updateChart, { deep: true });

</script>

<template>
  <apexchart height="350" type="area" 
    :options="options" 
    :series="series"
  ></apexchart>
</template>