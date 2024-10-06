<script lang="ts" setup>

import { messagePopup, messagePopupConfirm } from '@/functionsGlobals.js';
import snackbar from "@/layouts/components/SnackBar.vue";
import moment from 'moment';
import DataTableCustom from "../../../layouts/components/DataTableCustomv2.vue";


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

let isLoadingIngresoInspeccion = ref(false)
let id = ref(null)



// let isLoadingDetail = ref(false)
// let searchQueryDetail = ref('')
// let rowPerPageDetail = ref(10)
// let filtersDetail = ref([])
// let radioSearchDetail = ref('lote')

let dialog = ref(false)


let isSnackbarVisible = ref(null)
let titleSnackbar = ref(null)
let stateSnackbar = ref(null)


let columns = ref([


    { key: "date", name: "date", order: true, search: true, class: 'text-center' },
    { key: "year_calendar", name: "year calendar", order: true, search: true, class: 'text-center' },
    { key: "fiscal_year", name: "fiscal year", order: true, search: true, class: 'text-center' },
    { key: "name", name: "name", order: true, search: true, class: 'text-center' },
    { key: "lasta_name", name: "lasta name", order: true, search: true, class: 'text-center' },
    { key: "contact", name: "contact", order: true, search: true, class: 'text-center' },
    { key: "nationality", name: "nationality", order: true, search: true, class: 'text-center' },
    { key: "division", name: "division", order: true, search: true, class: 'text-center' },
    { key: "entity", name: "entity", order: true, search: true, class: 'text-center' },
    { key: "travel_modes", name: "travel modes", order: true, search: true, class: 'text-center' },
    { key: "airline", name: "airline", order: true, search: true, class: 'text-center' },
    {
        key: 'risk', name: 'RISK', order: true, search: false, class: 'text-center', alias: true, itemsAlias:
            [
                {
                    alias: 'SI',
                    color: 'success',
                    key: true,
                },
                {
                    alias: 'NO',
                    color: 'secondary',
                    key: false,
                },
            ]
    },
    { key: "travel_start_date", name: "travel start date", order: true, search: true, class: 'text-center' },
    { key: "travel_return_date", name: "travel return date", order: true, search: true, class: 'text-center' },
    { key: "total_travel_days", name: "total travel days", order: true, search: true, class: 'text-center' },

    {
        key: 'travel_partner', name: 'TRAVEL PARTNER', order: true, search: false, class: 'text-center', alias: true, itemsAlias:
            [
                {
                    alias: 'SI',
                    color: 'success',
                    key: true,
                },
                {
                    alias: 'NO',
                    color: 'secondary',
                    key: false,
                },
            ]
    },
    {
        key: 'embassy_requires', name: 'EMBASSY REQUIRES', order: true, search: false, class: 'text-center', alias: true, itemsAlias:
            [
                {
                    alias: 'SI',
                    color: 'success',
                    key: true,
                },
                {
                    alias: 'NO',
                    color: 'secondary',
                    key: false,
                },
            ]
    },

    { key: "comment", name: "comment", order: true, search: true, class: 'text-center' },

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
                {
                    alias: 'Cancelled',
                    color: 'secondary',
                    key: 3,
                },
            ]
    },

])




let data = ref([])
let selectedItems = ref([])


let listtTravelMode= []
let listtTravelDivision= []
let listtTravelentity= []
let listtTravelNatinatalies= []
let listtTravelRegion= []
let listtTravelCountries= []

let optionsTravelMode= ref([])
let optionsTravelDivision= ref([])
let optionsTravelentity= ref([])
let optionsTravelNatinatalies= ref([])
let optionsTravelRegion= ref([])
let optionsTravelCountries= ref([])





let optionState = ref([
    { value: 1, title: 'Active' },
    { value: 2, title: 'Inactive' },
    { value: 3, title: 'Cancelled' },
])

let optionTypeInput= ref([
    { value: "I", title: 'Ingreso' },
    { value: "S", title: 'Salida' },
])

