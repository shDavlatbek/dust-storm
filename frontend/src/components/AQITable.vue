<script setup>
import { defineProps, computed } from 'vue';


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
  }
});

const getAqiColor = (aqi) => {

  
  if (aqi <= 50) return '#00e400';
  if (aqi <= 100) return '#f7D543';
  if (aqi <= 150) return '#ff7e00';
  if (aqi <= 200) return '#E95F5E';
  if (aqi <= 300) return '#9168A1';
  
  return '#9D6878';
};

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

</script>

<template>
  <div class="table-responsive">
    <table class="table">
      <thead>
        <tr>
          <th>Nomi</th>
          <th class="text-end">AQI</th>
        </tr>
      </thead>
      <tbody class="table-tbody">
        <tr class="table-row" 
          v-for="(station, index) in props.stations" 
          :key="index" 
          :aria-disabled="getCurTimeParameter(station?.parameters)?.aqi ? false : true" 
          :class="{
            'pe-none': !getCurTimeParameter(station?.parameters)?.aqi,
            'bg-muted-lt': !getCurTimeParameter(station?.parameters)?.aqi
          }"
        >
          <td class="sort-name">{{ station?.name }}</td>
          <td class="sort-name text-end">
            <span class="badge text-white" 
              :style="{background: getAqiColor(getCurTimeParameter(station?.parameters)?.aqi)}"
              v-if="getCurTimeParameter(station?.parameters)?.aqi"
            >
              {{ getCurTimeParameter(station?.parameters)?.aqi }}
            </span>
            <span v-else>Ma'lumot mavjud emas</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>