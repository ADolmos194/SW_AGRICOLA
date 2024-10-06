<script lang="ts" setup>

import { messagePopupConfirm } from '@/functionsGlobals.js';
import DataTableCustom from "@/layouts/components/DataTableCustom.vue";
import snackbar from "@/layouts/components/SnackBar.vue";

import axios from "@axios";
import { requiredValidator } from '@validators';
import { computed, defineProps, onMounted, ref } from 'vue';
import { useRouter } from "vue-router";
import { PerfectScrollbar } from "vue3-perfect-scrollbar";


const props = defineProps([])

const router = useRouter();
let searchQuery = ref('')
let rowPerPage = ref(10)
let isLoading = ref(false)
let radioSearch = ref('año campaña')
let isDrawerVisible = ref(false)
let accion = ref(1)
const refForm = ref(null);

let filters = ref([])
let columns = ref([    
    {key: "anio_campania", name: "campaña", order: true, search: true, class: 'text-center'},
    {key: "sociedad", name: "Empresa", order: true, search: true, class: 'text-right'},
    {key: "centro", name: "Centro", order: true, search: true, class: 'text-center'},
    {key: "planta", name: "Planta", order: true, search: true, class: 'text-center', chip: true},
    {key: "fecha", name: "Fecha", order: true, search: true, class: 'text-center', chip: true},
    {
        key: 'estado', name: 'ESTADO', order: true, search: false, class: 'text-center', alias: true, itemsAlias:
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

let listYear = []
let listSociety = []
let listCenter = ref([])
let listPlant = ref([])
let listCrop = []

let stateScheduleTime = ref(false)


let optionYear = ref([])

let optionSociety = ref([])
// let optionCenter = ref([])
// let optionPlant = ref([])
let optionCrop = ref([])
let optionState = ref([
    { value: 1, title: 'Activo' },
    { value: 2, title: 'Inactivo' },
])


let year_id = ref(null)

let society_id = ref(null)
let center_id = ref(null)
let plant_id = ref(null)
let crop_id = ref(null)
let dateEntry = ref(null)
let state_id = ref(null)
let id = ref(null)

let isSnackbarVisible= ref(null)
let titleSnackbar= ref(null)
let stateSnackbar= ref(null)


onMounted(() => {
    listData()
    getListYear()
    getListSociety()
    getListCenter()
    getListPlant()
    getListCrop()

})


let optionCenter = computed(() => {
    return listCenter.value.filter((item: any) => parseInt(item.sociedadpais) == parseInt(society_id.value ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.abreviatura} - ${item.nombre}`.toUpperCase(),
        };
    });
});

const optionPlant = computed(() => {
    return listPlant.value.filter((item: any) => parseInt(item.centro) == parseInt(center_id.value?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.abreviatura} - ${item.nombre}`.toUpperCase(),
        };
    });
});


const listData = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: `/ingreso/1-2`,
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            data.value = response.data.data
            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}



const getListYear = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: "/campania/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listYear = response.data.data

            optionYear.value = listYear.map((item: any) => {
                return {
                    value: item.id,
                    title: item.anio,
                };
            });

            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}


