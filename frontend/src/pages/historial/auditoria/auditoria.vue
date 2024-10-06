<script lang="ts" setup>
import snackbar from "@/layouts/components/SnackBar.vue";
import DataTableCustom from "../../../layouts/components/DataTableCustomv2.vue";
import { PerfectScrollbar } from 'vue3-perfect-scrollbar';
import { requiredValidator } from '@validators';
import { computed, defineProps, onMounted, ref } from 'vue';
import { useRouter } from "vue-router";
import EstadoService from '@/services/servicio_estado/EstadoService';

import CultivoActivoService from "@/services/servicio_cultivo/CultivoActivoService";
import VariedadService from "@/services/servicio_variedad/VariedadService";
import AuditoriaService from "@/services/servicio_auditoria/AuditoriaService";

const props = defineProps([])
const router = useRouter();
let tabla = ref('');
let evento = ref('');
let sentencia = ref('');
let registro_id = ref('');
let usuario = ref("");
let fecha = ref("");
let hora = ref("");
let estado = ref(1);  // Estado por defecto 'Activo'
let dialog = ref(false);
let accion = ref(1);  // 1 = Crear, 2 = Editar
let id = ref(null);   // ID del centro al editar
let searchQuery = ref('')
let rowPerPage = ref(10)
let radioSearch = ref('date')
let isDrawerVisible = ref(false)
const refForm = ref(null);
let filters = ref([])
let isLoading = ref(false)
let isSnackbarVisible = ref(false)
let titleSnackbar = ref(null)
let stateSnackbar = ref(null)

let columns = ref([
    { key: "tabla", name: "tabla", order: true, search: true, class: 'text-left' },
    { key: "evento", name: "eventro", order: true, search: true, class: 'text-left' },
    { key: "sentencia", name: "sentencia", order: true, search: true, class: 'text-left' },
    { key: "registro_id", name: "id registro", order: true, search: true, class: 'text-left' },
    { key: "usuario", name: "usuario", order: true, search: true, class: 'text-left' },
    { key: "fecha", name: "fecha", order: true, search: true, class: 'text-left' },
    { key: "hora", name: "hora", order: true, search: true, class: 'text-left' },
]);

let data = ref([])

onMounted(() => {
    ListaDatos();
});


const ListaDatos = async () => {
    isLoading.value = true;
    let response;
    try {
        response = await AuditoriaService.getAuditorias();
        titleSnackbar.value = response.message_user;
        data.value = response.map(item => {
            return {
                ...item,
                estado: item.estado === 'Activo' ? 1 : (item.estado === 'Inactivo' ? 2 : 3)
            };
        });
    } catch (error) {
        titleSnackbar.value = "Error al cargar las empresas:", error
    } finally {
        isLoading.value = false;
    }
};


const onColSelected = (item: any) => {
    radioSearch.value = item
    console.log(item)
}
</script>


<template>
    <section>

        <snackbar :visible="isSnackbarVisible" :title="titleSnackbar" :close-visible="true" :state="stateSnackbar">
        </snackbar>

        <VRow>
            <VCol cols="12">
                <VCard>
                    <VCardTitle class="mb-3 mt-2">

                        LISTA DE VARIEDADES
                    </VCardTitle>

                    <VDivider />

                    <VCardText class="d-flex flex-wrap py-4 gap-4">

                        <div class="me-3" style="width: 80px;">
                            <VSelect v-model="rowPerPage" density="compact" variant="outlined"
                                :items="[10, 20, 30, 50]" />
                        </div>

                        <div class="me-3" style="width: 80px;">
                            <VBtn icon size="small" color="success" @click="ListaDatos">
                                <VIcon size="22" icon="tabler-analyze" />
                                <VTooltip activator="parent" location="end">
                                    RECARGAR DATOS
                                </VTooltip>
                            </VBtn>
                        </div>



                        <VSpacer />

                        <div class="app-user-search-filter d-flex align-center flex-wrap gap-4">

                            <div style="width: 30rem;">
                                <VTextField v-model="searchQuery" :placeholder="'Search by ' + radioSearch"
                                    density="compact" @input="searchQuery = searchQuery.toUpperCase()" />
                            </div>
                        </div>
                    </VCardText>

                    <VDivider />

                    <VRow>
                        <VCol cols="12">
                            <DataTableCustom :colums="columns" :data="data"
                                :on-col="onColSelected" :is-loading="isLoading" :search-query="searchQuery"
                                :row-per-page="rowPerPage" :filters="filters" :id-select="id">
                            </DataTableCustom>
                        </VCol>
                    </VRow>

                </VCard>
            </VCol>

        </VRow>
    </section>
</template>

<style lang="scss" scoped>
.cursor-pointer {
    cursor: pointer;
}

.text-columna-seleccionado {
    color: #000;
}

.table-schedule {
    border-width: 1px;
    border-style: solid;
    border-color: #eee;
    border-collapse: collapse;
}

.table-schedule td {
    border-width: 1px;
    border-color: #eee;
    border-block-end-style: solid;
    border-block-start-style: solid;
    color: #a7a7a7;
    font-family: monospace;
    font-size: 12px;
    font-weight: 600;
    padding-block: 4px;
    padding-inline: 7px;
    vertical-align: top;
}

.item_hour {
    border-radius: 3px;
    background: #aba3ff;
    block-size: 40px;
    inline-size: 251px;
}

.custom-dialog {
    z-index: 1000 !important;
    /* Ajusta este valor según sea necesario */
}

.date-time-picker {
    z-index: 2000 !important;
    /* Asegúrate de que este valor sea mayor que el z-index del VDialog */
}

.list-detail {
    display: flex;
    overflow: auto;
    flex-wrap: nowrap;
    justify-content: flex-start;
}

ul.list-detail .list-detail-column {
    //   background: aqua;
    margin-inline-end: 10px;
}

.col-guia {
    inline-size: 200px;
}

.col-provincia {
    inline-size: 320px;
}

.col-distrito {
    inline-size: 320px;
}

.col-variedad {
    inline-size: 350px;
}

.col-proveedor {
    inline-size: 430px;
}

.col-tipo-envase {
    inline-size: 218px;
}

.col-kilos {
    inline-size: 176px;
}

.col-porcentaje {
    inline-size: 176px;
}

.item-detail {
    display: flex;
    align-items: center;
    justify-content: center;
    block-size: 44px;
    margin-block-end: 10px;
}

.title {
    color: #a7a7a7;
    font-size: 12px;
    font-weight: 600;
    text-align: center;
}

.mask-style {
    padding: 6px;
    border: 1px solid #bdbdbd;
    border-radius: 8px;
    color: #8b8b8b;
}

.mask-style:focus {
    padding: 6px;
    border: 2px solid #671ad4 !important;
    border-radius: 8px;
}
</style>


<route lang="yaml">
meta:
    action: manage
    subject: historial_auditoria_auditoria
</route>