let travelLogDefault = {
    id: 0,
    travel_destination: "",
    date: moment().format('YYYY-MM-DD'),
    year_calendar: 0,
    fiscal_year: 0,
    name: "",
    lasta_name: "",
    contact: "",
    airline: "",
    travel_start_date: moment().format('YYYY-MM-DD'),
    travel_return_date: moment().format('YYYY-MM-DD'),
    total_travel_days: 0,
    travel_partner: false,
    comment: "",
    insurance_period: "",
    embassy_requires: false,
    state: 0,
    country_id: 1,
    division_id: null,
    entity_id: null,
    nationality_id: null,
    region_id: null,
    travel_type_id: null,
    risk: false,
    entity: "",
    division: "",
    region: "",
    nationality: "",
    travel_modes: ""
}

let travelLog = ref({
    id: 0,
    travel_destination: "",
    date: "2024-08-10",
    year_calendar: 0,
    fiscal_year: 0,
    name: "",
    lasta_name: "",
    contact: "",
    airline: "",
    travel_start_date: "",
    travel_return_date: "",
    total_travel_days: 0,
    travel_partner: false,
    comment: "",
    insurance_period: "",
    embassy_requires: false,
    state: 0,
    country_id: 1,
    division_id: null,
    entity_id: null,
    nationality_id: null,
    region_id: null,
    travel_type_id: null,
    risk: false,
    entity: "",
    division: "",
    region: "",
    nationality: "",
    travel_modes: "",
})


let travel_destination_ids = ref([])


let startDate= ref(moment().format('YYYY-MM-DD'))
let returnDate= ref(moment().format('YYYY-MM-DD'))

let configTravelStartDate  = ref({dateFormat: 'Y-m-d', maxDate: returnDate, allowInput: true})
let configTravelReturnDate  = ref({dateFormat: 'Y-m-d', minDate: startDate , maxDate: new Date(), allowInput: true})


onMounted(() => {


    listData()

    travel_mode()
    travel_division()
    travel_entry()
    travel_nationalities()
    travel_region()
    travel_countries()

  

})






const listData = async (idselect = 0) => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/travel-logs/1-2-3`,
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




const travel_mode = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/travel-modes/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listtTravelMode = response.data.data

            optionsTravelMode.value = listtTravelMode.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.name}`.toUpperCase(),
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


const travel_division = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/travel-divisions/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listtTravelDivision= response.data.data

            optionsTravelDivision.value = listtTravelDivision.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.name}`.toUpperCase(),
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


const travel_entry = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/travel-entities/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listtTravelentity= response.data.data

            optionsTravelentity.value = listtTravelentity.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.name}`.toUpperCase(),
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



const travel_nationalities = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/travel-nationalities/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listtTravelNatinatalies= response.data.data

            optionsTravelNatinatalies.value = listtTravelNatinatalies.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.name}`.toUpperCase(),
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



const travel_region = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/travel-regions/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listtTravelRegion= response.data.data

            optionsTravelRegion.value = listtTravelRegion.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.name}`.toUpperCase(),
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



