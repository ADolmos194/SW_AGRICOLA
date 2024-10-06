<script lang="ts" setup>
import DataTableCustom from "@/layouts/components/DataTableCustom.vue";
import axios from "@axios";
import { onMounted, ref } from 'vue';
import { useRouter } from "vue-router";


const props = defineProps(['title'])

const router = useRouter();
let searchQuery = ref('')
let rowPerPage = ref(10)
let isLoading = ref(false)
let radioSearch = ref('Fecha')
let isDrawerVisible = ref(false)
let accion = ref(1)
let filters = ref([])
let columns = ref([
    { key: "date", name: "Fecha", order: true, search: true, class: 'text-center' },
    { key: "process", name: "Proceso", order: true, search: true, class: 'text-center' },
    { key: "time_shift", name: "Horario Turno", order: true, search: true, class: 'text-center' },
    { key: "hour", name: "Hora", order: true, search: true, class: 'text-center', chip: true },
    { key: "daily_wage", name: "Jornales", order: true, search: true, class: 'text-right', chip: true },
    { key: "kghh", name: "Kg HH", order: true, search: true, class: 'text-right', chip: true },
    {
        key: 'state_id', name: 'ESTADO', order: true, search: false, class: 'text-center', alias: true, itemsAlias:
            [
                {
                    alias: 'Activo',
                    color: 'success',
                    key: 1,
                },
                {
                    alias: 'Inactivo',
                    color: 'secondary',
                    key: 2,
                },
            ]
    },
])


let data = ref([])
let selectedItems = ref([])

//let process_id = 0

let ratio= {
    crop: "",
    id: 0,
    nameprocess: "",
    society: "",
    year_campaing: 0
}

let dailyWage = ref(0)

const detailRatioProduction = ref([
    {
        color: 'primary',
        icon: 'tabler-currency-dollar',
        title: 'Razon Social',
        value: 'Agrovision Corp',
        progress: '0',
        width: '3'
    },
    {
        color: 'info',
        icon: 'tabler-chart-pie-2',
        title: 'Año Camapaña',
        value: '',
        progress: '25',
        width: '2'
    },
    {
        color: 'success',
        icon: 'tabler-brand-paypal',
        title: 'Cultivo',
        value: '',
        progress: '65',
        width: '2'
    },
    {
        color: 'success',
        icon: 'tabler-brand-paypal',
        title: 'Proceso',
        value: '',
        progress: '65',
        width: '2'
    },
    {
        color: 'error',
        icon: 'tabler-brand-paypal',
        title: 'Jornales',
        value: '0',
        progress: '65',
        width: '2'
    },

])




onMounted(() => {
    
    ratio =  JSON.parse(localStorage.getItem('ratio') ?? JSON.stringify(ratio))
    detailRatioProduction.value[0].value= ratio.society
    detailRatioProduction.value[1].value= ratio.year_campaing.toString()
    detailRatioProduction.value[2].value= ratio.crop
    detailRatioProduction.value[3].value= ratio.nameprocess


    listData()
})

