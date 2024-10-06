<script lang="ts" setup>

import { messagePopup, messagePopupConfirm } from '@/functionsGlobals.js';
import snackbar from "@/layouts/components/SnackBar.vue";
import moment from 'moment';
import DataTableCustom from "../../../layouts/components/DataTableCustomv2.vue";
import { PerfectScrollbar } from 'vue3-perfect-scrollbar';



import axios from "@axios";
import { requiredValidator } from '@validators';
import { computed, defineProps, onMounted, ref } from 'vue';
import { useRouter } from "vue-router";


const props = defineProps([])

const router = useRouter();
let searchQuery = ref('')
let rowPerPage = ref(10)
let isLoading = ref(false)
let radioSearch = ref('date')
let isDrawerVisible = ref(false)
let accion = ref(1)
const refForm = ref(null);

let filters = ref([])

let id = ref(null)


let dialog = ref(false)


let isSnackbarVisible = ref(null)
let titleSnackbar = ref(null)
let stateSnackbar = ref(null)


let columns = ref([


    { key: "name", name: "name", order: true, search: true, class: 'text-left' },
    { key: "description", name: "description", order: true, search: true, class: 'text-left' },
    {
        key: 'state', name: 'STATE', order: true, search: false, class: 'text-center', alias: true, itemsAlias:
            [
                {
                    alias: 'Active',
                    color: 'success',
                    key: 1,
                },
                {
                    alias: 'Inactive',
                    color: 'secondary',
                    key: 2,
                },
            ]
    },

])




let data = ref([])
let selectedItems = ref([])



let optionState = ref([
    { value: 1, title: 'Active' },
    { value: 2, title: 'Inactive' },
])


let travelLogDefault = {
    id: 0,
    name: "",
    description: "",
    state: 1
}

let travelLog = ref({
    id: 0,
    name: "",
    description: "",
    state: 1
})





onMounted(() => {


    listData()

    
  

})






