<script lang="ts" setup>

import snackbar from "@/layouts/components/SnackBar.vue";
import DataTableCustom from "../../../layouts/components/DataTableCustomv2.vue";
import { PerfectScrollbar } from 'vue3-perfect-scrollbar';

import { requiredValidator } from '@validators';
import { computed, defineProps, onMounted, ref } from 'vue';
import { useRouter } from "vue-router";
import MonedaService from '@/services/servicio_moneda/MonedaService'

import EstadoService from '@/services/servicio_estado/EstadoService'


const props = defineProps([])

const router = useRouter();
let moneda = ref('');
let abreviatura = ref('');


let estado = ref(1);  // Estado por defecto 'Activo'
let dialog = ref(false);
let accion = ref(1);  // 1 = Crear, 2 = Editar
let id = ref(null);   // ID para editar

let searchQuery = ref('')
let rowPerPage = ref(10)

let radioSearch = ref('date')
let isDrawerVisible = ref(false)
const refForm = ref(null);

let filters = ref([])

let isLoading = ref(false)
let isSnackbarVisible = ref(false)
let titleSnackbar = ref('')
let stateSnackbar = ref('success')


let columns = ref([


    { key: "nombre", name: "nombre", order: true, search: true, class: 'text-left' },
    { key: "abreviatura", name: "abreviatura", order: true, search: true, class: 'text-left' },
    {
        key: 'estado', name: 'estado', order: true, search: false, class: 'text-center', alias: true, itemsAlias:
            [
                {
                    alias: 'ACTIVO',
                    color: 'success',
                    key: 1, // Clave numérica que debe coincidir con el valor de `int_state`
                },
                {
                    alias: 'INACTIVO',
                    color: 'secondary',
                    key: 2,
                },
            ]
    },
    { key: "fecha_creacion", name: "fecha creación", order: true, search: true, class: 'text-left' },
    { key: "fecha_modificacion", name: "fecha modificación", order: true, search: true, class: 'text-left' },

])




let data = ref([])
let selectedItems = ref([])



onMounted(() => {
    ListaDatos();
    CargarEstados();
});


let opcionesEstado = ref([])

const CargarEstados = async () => {
    try {
        const response = await EstadoService.getEstados();
        opcionesEstado.value = response
        .map(estado => ({
            value: estado.id,
            title: estado.nombre
        }));
    } catch (error) {
        console.error("Error fetching states:", error);
    }
};

const ListaDatos = async () => {
    isLoading.value = true;
    try {
        const response = await MonedaService.getMonedas();
        data.value = response.map(item => {
            return {
                ...item,
                estado: item.estado === 'Activo' ? 1 : (item.estado === 'Inactivo' ? 2 : 3)
            };
        });
    } catch (error) {
        console.error("Error al listar las monedas:", error);
    } finally {
        isLoading.value = false;
    }
};

const onNew = () => {
    refForm.value = false;
    accion.value = 1;
    dialog.value = true;
};

const onEdit = (item: any) => {
    id.value = item.id;
    moneda.value = item.nombre;
    abreviatura.value = item.abreviatura;
    estado.value = item.estado;
    accion.value = 2;
    dialog.value = true;
};

const nombreRules = computed(() => {
    return [
        v => !!v || 'Nombre es requerido',
        v => (v && v.length >= 2) || 'Mínimo 2 caracteres',
        v => (v && v.length <= 18) || 'Máximo 18 caracteres',
    ];
});

