<script setup>
import { defineProps, computed, watch, onMounted } from 'vue';


const props = defineProps({
  stations: {
    type: Array,
    required: true,
    default: () => []
  },
  selectedHour: {
    type: Number,
    required: true,
    default: () => {
      const now = new Date();
      now.setMinutes(0);
      now.setSeconds(0);
      now.setMilliseconds(0);
      return now.getHours(); // Returns the current hour (0-23)
    }
  },
});

let options = {
      chart: {
        type: 'bar'
      },
      xaxis: {
        categories: [],
        labels: {
          show: false
        }
      }
    }
let series = [{
      name: '',
      data: []
    }]

const utcRoundedTime = computed(() => {
      const now = new Date();
      return new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate(),
        props.selectedHour, // Keep hours
        0,                 // Set minutes to 0
        0,                 // Set seconds to 0
        0                  // Set milliseconds to 0
      );
    })

function getCurTimeParameter(parameters) {
  // Вычисляем текущее округленное время
  const curTime = utcRoundedTime.value; // Если utcRoundedTime - это computed, нужно использовать .value

  // Ищем параметр с совпадающим временем
  const curTimeParameter = parameters.find((param) => {
    const paramTime = new Date(param.datetime);
    return paramTime.getTime() === curTime.getTime();
  });

  return curTimeParameter;
}

const updateChart = () => {
  const seriesData = props.stations.map((station) => {
    const curTimeParameter = getCurTimeParameter(station.parameters);
    const pm25 = curTimeParameter ? `${curTimeParameter.pm25} mkg/m³` : null;
    return {
      name: station.name,
      data: [pm25],
    };
  });
  if (seriesData.length === 0) {
    seriesData.push({
      name: '',
      data: [0],
    });
  }

  series = seriesData;
  options = {
    ...options,
    title: {
              text: `PM2.5 ${utcRoundedTime.value.toLocaleString('ru-RU', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false,
              })} (mkg/m³)`,
              align: 'center',
              style: {
                color: '#444'
              }
            },
    xaxis: {
      ...options.xaxis,
      categories: [utcRoundedTime.value.toLocaleString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      })],
    },
  };
};

onMounted(() => {
  updateChart();
});

watch([() => props.stations, () => props.selectedHour], updateChart, { deep: true });

</script>

<template>
  <apexchart height="350" type="bar" 
    :options="options" 
    :series="series"
  ></apexchart>
</template>