const listData = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/ratios-detail/${ratio.id}/1-2`,
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            data.value = response.data.data
         
            
            dailyWage.value = 0
            data.value.forEach((item) => {
                dailyWage.value = Math.max(dailyWage.value, item.daily_wage);
            })

            detailRatioProduction.value[4].value= dailyWage.value.toString()
            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}



const onColSelected = (col) => {
    console.log(col);
    radioSearch.value = col
}

const onInputed = (value) => {
    console.log(value);
    searchQuery.value = value
}

const onNew = () => {
}

const onEdit = (item) => {
}


const onDelete = (item) => {
    console.log(item);
}

const itemsSelected = (items) => {
    selectedItems.value = items
}

const downloadExcel = () => {

    const url = `/ingreso/download-excel/`;

    axios.get(url, {
        params: {
        },
        responseType: 'blob' // Especificar que esperamos una respuesta binaria (blob)
    })
    .then(response => {
        // Crear un objeto URL para el archivo binario
        const url = window.URL.createObjectURL(new Blob([response.data]));
        
        // Crear un enlace para descargar el archivo
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'ingresos.xlsx'); // Nombre del archivo
        
        // Simular un clic en el enlace para descargar el archivo
        document.body.appendChild(link);
        link.click();
        
        // Limpiar el objeto URL
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error al descargar el archivo:', error);
    });

}



</script>

<template>
    <section>
        <VRow>
            <VCol cols="12">
                <VCard>

                    <VCardTitle class="mb-3 mt-2">
                        <VBtn icon size="small" @click="router.go(-1)"
                            style="background-color: transparent !important; box-shadow: none;">
                            <VIcon size="22" icon="tabler-arrow-big-left" color="primary" />
                            <VTooltip activator="parent" location="end">
                                Volver a programacion
                            </VTooltip>
                        </VBtn>
                        DETALLE DE {{ props.title.toString().toUpperCase() ?? "RATIO" }} 
                    </VCardTitle>

                    <!--   <VDivider /> -->

                    <div class="border rounded mt-3 pa-4 ml-5 mr-5">
                        <VRow style="justify-content: center;">
                            <VCol v-for="report in detailRatioProduction" :key="report.title" cols="12" :sm="report.width">
                                <div class="d-flex align-center">
                                    <VAvatar rounded size="30" :color="report.color" variant="tonal" class="me-2">
                                        <VIcon :icon="report.icon" />
                                    </VAvatar>

                                    <h6 class="text-base font-weight-medium">
                                        {{ report.title }}
                                    </h6>
                                </div>
                                <h6 class="text-h6 my-3">
                                    {{ report.value.toUpperCase() }}
                                </h6>
                               <!--  <VProgressLinear :model-value="report.progress" :color="report.color" height="8" rounded
                                    rounded-bar /> -->
                            </VCol>
                        </VRow>
                    </div>

                    <br>
                    <br>

                    <VCardText class="d-flex flex-wrap py-4 gap-4">

                        <div class="me-3" style="width: 80px;">
                            <VSelect v-model="rowPerPage" density="compact" variant="outlined" :items="[10, 20, 30, 50]" />
                        </div>

                        <div class="me-3" style="width: 80px;">
                            <VBtn icon size="small" color="success" @click="listData">
                                <VIcon size="22" icon="tabler-analyze" />
                                <VTooltip activator="parent" location="end">
                                    Cargar Datos
                                </VTooltip>
                            </VBtn>
                        </div>

                        <VSpacer />

                        <div class="app-user-search-filter d-flex align-center flex-wrap gap-4">

                            <div style="width: 30rem;">
                                <VTextField v-model="searchQuery" :placeholder="'Buscar por ' + radioSearch"
                                    density="compact" @input="searchQuery = searchQuery.toUpperCase()" />
                            </div>

                            <!-- <div class="">
                            <VBtn color="success" prepend-icon="tabler-edit"
                                :to="{ name: 'packingscreen-ratioHeaderAcopio-ratioHeaderAcopioDetailUpdateAll' }"
                                >
                                Editar
                            </VBtn>
                            </div> -->

                            <VBtn prepend-icon="tabler-plus" 
                            :to="{ name: 'packingscreen-ratios-ratioDetailAddUpdate' }">
                                Nuevo
                            </VBtn>

                            <VBtn variant="tonal" color="secondary" prepend-icon="tabler-screen-share"
                                @click="downloadExcel()">
                                Exportar
                            </VBtn>
                        </div>
                    </VCardText>

                    <VDivider />

                    <VRow>
                        <VCol cols="12">
                            <DataTableCustom :data="data" :colums="columns" :on-col="onColSelected" :is-loading="isLoading"
                                :search-query="searchQuery" :row-per-page="rowPerPage" :filters="filters"
                                :on-selected="itemsSelected">
                            </DataTableCustom>
                        </VCol>
                    </VRow>

                </VCard>
            </VCol>
        </VRow>
    </section>
</template>

<style lang="scss">
.cursor-pointer {
  cursor: pointer;
}

.text-columna-seleccionado {
  color: #000;
}
</style>