const abreviaturaRules = computed(() => {
    return [
        v => !!v || 'Abreviatura es requerida',
        v => (v && v.length >= 2) || 'Mínimo 2 caracteres',
        v => (v && v.length <= 18) || 'Máximo 18 caracteres',
    ];
});
const onSubmit = async () => {
    const nombreValidacion = nombreRules.value.every(rule => rule(moneda.value) === true);
    const abreviaturaValidacion = abreviaturaRules.value.every(rule => rule(abreviatura.value) === true);

    if (!nombreValidacion || !abreviaturaValidacion) {
        return; 
    }
    
    isLoading.value = true;
    try {
        const formData = {
            nombre: moneda.value,
            abreviatura: abreviatura.value,
            estado: estado.value,
        };
        let response : { message_user: any; };
        if (accion.value === 1) {
            response = await MonedaService.createMoneda(formData);
        } else {
            response = await MonedaService.updateMoneda(id.value, formData);
        }
        titleSnackbar.value = response.message_user || 'Operación exitosa'; // Mensaje amigable
        stateSnackbar.value = 'success';
        isSnackbarVisible.value = false;  // Reiniciar el estado del snackbar
        setTimeout(() => {                 // Asegurarse de que el snackbar vuelva a aparecer
            isSnackbarVisible.value = true;
        }, 0);
        ListaDatos(); // Recargar datos
        dialog.value = false;
    } catch (error) {
        titleSnackbar.value = error.response.data.message_user || 'Error inesperado';
        stateSnackbar.value = 'error';
        isSnackbarVisible.value = false;  // Reiniciar el estado del snackbar
        setTimeout(() => {                 // Asegurarse de que el snackbar vuelva a aparecer
            isSnackbarVisible.value = true;
        }, 0);
    } finally {
        isLoading.value = false;
    }
};

const onDelete = async (item: any) => {
    try {
        let response: { message_user: any; }
        response = await  MonedaService.deleteMoneda(item.id);
        titleSnackbar.value = response.message_user;
        stateSnackbar.value = 'success';
        isSnackbarVisible.value = false;  // Reiniciar el estado del snackbar
        setTimeout(() => {                 // Asegurarse de que el snackbar vuelva a aparecer
            isSnackbarVisible.value = true;
        }, 0);
        ListaDatos(); // Recargar datos
        dialog.value = false;
    } catch (error) {
        titleSnackbar.value = error.response.data.message_user;
        stateSnackbar.value = 'error';
        isSnackbarVisible.value = false;  // Reiniciar el estado del snackbar
        setTimeout(() => {                 // Asegurarse de que el snackbar vuelva a aparecer
            isSnackbarVisible.value = true;
        }, 0);
    }
}

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
                        LISTA DE MONEDAS
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



                            <VBtn prepend-icon="tabler-plus" @click="onNew()">
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
                            <DataTableCustom :colums="columns" :data="data" :on-edit="onEdit" :on-delete="onDelete"
                                :on-col="onColSelected" :is-loading="isLoading" :search-query="searchQuery"
                                :row-per-page="rowPerPage" :filters="filters" :id-select="id">

                            </DataTableCustom>
                        </VCol>
                    </VRow>

                </VCard>
            </VCol>

        </VRow>



        <VNavigationDrawer temporary :width="400" location="end" class="scrollable-content" :model-value="dialog"
            @update:model-value=" dialog = false">

            <div class="d-flex align-center pa-6 pb-1">
                <h6 class="text-h6">
                    {{ accion == 1 ? 'NUEVA MONEDA' : 'EDITAR MONEDA' }}
                </h6>

                <VSpacer />

                <VBtn variant="tonal" color="default" icon size="32" class="rounded" @click=" dialog = false">
                    <VIcon size="18" icon="tabler-x" />
                </VBTn>
            </div>

            <PerfectScrollbar :options="{ wheelPropagation: false }">
                <VCard flat>
                    <VCardText>

                        <VForm ref="refForm" @submit.prevent="onSubmit">
                            <VRow>
                                <VCol cols="12">
                                    <VTextField v-model="moneda" label="Moneda" :rules="nombreRules" type="text" />
                                </VCol>


                                <VCol cols="12">
                                    <VTextField v-model="abreviatura" label="Abreviatura" :rules="abreviaturaRules"
                                        type="text" />
                                </VCol>

                                <VCol cols="12" v-if="accion == 2">
                                    <VSelect v-model="estado" label="Estado" :rules="[requiredValidator]"
                                        :items="opcionesEstado"/>
                                        
                                </VCol>
                                <VCol cols="12">
                                    <VBtn type="submit" class="me-3">
                                        {{ accion === 1 ? 'Guardar' : 'Editar' }}
                                    </VBtn>
                                    <VBtn type="reset" variant="tonal" color="secondary" @click=" dialog = false">
                                        Cerrar
                                    </VBtn>
                                </VCol>
                            </VRow>
                        </VForm>

                    </VCardText>
                </VCard>
            </PerfectScrollbar>
        </VNavigationDrawer>


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
    subject: general_moneda_moneda
</route>
