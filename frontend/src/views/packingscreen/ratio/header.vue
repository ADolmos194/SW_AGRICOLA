<script lang="ts" setup>

import { messagePopupConfirm } from '@/functionsGlobals.js';
import DataTableCustom from "@/layouts/components/DataTableCustom.vue";
import snackbar from "@/layouts/components/SnackBar.vue";

import axios from "@axios";
import { requiredValidator } from '@validators';
import { defineProps, onMounted, ref } from 'vue';
import { useRouter } from "vue-router";
import { PerfectScrollbar } from "vue3-perfect-scrollbar";


const props = defineProps(['title', 'stateprocess'])

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
    {key: "society", name: "Sociedad", order: true, search: true, class: 'text-center'},
    {key: "year_campaing", name: "año campaña", order: true, search: true, class: 'text-right'},
    {key: "crop", name: "Cultivo", order: true, search: true, class: 'text-center'},
    {key: "nameprocess", name: "Proceso", order: true, search: true, class: 'text-center', chip: true},
    {key: "timeshift", name: "Turno Horario", order: true, search: true, class: 'text-center', chip: true},
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

let listProcess = []
let listCrop = []
let listSociety = []
let listYear = []
let listScheduleTime = []
let listScheduleTimeDetail = []
let listScheduleTimeDetailSelected = ref([])

let stateScheduleTime = ref(false)


let optionProcess = ref([])
let optionCrop = ref([])
let optionSociety = ref([])
let optionYear = ref([])
let optionScheduleTime = ref([])
let optionState = ref([
    { value: 1, title: 'Activo' },
    { value: 2, title: 'Inactivo' },
])


let crop_id = ref(null)
let process_id = ref(null)
let society_id = ref(null)
let year_id = ref(null)
let timeshift_id = ref(null)
let state_id = ref(null)
let id = ref(null)

let isSnackbarVisible= ref(null)
let titleSnackbar= ref(null)
let stateSnackbar= ref(null)


onMounted(() => {
    listData()
    getListCrop()
    getListprocess()
    getListSociety()
    getListYear()
    getListScheduleTime()
    getListScheduleTimeDetail()

})


const listData = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: `/ratios/${props.stateprocess ?? 1}/1-2`,
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