const getListSociety = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: "/sociedad/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listSociety = response.data.data

            optionSociety.value = listSociety.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.pais} - ${item.sociedad}`.toUpperCase(),
                };
            });
           
            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}

const getListCenter = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: `/centro/1`,
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listCenter.value = response.data.data

            /* optionCenter.value = listCenter.map((item: any) => {
                return {
                    value: item.id,
                    title: item.name,
                };
            }); */

            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}



const getListPlant = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: "/planta/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listPlant.value = response.data.data
        /* 
            optionPlant.value = listPlant.map((item: any) => {
                return {
                    value: item.id,
                    title: item.timeshift,
                };
            }); */          

            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}


const getListCrop = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: "/cultivo/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listCrop = response.data.data

            optionCrop.value = listCrop.map((item: any) => {
                return {
                    value: item.id,
                    title: item.nombre,
                };
            });

            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}





const onEdit = (item: any) => {

    
    accion.value = 2
    stateScheduleTime.value= false
    isDrawerVisible.value = true
    
    refForm.value.reset();

    id.value = item.id
    crop_id.value = item.cultivo_id
    year_id.value = item.campania_id
    society_id.value = item.socieda_paid_id
    center_id.value = item.centro_id
    plant_id.value = item.planta_id
    state_id.value = item.estado
    dateEntry.value= null
    dateEntry.value = item.fecha

}

const onNew = ()=>{
    accion.value = 1
    isDrawerVisible.value = true
    stateScheduleTime.value= false
    refForm.value.reset();

    id.value = null
    crop_id.value = null
    year_id.value = null
    plant_id.value = null
    center_id.value = null
    society_id.value = null
    dateEntry.value= null


}


const onSubmit = async () => {
    const isValid = await refForm.value.validate();
    if (!isValid.valid) return;

    isSnackbarVisible.value = false

    let data = {
        fecha: dateEntry.value,
        campania: year_id.value,
        cultivo: crop_id.value,
        planta: plant_id.value,
        estado: state_id.value
    }
    
    const config = {
        method: accion.value == 1 ?  "post": "put",
        url: accion.value == 1 ?  "/ingreso/create/": "/ingreso/update/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            isDrawerVisible.value = false
            listData()
            stateSnackbar.value = 'success'
            titleSnackbar.value = accion.value == 1 ? 'Registro creado con exito' : 'Registro actualizado con exito'
        }else{
            stateSnackbar.value = 'danger'
            titleSnackbar.value = accion.value == 1 ? 'Error al crear el registro' : 'Error al actualizar el registro'
        }
    } catch (error) {
        if (error.response.status == 409){
            stateSnackbar.value = 'danger'
            titleSnackbar.value = error.response.data.message_user

        }else{
            stateSnackbar.value = 'danger'
            titleSnackbar.value = accion.value == 1 ? 'Error al crear el registro' : 'Error al actualizar el registro'
        }
    }finally{
        isSnackbarVisible.value = true
        isDrawerVisible.value = false
        refForm.value.reset();
        dateEntry.value= false

    }
}

const onDelete = async (item: any) => {

    
    let values= await messagePopupConfirm({
        message: '¿Esta seguro de eliminar el registro?',
    })
    if (!values) return;
    

    isSnackbarVisible.value = false
    id.value = item.id

    let data = {
        estado: 0
    }

    const config = {
        method: "put",
        url: "/ingreso/update-state/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            isDrawerVisible.value = false
            listData()
           
            stateSnackbar.value = 'success'
            titleSnackbar.value = 'Registro eliminado con exito'
        }
    } catch (error) {
        stateSnackbar.value = 'danger'
        titleSnackbar.value = 'Error al eliminar el registro'
    }finally{
        isSnackbarVisible.value = true
    }
    
}

const itemsSelected = (items: any) => {
    selectedItems.value = items
    console.log(items);
    
}

const onColSelected = (item: any) => {
    radioSearch.value= item
    console.log(item)
}


const onInputed = (item: any) => {
    
    if (item.estado == 1){
        router.push({ name: 'packing-ingresos-ingresos'});
        localStorage.setItem('packing_plant', JSON.stringify(item))
    }else{
        console.log('no se puede editar');

        stateSnackbar.value = 'danger'
        titleSnackbar.value = 'Error, el registro no esta activo'
        isSnackbarVisible.value = true
        
    }

}


const downloadExcel = async ()=>{

    const config = {
        method: "post",
        maxBodyLength: Infinity,
        url: "/ingreso/download-excel/",
        headers: { 'Content-Type': 'multipart/form-data', },
        responseType: 'arraybuffer'
    };


    try {
        const response = await axios(config);
        
        if (response.status == 200) {
            const fileURL = window.URL.createObjectURL(new Blob([response.data]));

            const fileLink = document.createElement('a');
            fileLink.href = fileURL;
            fileLink.setAttribute('download', "ingresos.xlsx");
            document.body.appendChild(fileLink);
            fileLink.click();
       
        }
    } catch (error) {
        console.log("error ");
    }
}


</script>

<template>
    <section>
        
        <snackbar
            :visible="isSnackbarVisible"
            :title="titleSnackbar"
            :close-visible="true"
            :state="stateSnackbar"
        ></snackbar>

        <VRow>
            <VCol cols="12">
                <VCard title="PLANTAS DE MATERIA PRIMA">


                    <VDivider />

                    <VCardText class="d-flex flex-wrap py-4 gap-4">

                        <div class="me-3" style="width: 80px;">
                            <VSelect v-model="rowPerPage" density="compact" variant="outlined" :items="[10, 20, 30, 50]"
                                 />
                        </div>

                        <div class="me-3" style="width: 80px;">
                            <VBtn icon size="small" color="success" @click="listData">
                                <VIcon size="22" icon="tabler-analyze" />
                                <VTooltip activator="parent" location="end">
                                    Cargar Datos
                                </VTooltip>
                            </VBtn>
                        </div>


                        <!-- <div class="me-3">

                            <VBtn color="secondary"
                                :to="{ name: 'proyswarm-prospeccioncentropoblados-prospeccion_centro_poblado_updatemasivo' }">
                                Actualizacion Masiva de Empadronamiento
                            </VBtn>
                        </div>  -->

                        <VSpacer />

                        <div class="app-user-search-filter d-flex align-center flex-wrap gap-4">

                            <div style="width: 30rem;">
                                <VTextField v-model="searchQuery" 
                                    :placeholder=" 'Buscar por ' + radioSearch" 
                                    density="compact" 
                                    @input="searchQuery = searchQuery.toUpperCase()"
                                />
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
                            <DataTableCustom :on-edit="onEdit" :on-delete="onDelete"
                                :data="data" :colums="columns"
                                :on-col="onColSelected" :is-loading="isLoading" :search-query="searchQuery"
                                :row-per-page="rowPerPage" :filters="filters" :on-selected="itemsSelected" :on-input="onInputed" >
                            </DataTableCustom>
                        </VCol>
                    </VRow>

                </VCard>
            </VCol>
        </VRow>

        <VNavigationDrawer temporary :width="400" location="end" class="scrollable-content" :model-value="isDrawerVisible"
            @update:model-value=" isDrawerVisible = false">

            <div class="d-flex align-center pa-6 pb-1">
                <h6 class="text-h6">
                    {{ accion === 1 ? `Nuevo Ingreso` : `Editar Ingreso` }}
                </h6>

                <VSpacer />

                <VBtn variant="tonal" color="default" icon size="32" class="rounded" @click=" isDrawerVisible = false; dateEntry= false ">
                    <VIcon size="18" icon="tabler-x" />
                </VBTn>
            </div>

            <PerfectScrollbar :options="{ wheelPropagation: false }">
                <VCard flat>
                    <VCardText>

                        <VForm ref="refForm" @submit.prevent="onSubmit">
                            <VRow>
                                <VCol cols="12">
                                    <VSelect v-model="year_id" label="Seleccionar Campaña" :rules="[requiredValidator]" clearable
                                        :items="optionYear" />
                                </VCol>

                                <VCol cols="12">
                                    <VSelect v-model="society_id" label="Seleccionar Sociedad" :rules="[requiredValidator]" clearable
                                        :items="optionSociety"  />
                                </VCol>

                                <VCol cols="12">
                                    <VSelect v-model="center_id" label="Seleccionar Centro" :rules="[requiredValidator]" clearable
                                        :items="optionCenter" />
                                </VCol>

                                <VCol cols="12">
                                    <VSelect v-model="plant_id" label="Seleccionar Planta" :rules="[requiredValidator]" clearable
                                        :items="optionPlant" />
                                </VCol>

                                <VCol cols="12">
                                    <VSelect v-model="crop_id" label="Seleccionar Cultivo" clearable
                                       :rules="[requiredValidator]" :items="optionCrop" />
                                    <!-- <VAutocomplete v-model="crop_id" label="Seleccionar Cultivo"
                                       :rules="[requiredValidator]" :items="optionCrop" /> -->
                                </VCol>
                              
                                <VCol cols="12">
                                    <AppDateTimePicker
                                        v-model="dateEntry" clearable 
                                        label="Seleccionar Fecha"
                                        :rules="[requiredValidator]"
                                    />
                                </VCol>
                              

                                <VCol v-if="accion==2" cols="12">
                                    <VSelect v-model="state_id" label="Seleccionar Estado"
                                        :rules="[requiredValidator]" :items="optionState" />
                                </VCol>

                                <VCol cols="12">
                                    <VBtn type="submit" class="me-3">
                                        {{ accion === 1 ? 'Guardar' : 'Editar' }}
                                    </VBtn>
                                    <VBtn type="reset" variant="tonal" color="secondary" @click=" isDrawerVisible = false; dateEntry= false">
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

</style>
    
