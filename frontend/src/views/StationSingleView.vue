<template>
  <div class="page-body" v-if="station">
    <div class="container-xl">
      <div class="card mb-4">
        <div class="card-header">
          <h3 class="card-title">Stansiya ma'lumotlari</h3>
          <div class="card-actions">
            <!-- data-bs-toggle="modal" data-bs-target="" -->
            <a href="#" >
              Tahrirlash
              <IconPencil class="icon" stroke="2" />
            </a>
          </div>
        </div>
        <div class="card-body">
          <div class="datagrid">
            <div class="datagrid-item">
              <div class="datagrid-title">Stansiya nomi</div>
              <div class="datagrid-content">{{ station?.name ? station?.name : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Stansiya raqami</div>
              <div class="datagrid-content">{{ station?.number ? station?.number : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Shimoliy kenglik</div>
              <div class="datagrid-content">{{ station?.lat ? station?.lat : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Sharqiy uzunlik</div>
              <div class="datagrid-content">{{ station?.lon ? station?.lon : noInfoMes }}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="row row-cards">
        <div class="col-12 col-lg-6">
          <div class="card">
            <div class="card-body">
              <div class="d-flex">
                <h3 class="card-title">AQI darajasi</h3>
                <div class="ms-auto">
                  <div class="dropdown">
                    <a class="dropdown-toggle text-secondary" aria-haspopup="true" aria-expanded="false" aria-disabled="true">Ohirgi 10 kun</a>
                  </div>
                </div>
              </div>
              <AQIChartSingle :station="station" />
            </div>
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Stansiya xaritadagi ko'rinishi</h3>
            </div>
            <AQIMap :stations="[station]" :view-coordinates="[station.lat, station.lon]" :view-zoom="13" />
          </div>
        </div>
        <div class="col">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Parameterlar</h3>
            </div>
            <div class="table-responsive">
              <table class="table table-vcenter card-table table-bordered">
                <thead>
                  <tr>
                    <th>Sana</th>
                    <th v-for="pn in parameter_names" :key="pn.id">{{ pn.name }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(params, date) in dataByDate" :key="date">
                    <td>{{ date }}</td>
                    <td v-for="pn in parameter_names" :key="pn.id">
                      {{ params[pn.id] !== undefined ? params[pn.id] : '' }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
      </div>
    </div>
    
  </div>

  <teleport to="body">
    <ModalAlert :title="modalTitle" :description="modalDesc" ref="modalAlert" :type="modalType">
      <template #buttons>
        <div class="col">
          <button class="btn w-100" @click="modalOnCloseFunc" data-bs-dismiss="modal" data-bs-target="#modal-alert">
            Tushinarli
          </button>
        </div>
      </template>
    </ModalAlert>
  </teleport>
</template>

<script>
import { getStation } from '@/api/station';
import { ref } from 'vue';
import { format } from 'date-fns';
import { IconPencil } from '@tabler/icons-vue'
import ModalAlert from '@/components/ModalAlert.vue';
import AQIMap from '@/components/AQIMap.vue';
import AQIChartSingle from '@/components/AQIChartSingle.vue';


export default {
  data: () => ({
    station: null,
    modalTitle: '',
    modalDesc: '',
    modalType: '',
    noInfoMes: '-',
    modalOnCloseFunc: () => { },
    parameter_names: [],
    parameters: [],
  }),

  components: {
    IconPencil, ModalAlert, AQIMap, AQIChartSingle
  },

  setup() {
    const modalAlert = ref();
    return {
      modalAlert
    }
  },
  computed: {
    format() {
      return format;
    },
    dataByDate() {
      const grouped = {};
      for (const param of this.parameters) {
        const date = param.date.split("T")[0]; 
        if (!grouped[date]) {
          grouped[date] = {};
        }
        grouped[date][param.parameter_name] = param.value;
      }
      return grouped;
    }
  },

  methods:{
    setGwlOptionsSeries(parameters){
      const grouped = {};
      for (const param of parameters) {
        const date = param.date.split("T")[0]; 
        if (!grouped[date]) {
          grouped[date] = {};
        }
        grouped[date][param.parameter_name] = param.value;
      }
      return grouped;
    },
  },

  async mounted() {
    const stationNumber = this.$route?.params?.number;
    if (stationNumber) {
      try {
        this.station = await getStation(stationNumber);
        // this.setGwlOptionsSeries(this.parameters);
      } catch (error) {
        // if (error?.response?.status === 404) {
        //   this.$router.replace('/404');
        // } else {
          console.error('Error fetching station data:', error);
          this.modalTitle = "Ma'lumotlarni yuklashda xatolik yuzaga keldi";
          this.modalDesc = `Xato xabari: ${error?.message}`;
          this.modalType = 'danger';
          this.modalAlert.openModal();
        // }
      }
    } else {
      this.$router.replace('/404');
    }
  },
};
</script>