const getListprocess = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: `/process/${props.stateprocess ?? 1}`,
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listProcess = response.data.data

            optionProcess.value = listProcess.map((item: any) => {
                return {
                    value: item.id,
                    title: item.name,
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

const getListCrop = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: "/crop/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listCrop = response.data.data

            optionCrop.value = listCrop.map((item: any) => {
                return {
                    value: item.id,
                    title: item.name,
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
        url: "/society/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listSociety = response.data.data

            optionSociety.value = listSociety.map((item: any) => {
                return {
                    value: item.id,
                    title: item.name,
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

const getListYear = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: "/year-campaing/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listYear = response.data.data

            optionYear.value = listYear.map((item: any) => {
                return {
                    value: item.year_campaign,
                    title: item.year_campaign,
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

const getListScheduleTime = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: "/schedule/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listScheduleTime = response.data.data

            optionScheduleTime.value = listScheduleTime.map((item: any) => {
                return {
                    value: item.id,
                    title: item.timeshift,
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

const getListScheduleTimeDetail = async () => {
    
    isLoading.value = true

    const config = {
        method: "get",
        url: "/schedule-detail/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listScheduleTimeDetail = response.data.data

            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}

const getListScheduleTimeDetailSelected = async () => {
    
    listScheduleTimeDetailSelected.value= []
    stateScheduleTime.value= false;

    for (const element of listScheduleTimeDetail) {
        if (parseInt(timeshift_id.value) == parseInt(element.schedule_id)) {
            listScheduleTimeDetailSelected.value.push(element)
        }
    }

    stateScheduleTime.value= true;

}



const onEdit = (item: any) => {
    console.log(item)

    accion.value = 2
    stateScheduleTime.value= false
    isDrawerVisible.value = true

    id.value = item.id
    society_id.value = item.society_id
    crop_id.value = item.crop_id
    process_id.value = item.process_id
    year_id.value = item.year_campaing
    state_id.value = item.state_id
    timeshift_id.value = item.schedule_id
    getListScheduleTimeDetailSelected()

}

const onNew = ()=>{
    accion.value = 1
    isDrawerVisible.value = true
    stateScheduleTime.value= false
    refForm.value.reset();

    id.value = null
    society_id.value = null
    crop_id.value = null
    process_id.value = null
    year_id.value = null


}


const onSubmit = async () => {
    const isValid = await refForm.value.validate();
    if (!isValid) return;

    isSnackbarVisible.value = false

    let data = {
        society_id: society_id.value,
        crop_id: crop_id.value,
        process: process_id.value,
        year_campaing: year_id.value,
        schedule: timeshift_id.value,
        state: state_id.value,
    }

    const config = {
        method: accion.value == 1 ?  "post": "put",
        url: accion.value == 1 ?  "/ratios/create/": "/ratios/update/" + id.value.toString(),
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
        stateSnackbar.value = 'danger'
        titleSnackbar.value = accion.value == 1 ? 'Error al crear el registro' : 'Error al actualizar el registro'
    }finally{
        isSnackbarVisible.value = true
        isDrawerVisible.value = false
        refForm.value.reset();

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
        state : 3
    }

    const config = {
        method: "delete",
        url: "/ratios/delete/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axiospantallas(config);
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
    
    console.log(item)
}

const itemsSelected = (items: any) => {
    selectedItems.value = items
}

const onColSelected = (item: any) => {
    radioSearch.value= item
    console.log(item)
}


const onInputed = (item: any) => {
    
    if (item.state_id == 1){
        router.push({ name: 'packingscreen-ratios-ratiosDetail'});
        localStorage.setItem('ratio', JSON.stringify(item))
    }else{
        console.log('no se puede editar');
        
    }

}


const downloadExcel = ()=>{

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
                <VCard :title="'PROGRAMACION DE ' + props.title.toString().toUpperCase() ?? 'RATIOS' ">


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
                    {{ accion === 1 ? `Nuevo ${props.title}` : `Editar ${props.title}` }}
                </h6>

                <VSpacer />

                <VBtn variant="tonal" color="default" icon size="32" class="rounded" @click=" isDrawerVisible = false">
                    <VIcon size="18" icon="tabler-x" />
                </VBTn>
            </div>

            <PerfectScrollbar :options="{ wheelPropagation: false }">
                <VCard flat>
                    <VCardText>

                        <VForm ref="refForm" @submit.prevent="onSubmit">
                            <VRow>

                                <VCol cols="12">
                                    <VSelect v-model="society_id" label="Seleccionar Sociedad" :rules="[requiredValidator]"
                                        :items="optionSociety" />
                                </VCol>

                                <VCol cols="12">
                                    <VSelect v-model="year_id" label="Seleccionar Campaña" :rules="[requiredValidator]"
                                        :items="optionYear" />
                                </VCol>

                                <VCol cols="12">
                                    <VSelect v-model="process_id" label="Seleccionar Proceso" :rules="[requiredValidator]"
                                        :items="optionProcess" />
                                </VCol>
                                <VCol cols="12">
                                    <VAutocomplete v-model="crop_id" label="Seleccionar Cultivo"
                                       :rules="[requiredValidator]" :items="optionCrop" />
                                </VCol>
                              
                                <VCol cols="12">
                                    <VAutocomplete v-model="timeshift_id" label="Seleccionar Turno horario"
                                       :rules="[requiredValidator]" :items="optionScheduleTime" @update:model-value="getListScheduleTimeDetailSelected"  />
                                </VCol>
                                
                                <VCol cols="12">
                                    <div v-if="stateScheduleTime" style=" overflow: auto;height: 290px;">
                                        <table class="table-schedule">
                                             <tr v-for="item in listScheduleTimeDetailSelected" :key="item.id">
                                                  <td>
                                                      {{ item.hour }}
                                                  </td>
                                                  <td>
                                                     <div class="item_hour">
     
                                                     </div>
                                                  </td>
                                             </tr>
                                        </table>

                                    </div>
                                </VCol>



                                <VCol v-if="accion==2" cols="12">
                                    <VSelect v-model="state_id" label="Seleccionar Estado"
                                        :rules="[requiredValidator]" :items="optionState" />
                                </VCol>

                                <VCol cols="12">
                                    <VBtn type="submit" class="me-3">
                                        {{ accion === 1 ? 'Guardar' : 'Editar' }}
                                    </VBtn>
                                    <VBtn type="reset" variant="tonal" color="secondary" @click=" isDrawerVisible = false">
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
    
