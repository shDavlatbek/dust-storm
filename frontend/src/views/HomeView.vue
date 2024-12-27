<template>
  <div class="page-body">
    <div class="container-xl">
      <div class="row">
        <div class="col-12">
          <div class="card mb-4">
            <div class="card-header">
              <h3 class="card-title">Havo sifati interpolyatsiyasi</h3>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-12 col-lg-6">
                  <label class="form-label d-flex">Vaqt bo'yicha <span class="ms-auto">{{ formattedTime }}</span></label>
                  <input type="range" class="form-range mb-2" v-model.number="selectedHour" value="1" min="0" max="23" step="1">
                </div>
                <div class="col-12 col-lg-6 d-flex justify-content-end align-items-center">
                  <h1 class="m-0">{{ formattedDateTime }}</h1>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-12 col-lg-4">
          <div class="card mb-4">
            <div class="card-header">
              <h3 class="card-title">Stansiyalar bo‘yicha havo sifati</h3>
            </div>
            <AQITable :stations="stations" :selected-hour="selectedHour" />
          </div>
          
        </div>
        <div class="col-12 col-lg-8">
          <div class="card mb-4">
            <div class="card-body">
              <div class="badges-list">
                <span class="badge text-white ms-lg-auto" style="background-color: #00e400;">Yaxshi</span>
                <span class="badge text-white" style="background-color: #f7D543;">O‘rtacha</span>
                <span class="badge text-white" style="background-color: #ff7e00;">Nozik guruhlar uchun zararli</span>
                <span class="badge text-white" style="background-color: #E95F5E;">Zararli</span>
                <span class="badge text-white" style="background-color: #9168A1;">Juda zararli</span>
              </div>
            </div>
            <AQIMap :stations="stations" :selected-hour="selectedHour" />
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="card mb-4">
            <div class="card-body pt-5">
              <AQIChart :stations="stations" :selected-hour="selectedHour" />
            </div>
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="card mb-4">
            <div class="card-body pt-5">
              <PM25Chart :stations="stations" :selected-hour="selectedHour" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AQIMap from "@/components/AQIMap.vue";
import AQITable from "@/components/AQITable.vue";
import { getStationsParams } from "@/api/station";
import PM25Chart from "@/components/PM25Chart.vue";
import AQIChart from "@/components/AQIChart.vue";

export default {
  data() {
    return {
      dashboard: null,
      stations: [],
      selectedHour: 0,
    };
  },
  
  methods: {
    loadFrame(event){
      const iframe = event.target;
      try {
        const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
        iframe.style.height = iframeDocument.body.scrollHeight + 'px';
      } catch (error) {
        console.error("Unable to adjust iframe height:", error);
      }
    },
    utcRoundedTime() {
      const now = new Date();
      return new Date(Date.UTC(
        now.getUTCFullYear(),
        now.getUTCMonth(),
        now.getUTCDate(),
        now.getUTCHours(), // Keep hours
        0,                 // Set minutes to 0
        0,                 // Set seconds to 0
        0                  // Set milliseconds to 0
      ));
    },
    utcTime10daysAgo() {
      const now = new Date();
      return new Date(Date.UTC(
        now.getUTCFullYear(),
        now.getUTCMonth(),
        now.getUTCDate() - 10,
        now.getUTCHours(), // Keep hours
        0,                 // Set minutes to 0
        0,                 // Set seconds to 0
        0                  // Set milliseconds to 0
      ));
    },
  },
  computed: {
    formattedTime() {
      const hours = this.selectedHour.toString().padStart(2, '0')
      return `${hours}:00:00`
    },
    formattedDateTime() {
      const now = new Date()
      now.setHours(this.selectedHour, 0, 0, 0)
      return now.toLocaleString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      })
    },
    getRoundedHour() {
      const now = new Date();
      now.setMinutes(0);
      now.setSeconds(0);
      now.setMilliseconds(0);
      return now.getHours(); // Returns the current hour (0-23)
    }
  },
  async mounted() {
    this.stations = await getStationsParams(
      this.utcTime10daysAgo(),
      this.utcRoundedTime(),
      this.selectedHour = this.getRoundedHour
    );
  },

  components: { AQIMap, AQITable, PM25Chart, AQIChart }
};
</script>