const listData = async (idselect = 0) => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/travel-nationalities/1-2`,
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            data.value = response.data.data
            
            // id.value = idselect

            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}





const onEdit = async (item: any) =>  {


    accion.value = 2
    // isDrawerVisible.value = true

    dialog.value = true

    if (refForm.value != null)
        refForm.value.reset();

    id.value = item.id

    travelLog.value={...item}



}



const onNew = () => {
    accion.value = 1

    dialog.value = true

    // isDrawerVisible.value = true

    if (refForm.value != null)
        refForm.value.reset();

    id.value = null

    travelLog.value = {...travelLogDefault}

   



}


const onSubmit = async () => {


  

    const isValid = await refForm.value.validate();
    if (!isValid.valid) return;


    isSnackbarVisible.value = false


    let data = {

        name: travelLog.value.name,
        description: travelLog.value.description,
        state: accion.value == 1 ?  1 : travelLog.value.state
    }

    console.log(data);
    
    // return;
    


    const config = {
        method: accion.value == 1?  "post": "put",
        url:  accion.value == 1? "/travel-nationality/create": "/travel-nationality/update/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            isDrawerVisible.value = false
            
            listData(response.data.data.id)
            stateSnackbar.value = 'success'
            titleSnackbar.value = accion.value == 1 ? 'Register created successfully' : 'Register updated successfully'
            dialog.value = false
            refForm.value.reset();

        } else {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = accion.value == 1 ? 'Error creating record' : 'Error updating record'
        }
    } catch (error) {
        if (error.response.status == 409) {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = error.response.data.message_user

        } else {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = accion.value == 1 ? 'Error creating record' : 'Error updating record'
        }
    } finally {
        isSnackbarVisible.value = true
        isDrawerVisible.value = false

    }
}

const onDelete = async (item: any) => {


    let values = await messagePopupConfirm({
        message: 'Are you sure you want to delete the record?', //en ingles
    })
    if (!values) return;


    isSnackbarVisible.value = false
    id.value = item.id

    let data = {
        state: 0
    }



    const config = {
        method: "delete",
        url: "/travel-nationality/delete/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            isDrawerVisible.value = false
            listData()

            stateSnackbar.value = 'success'
            titleSnackbar.value = 'Register deleted successfully'
        }
    } catch (error) {

        if (error.response.status == 409) {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = error.response.data.message_user

        } else {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = 'Error deleting the record'
        }

        // stateSnackbar.value = 'danger'
        // titleSnackbar.value = 'Error al eliminar el registro'
    } finally {
        isSnackbarVisible.value = true
    }

}


const onColSelected = (item: any) => {
    radioSearch.value = item
    console.log(item)
}


const onInputed = (item: any) => {

    router.push({ name: 'packing-ingresos-detalle_ingresos'});
    localStorage.setItem('ingreso', JSON.stringify(item))

}


const downloadExcel = async () => {

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
            fileLink.setAttribute('download', "travelmodes.xlsx");
            document.body.appendChild(fileLink);
            fileLink.click();

        }
    } catch (error) {
        console.log("error ");
    }
}



/* const minValidatorDateEntry = (value) => {
    return ((value ?? "").toString().length <= 0) || `Debe ingresar la fecha`
} */

</script>

<template>
    <section>

        <snackbar :visible="isSnackbarVisible" :title="titleSnackbar" :close-visible="true" :state="stateSnackbar">
        </snackbar>

        <VRow>
            <VCol cols="12">
                <VCard>
                    <VCardTitle class="mb-3 mt-2">
                        
                        LIST OF NATIONALITIES
                    </VCardTitle>

                    <VDivider />

                    <VCardText class="d-flex flex-wrap py-4 gap-4">

                        <div class="me-3" style="width: 80px;">
                            <VSelect v-model="rowPerPage" density="compact" variant="outlined"
                                :items="[10, 20, 30, 50]" />
                        </div>

                        <div class="me-3" style="width: 80px;">
                            <VBtn icon size="small" color="success" @click="listData">
                                <VIcon size="22" icon="tabler-analyze" />
                                <VTooltip activator="parent" location="end">
                                    Load Data
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
                                NEW
                            </VBtn>

                            <VBtn variant="tonal" color="secondary" prepend-icon="tabler-screen-share"
                                @click="downloadExcel()">
                                Export
                            </VBtn>
                        </div>
                    </VCardText>

                    <VDivider />

                    <VRow>
                        <VCol cols="12">
                            <DataTableCustom 
                                :colums="columns"
                                :data="data"

                                :on-edit="onEdit" 
                                :on-delete="onDelete" 
                                
                                :on-col="onColSelected" 
                                :is-loading="isLoading" 
                                :search-query="searchQuery"
                                
                                :row-per-page="rowPerPage" 
                                :filters="filters" 
                                
                                :id-select="id"

                                >
                                
                            </DataTableCustom>
                        </VCol>
                    </VRow>

                </VCard>
            </VCol>

        </VRow>



        <VNavigationDrawer temporary :width="400" location="end" class="scrollable-content"
            :model-value="dialog" @update:model-value=" dialog = false">

            <div class="d-flex align-center pa-6 pb-1">
                <h6 class="text-h6">
                    {{ accion == 1 ? 'NEW NATIONALITY' : 'EDIT NATIONALITY'  }}
                </h6>

                <VSpacer />

                <VBtn variant="tonal" color="default" icon size="32" class="rounded"
                    @click=" dialog = false">
                    <VIcon size="18" icon="tabler-x" />
                </VBTn>
            </div>

            <PerfectScrollbar :options="{ wheelPropagation: false }">
                <VCard flat>
                    <VCardText>

                        <VForm ref="refForm"  @submit.prevent="onSubmit">
                            <VRow>
                                <VCol cols="12">
                                    <VTextField v-model="travelLog.name" label="Name" :rules="[requiredValidator]" type="text" />
                                </VCol>


                                <VCol cols="12">
                                    <VTextarea v-model="travelLog.description"   label="description*"  rows="2"  />
                                </VCol>

                                <VCol cols="12" v-if="accion ==2">
                                    <VSelect v-model="travelLog.state" label="State" :rules="[requiredValidator]" 
                                            :items="optionState"   />
                                </VCol>
                             
                                
                              
                                
                                <VCol cols="12">
                                    <VBtn type="submit" class="me-3">
                                        {{ accion === 1 ? 'Guardar' : 'Editar' }}
                                    </VBtn>
                                    <VBtn type="reset" variant="tonal" color="secondary"
                                        @click=" dialog = false">
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
  z-index: 1000 !important; /* Ajusta este valor según sea necesario */
}

.date-time-picker {
  z-index: 2000 !important; /* Asegúrate de que este valor sea mayor que el z-index del VDialog */
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
    subject: travel_travel_modes
</route>

    