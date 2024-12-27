<script setup>
import { onMounted, ref, watch, defineProps, computed } from 'vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

const mapContainer = ref(null);
let map;

const props = defineProps({
  stations: {
    type: Array,
    required: true,
    default: () => []
  },
  selectedHour: {
    type: Number,
    required: false,
    default: () => {
      const now = new Date();
      now.setMinutes(0);
      now.setSeconds(0);
      now.setMilliseconds(0);
      return now.getHours(); // Returns the current hour (0-23)
    }
  },
  viewCoordinates: {
    type: Array,
    required: false,
    default: () => [41.2773372, 69.2609832]
  },
  viewZoom: {
    type: Number,
    required: false,
    default: () => 11
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

const updateMarkers = () => {
  if (map) {
    // Clear existing layers
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Circle) {
        map.removeLayer(layer);
      }
    });

    // Add station markers and circles
    props.stations.forEach(station => {
      // getAqiColor(station?.parameter[0]?.aqi)
      // station?.parameter[0]?.aqi
      let markerHtml
      if (getCurTimeParameter(station?.parameters)){
        markerHtml = `
          <div class="station-marker" style="background-color: ${getAqiColor(getCurTimeParameter(station?.parameters).aqi)}">
            <span>${getCurTimeParameter(station?.parameters).aqi}</span>
          </div>
        `;

      }else{
        markerHtml = `
          <div class="station-marker" style="background-color: ${"transparent"}">
            <span>Ma'lumot mavjud emas</span>
          </div>
        `;
      }
      
      const icon = L.divIcon({
        html: markerHtml,
        className: 'custom-div-icon',
        iconSize: [30, 30],
      });

      // Add circle with opacity
      if (getCurTimeParameter(station?.parameters)){
        L.circle([station.lat, station.lon], {
          color: getAqiColor(getCurTimeParameter(station?.parameters).aqi),
          fillColor: getAqiColor(getCurTimeParameter(station?.parameters).aqi),
          fillOpacity: 0.2,
          radius: 2000
        }).addTo(map);
      } else {
        L.circle([station.lat, station.lon], {
          color: "black",
          fillColor: "black",
          fillOpacity: 0.2,
          radius: 2000
        }).addTo(map);
      }

      L.marker([station.lat, station.lon], { icon })
        .bindPopup(`
          <strong>${station?.name}</strong><br>
          AQI: ${getCurTimeParameter(station?.parameters)?.aqi}
        `)
        .addTo(map);
    });
  }
};

onMounted(() => {
  if (mapContainer.value) {
    // Initialize map
    map = L.map(mapContainer.value).setView(props.viewCoordinates, props.viewZoom);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Initial marker load
    updateMarkers();
  }
});

watch([() => props.stations, () => props.selectedHour], updateMarkers, { deep: true });
</script>

<template>
  <div class="map-container">
    <div ref="mapContainer" class="map"></div>
    <div class="time-tracker">
      {{ new Date().toLocaleTimeString() }}
    </div>
  </div>
</template>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 500px;
}

.map {
  width: 100%;
  height: 100%;
}

.time-tracker {
  position: absolute;
  top: 10px;
  right: 10px;
  background: white;
  padding: 5px 10px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  z-index: 1000;
}

:deep(.station-marker) {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

:deep(.custom-div-icon) {
  background: none;
  border: none;
}
</style>