const travel_countries = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/travel-countries/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listtTravelCountries= response.data.data

            optionsTravelCountries.value = listtTravelCountries.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.name}`.toUpperCase(),
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



const onEdit = async (item: any) =>  {


    accion.value = 2
    // isDrawerVisible.value = true

    dialog.value = true

    if (refForm.value != null)
        refForm.value.reset();

    id.value = item.id

    travelLog.value={...item}


    const arrayCountrys = [];
    travelLog.value.travel_destination.split(",").filter((item) => {
        const found = optionsTravelCountries.value.find(element => element.value === Number(item));
        if (found !== undefined) {
            arrayCountrys.push(Number(item));
        }
    });

    travel_destination_ids.value = arrayCountrys;

    updateTravelStartDate()
    updateTravelReturntDate()

    calcularDiferenciaDias()



}



const onNew = () => {
    accion.value = 1

    dialog.value = true

    // isDrawerVisible.value = true

    if (refForm.value != null)
        refForm.value.reset();

    id.value = null

    travelLog.value = {...travelLogDefault}

    travel_destination_ids.value = []

    updateTravelStartDate()
    updateTravelReturntDate()

    calcularDiferenciaDias()

   



}


const onSubmit = async () => {


    if ((travelLog.value.date ?? "").toString().length <=0 || ((travelLog.value.travel_start_date ?? "").toString().length <=0) || ((travelLog.value.travel_return_date ?? "").toString().length <=0)) {
        messagePopup('warning', 'Date is required')
        return
    }

    const isValid = await refForm.value.validate();
    if (!isValid.valid) return;

    let contador=0

    let travel_destination_ids_str=''

    travel_destination_ids.value.filter((item) => {

        if (parseInt(item) == 0) {
            return;
        }

        if (contador === 0) {
            travel_destination_ids_str = item;
        } else {
            travel_destination_ids_str = travel_destination_ids_str + ',' + item;
        }
        contador++;
    });
    

    isSnackbarVisible.value = false

    let year_calendar = moment(travelLog.value.travel_start_date).format('YYYY')
    let year_fiscal = moment(travelLog.value.travel_start_date).format('YYYY')

    let data = {

        travel_destination: travel_destination_ids_str,
        date: travelLog.value.date,
        year_calendar: year_calendar,
        fiscal_year: year_fiscal,
        name: travelLog.value.name,
        lasta_name: travelLog.value.lasta_name,
        contact: travelLog.value.contact,
        airline: travelLog.value.airline,
        travel_start_date: travelLog.value.travel_start_date,
        travel_return_date: travelLog.value.travel_return_date,
        total_travel_days: travelLog.value.total_travel_days,
        travel_partner: travelLog.value.travel_partner,
        comment: travelLog.value.comment,
        insurance_period: travelLog.value.insurance_period,
        embassy_requires: travelLog.value.embassy_requires,
        risk: travelLog.value.risk,

        country: travelLog.value.country_id,
        division: travelLog.value.division_id,
        entity: travelLog.value.entity_id,
        nationality: travelLog.value.nationality_id,
        region: travelLog.value.region_id,
        travel_type: travelLog.value.travel_type_id,
        
        state: accion.value == 1 ?  1 : travelLog.value.state,
    }

    console.log(data);
    
    // return;
    


    const config = {
        method: accion.value == 1?  "post": "put",
        url:  accion.value == 1? "/travel-log/create": "/travel-log/update/" + id.value.toString(),
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
        url: "/travel-log/delete/" + id.value.toString(),
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
            fileLink.setAttribute('download', "ingresos.xlsx");
            document.body.appendChild(fileLink);
            fileLink.click();

        }
    } catch (error) {
        console.log("error ");
    }
}



const minValidatorRespiracion = (value) => {
    return value > 0 || `Mayor que 0`
}

const updateTravelStartDate = () =>{
    
    startDate.value = travelLog.value.travel_start_date
}

const updateTravelReturntDate = () =>{

    returnDate.value = travelLog.value.travel_return_date
}

const calcularDiferenciaDias = () => {
    let fechaInicio = new Date(travelLog.value.travel_start_date);
    let fechaFin = new Date(travelLog.value.travel_return_date);
    let diferenciaTiempo = fechaFin - fechaInicio
    travelLog.value.total_travel_days =( diferenciaTiempo / (1000 * 3600 * 24) + 1);
}

const calRiskCountry = () =>{

    let state_risk = false

    for (let item of travel_destination_ids.value){

        const found = listtTravelCountries.find(element => element.id === Number(item));

        if (found !== undefined) {
            if (found.risk){
                state_risk = found.risk
            }
        }
    }

    travelLog.value.risk = state_risk
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
                        
                        LIST OF TRAVELS
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


                        <!-- <div class="me-3">

                            <VBtn color="secondary"
                                :to="{ name: 'proyswarm-prospeccioncentropoblados-prospeccion_centro_poblado_updatemasivo' }">
                                Actualizacion Masiva de Empadronamiento
                            </VBtn>
                        </div>  -->

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


        <VDialog
            v-model="dialog"
            max-width="1300"
            class="custom-dialog"
            persistent 
            no-click-animation 
        >
            <VCard>
                <VForm ref="refForm" @submit.prevent="onSubmit">
                    <VToolbar dense flat>
                        <VToolbarTitle>
                            {{ accion == 1 ? 'NEW TRAVEL' : 'EDIT TRAVEL '  }}

                         
                            
                        </VToolbarTitle>
                        <VSpacer />
                    
                    
                        <VBtn
                            color="primary"
                            prepend-icon="mdi-content-save"
                            type="submit"
                        >
                                GUARDAR
                        </VBtn>
                        <VBtn
                            color="secondary"
                            prepend-icon="mdi-close-circle"
                            @click="dialog = false">
                            CANCELAR
                        </VBtn>

                    </VToolbar>
                    <VCardText>
                    
                        <VRow justify="space-between">



                                    <VCol cols="3">
                                        <AppDateTimePicker v-model="travelLog.date"  label="Date"  class="date-time-picker"
                                          :config="{dateFormat: 'Y-m-d', maxDate: new Date(), allowInput: true}" 
                                        :rules="[requiredValidator]" disabled />
                                    </VCol>

                                    <VCol cols="3">
                                        <VTextField v-model="travelLog.contact" label="Contact" :rules="[requiredValidator]" type="email" />
                                    </VCol>
                                    <VCol cols="3">
                                        <VTextField v-model="travelLog.name" label="Name" :rules="[requiredValidator]" />
                                    </VCol>

                                    <VCol cols="3">
                                        <VTextField v-model="travelLog.lasta_name" label="Lasta Name" :rules="[requiredValidator]" />
                                    </VCol>
                                    
                                    
                                    <VCol cols="3">
                                        <VSelect v-model="travelLog.nationality_id" label="Nationality" :rules="[requiredValidator]"
                                             :items="optionsTravelNatinatalies"  />
                                    </VCol>

                                    <VCol cols="3">
                                        <VSelect v-model="travelLog.division_id" label="Division" :rules="[requiredValidator]"
                                             :items="optionsTravelDivision"   />
                                    </VCol>
                                    
                                    <VCol cols="3">
                                        <VSelect v-model="travelLog.entity_id" label="Company" :rules="[requiredValidator]"
                                             :items="optionsTravelentity"  />
                                    </VCol>

                                    <VCol cols="3">
                                        <VSelect v-model="travelLog.travel_type_id" label="Travel Type" :rules="[requiredValidator]"
                                             :items="optionsTravelMode"  />
                                    </VCol>
                                    
                                  
                                    <VCol cols="3">
                                        <VSelect v-model="travelLog.region_id" label="Region" :rules="[requiredValidator]"
                                             :items="optionsTravelRegion"  />
                                    </VCol>
                                
                                    <VCol cols="3">
                                        <VTextField v-model="travelLog.airline" label="Airline" :rules="[requiredValidator]" />
                                    </VCol>
                                     
                                    <VCol cols="4">
                                        <VSelect v-model="travel_destination_ids" label="Travel destination" :rules="[requiredValidator]" multiple
                                             :items="optionsTravelCountries"  @update:model-value="calRiskCountry"  />
                                    </VCol>
                                    
                                    <VCol cols="2">
                                        <VCheckbox v-model="travelLog.risk" label="Country Risk" readonly/>
                                    </VCol>

                                    <VCol cols="4">
                                        <AppDateTimePicker v-model="travelLog.travel_start_date"  label="Travel start date"  class="date-time-picker"
                                          :config="configTravelStartDate"  @update:model-value="updateTravelStartDate();calcularDiferenciaDias()" 
                                        :rules="[requiredValidator]" />
                                    </VCol>
                                   
                                    <VCol cols="4">
                                        <AppDateTimePicker v-model="travelLog.travel_return_date"  label="Travel return Date"  class="date-time-picker"
                                          :config="configTravelReturnDate" @update:model-value="updateTravelReturntDate();calcularDiferenciaDias()"
                                        :rules="[requiredValidator]" />
                                    </VCol>


                                    <VCol cols="4">
                                        <VTextField v-model="travelLog.total_travel_days" label="Total travel days" :rules="[requiredValidator]" disabled />
                                    </VCol>
                                    
                                    <VCol cols="3">
                                        <VCheckbox v-model="travelLog.travel_partner" label="Travel Partner"/>
                                    </VCol>
                                    <VCol cols="3">
                                        <VCheckbox v-model="travelLog.embassy_requires" label="embassy requires"/>
                                    </VCol>
                                    
                                    <VCol cols="3">
                                        <VTextField v-model="travelLog.insurance_period" label="Insurance Period" :rules="[requiredValidator]" />
                                    </VCol>


                                    <VCol cols="3" v-if="accion ==2">
                                        <VSelect v-model="travelLog.state" label="State" :rules="[requiredValidator]" 
                                             :items="optionState"   />
                                    </VCol>
                                       
                                    
                                    <VCol cols="12">
                                        <VTextarea v-model="travelLog.comment"   label="comment*"  rows="2"  />
                                    </VCol>
                                 
                                
                            

                        </VRow>
    
                       
                        
                        
                        
                    </VCardText>
                    
                    
                </VForm>    
            </VCard>
        </VDialog>

       

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
    subject: travel_log
</route>

    