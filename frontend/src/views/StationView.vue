<template>
  <HeaderText :title="title" :modal-id="modalId" :on-modal-open="loadForm" />

  <div class="page-body">
    <div class="container-xl">
      <div class="card">
        <div class="card-body py-3">
          <div class="d-flex">
            <div class="ms-auto row">
              <div class="col-auto">
                <label for="station-search" class="col-form-label p-0">Qidiruv</label>
              </div>
              <div class="col-auto">
                <input type="text" v-model="searchQuery" @input="updateSearch" id="station-search" class="form-control form-control-sm">
              </div>
            </div>
          </div>
        </div>
        <div id="table-station" class="table-responsive" >
          <table class="table table-bordered">
            <thead>
              <tr>
                <th><button class="table-sort" data-sort="sort-name">Nomi</button></th>
                <th><button class="table-sort" data-sort="sort-number">Raqam</button></th>
                <th><button class="table-sort" data-sort="sort-lat">Shimoliy kenglik</button></th>
                <th><button class="table-sort" data-sort="sort-lon">Sharqiy uzunlik</button></th>
              </tr>
            </thead>
            <tbody class="table-tbody">
              <tr class="table-row" v-for="(station, index) in stations" :key="index" @click="navigateToStationSingle(station.number)">
                <td class="sort-name">{{ station?.name }}</td>
                <td class="sort-number">{{ station?.number }}</td>
                <td class="sort-lat">{{ station?.lat }}</td>
                <td class="sort-lon">{{ station?.lon }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <teleport to="body">
    <ModalForm :modal-id="modalId" :modal-title="title" :modal-form-confirm="formHandler" ref="modalForm">
      <template #modal-body>
        <div class="modal-body">
          <div class="row">
            <div class="col-12 col-lg-6">
              <InputField :required="true" label="Nomi" v-model="addStationForm.name" />
            </div>
            <div class="col-12 col-lg-6">
              <InputField :required="true" label="Stansiya raqami" v-model="addStationForm.number" />
            </div>
            <div class="col-12 col-lg-6">
              <InputField :required="true" label="Shimoliy kenglik" v-model="addStationForm.lat" />
            </div>
            <div class="col-12 col-lg-6">
              <InputField :required="true" label="Sharqiy uzunlik" v-model="addStationForm.lon" />
            </div>
          </div>
        </div>
      </template>
    </ModalForm>
  </teleport>

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
import HeaderText from '@/components/HeaderTextComponent.vue';
import ModalAlert from '@/components/ModalAlert.vue';
import InputField from '@/components/InputField.vue';
import ModalForm from '@/components/ModalFormComponent.vue';
import List from 'list.js';
import { getStations, addStation } from '@/api/station';
import { ref } from 'vue';

export default {
  data() {
    return {
      title: "Meteorologik ma'lumotlar",
      modalId: "add-station",
      formLoaded: false,
      stations: {},
      modalOnCloseFunc: null,
      list: null,
      searchQuery: '',
      modalType: null,
      modalDesc: '',
      modalTitle: '',
      noInfoMessage: '------',
      addStationForm: {
        name: '',
        number: '',
        lat: '',
        lon: '',
      }
    }
  },
  computed: {
  },
  setup() {
    const modalAlert = ref();
    const modalForm = ref();
    return {
      modalAlert, modalForm
    }
  },
  methods: {
    async formHandler() {
      console.log("Form submitted");
      try {
        await addStation(JSON.stringify(this.addStationForm));
        this.modalForm.resetForm();
        this.modalForm.closeModal();
        this.modalAlert.openModal();
        this.modalTitle = "Ma'lumotlar muvaffaqiyatli qo'shildi";
        this.modalDesc = ""
        this.modalType = 'success';
        setTimeout(() => {
          this.$router.go();
        }, 2000);
        this.modalOnCloseFunc = () => {this.$router.go();};
      } catch (error) {
        console.log(error);
        this.modalForm.resetForm();
        this.modalForm.closeModal();
        this.modalAlert.openModal();
        this.modalTitle = "Ma'lumotlarni saqlashda xatolik yuzaga keldi";
        this.modalDesc = `Xato xabari: ${error?.message}<br>Url: ${error?.config?.url}`;
        this.modalType = 'danger'; 
        this.modalOnCloseFunc = () => {};
      }
    },
    initializeList() {
      const tableStation = document.getElementById('table-station');
      if (tableStation) {
        if (!this.list) {
          this.list = new List('table-station', {
            sortClass: 'table-sort',
            listClass: 'table-tbody',
            valueNames: ['sort-name', 'sort-number', 'sort-lat', 'sort-lon'],
          });
        } else {
          this.list.reIndex();
        }
      } else {
        console.error("Element #table-station not found!");
      }
    },
    updateSearch() {
      if (this.list) {
        this.list.search(this.searchQuery);
      }
    },
    navigateToStationSingle(number) {
      this.$router.push({ name: "StationSingle", params: { number } });
    },
  },
  async mounted() {
    try {
      this.stations = await getStations();
      await this.$nextTick();
      this.initializeList();
    } catch (error) {
      console.log(error);
      this.modalAlert.openModal();
      this.modalTitle = "Ma'lumotlarni yuklashda xatolik yuzaga keldi";
      if( error.message && error.config ){
        this.modalDesc = `Xato xabari: ${error.message}<br>Url: ${error?.config?.url}`;
      } else {
        this.modalDesc = `Xato xabari: ${error}`;
      }
      this.modalType = 'danger';
      this.modalOnCloseFunc = () => {};
    }
  },
  components: {
    HeaderText, ModalAlert, InputField, ModalForm
  },
}

</script>