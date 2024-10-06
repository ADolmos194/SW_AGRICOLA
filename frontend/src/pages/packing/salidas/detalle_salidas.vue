<script lang="ts" setup>

import { messagePopupConfirm } from '@/functionsGlobals.js';
import snackbar from "@/layouts/components/SnackBar.vue";
import moment from 'moment';
import { PerfectScrollbar } from 'vue3-perfect-scrollbar';
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
let radioSearch = ref('fecha')

let searchQueryDetailLote = ref('')
let rowPerPageDetailLote = ref(10)
let isLoadingDetailLote = ref(false)
let radioSearchDetailLote = ref('sublote')


let isDrawerVisible = ref(false)
let accion = ref(1)
const refForm = ref(null);
const refFormDialog = ref(null);

let filters = ref([])

let minDate= ref(moment().format('YYYY-MM-DD'))
let maxdate= ref(moment().format('YYYY-MM-DD'))


let configSelectFecha = ref({dateFormat: 'Y-m-d', maxDate: maxdate,  allowInput: true, minDate: minDate})


// let isLoadingDetail = ref(false)
// let searchQueryDetail = ref('')
// let rowPerPageDetail = ref(10)
// let filtersDetail = ref([])
// let radioSearchDetail = ref('lote')

let dialog = ref(false)


let columns = ref([
    
   

    // {key: "guia_remicion", name: "guia_remicion", order:true, search: true, class: 'text-center'},
    // {key: "guia_transportista", name: "guia_transportista", order:true, search: true, class: 'text-center'},
    { key: "fecha", name: "fecha", order: true, search: true, class: 'text-center' },
    {key: "serie_lote", name: "serie lote", order:true, search: true, class: 'text-center'},
    {key: "consumo_total", name: "consumo total", order:true, search: true, class: 'text-center'},
    {key: "merma", name: "merma", order:true, search: true, class: 'text-center'},
    {key: "procesado", name: "procesado", order:true, search: true, class: 'text-center'},
    {key: "respiracion_ptje", name: "respiracion %", order:true, search: true, class: 'text-center'},
    {key: "respiracion_kg", name: "respiracion kg", order:true, search: true, class: 'text-center'},
    {key: "stock_consumo", name: "stock a consumir", order:true, search: true, class: 'text-center'},
    {key: "variedad", name: "variedad", order:true, search: true, class: 'text-center'},
    {key: "cultivo", name: "cultivo", order:true, search: true, class: 'text-center'},
    {key: "subgrupo", name: "sub grupo", order:true, search: true, class: 'text-center'},
    {key: "grupo", name: "grupo", order:true, search: true, class: 'text-center'},
    {key: "proveedor", name: "proveedor", order:true, search: true, class: 'text-center'},
    {key: "fecha_creacion", name: "fecha creacion", order:true, search: true, class: 'text-center'},
   
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
let dataDetailLote = ref([])
let listDetailMovement = ref([])
let selectedItems = ref([])

let idSelect = ref(null)


let listTipoEnvase = []
let listProveedor=[]
let listVariedad=ref([])

let optionState = ref([
    { value: 1, title: 'Activo' },
    { value: 2, title: 'Inactivo' },
])
let optionProveedor = ref([])
let optionTipoEnvase = ref([])
let optionVariedad = ref([])

let filterDataLoteDetalle= ref([])
let itemSelectedDetail= ref(null)


let state_id = ref(null)
let id = ref(null)



let isSnackbarVisible = ref(null)
let titleSnackbar = ref(null)
let stateSnackbar = ref(null)


let detail_defaul = {
    id: null,
    movimiento_id: null,
    lote: "",
    serie: "",
    serie_lote: "",
    sublote: "",
    grupo_id: null,
    grupo: "",
    subgrupo_id: null,
    subgrupo: "",
    cultivo_id: null,
    cultivo: "",
    variedad_id: null,
    variedad: "",
    tipo_envase_id: null,
    tipo_envase: "",
    peso_envase: 0,
    cantidad_envase: 1,
    peso_bruto: 0,
    peso_neto_guia: 0,
    peso_balanza: 0,
    peso_neto_planta: 0,
    peso_promedio_jaba: 0,
    diferencia_peso_guia: 0,
    porcentaje: 0,
    estado: 1,
    gruposublote: 1,
    proveedor_centro_id: null,
    proveedor_id: null,
    proveedor: '',

    movimiento_detalle_id: null,
    stock_consumo: 0,
    merma: 0,
    procesado: 1,
    respiracion_ptje: "0",
    respiracion_kg: 0,
    consumo_total: "0",
    stock: "0",
    fecha: null,

    maxmema: 0,
    maxprocesado: 1,
    maxrespiracion: 0,
    minFecha: null
}

let detail = ref({
    id: null,
    movimiento_id: null,
    lote: "",
    serie: "",
    serie_lote: "",
    sublote: "0",
    grupo_id: null,
    grupo: "",
    subgrupo_id: null,
    subgrupo: "",
    cultivo_id: null,
    cultivo: "",
    variedad_id: null,
    variedad: "",
    tipo_envase_id: null,
    tipo_envase: "",
    peso_envase: 0,
    cantidad_envase: 1,
    peso_bruto: 0,
    peso_neto_guia: 0,
    peso_balanza: 0,
    peso_neto_planta: 0,
    peso_promedio_jaba: 0,
    diferencia_peso_guia: 0,
    porcentaje: 0,
    estado: 1,
    gruposublote: 1,
    proveedor_centro_id: null,
    proveedor_id: null,
    proveedor: '',

    movimiento_detalle_id: null,
    stock_consumo: 0,
    merma: 0,
    procesado: 1,
    respiracion_ptje: "0",
    respiracion_kg: 0,
    consumo_total: "0",
    stock: "0",
    fecha: null,

    maxmema: 0,
    maxprocesado: 1,
    maxrespiracion: 0,
    minFecha: null
})


let itemDetailMovement = ref([])
let optionGrupoLote = ref([])



let itemMovement = ref({
    id: null,
    distrito_centro_id: null,
    distrito_id: null,
    distrito: "",
    provincia_id: null,
    provincia: "",
    departamento_id: null,
    departamento: "",
    procedencia: "",
    almacen_mov_doc_subgrupo_id: null,
    almacen_subgrupo_id: null,
    almacen_id: null,
    almacen: "",
    subgrupo_id: null,
    subgrupo: "",
    centro_id: null,
    centro: "",
    guida_remicion: "",
    guia_tranportista: "",
    fecha: "",
    // proveedor_centro_id: null,
    // proveedor_id: null,
    // proveedor: "",
    vehiculo_id: null,
    vehiculo: "",
    transportista_id: null,
    transportista: "",
    campania_id: null,
    campania: 2024,
    documento: '',
    // inspeccion: false,
    estado: 1
})

onMounted(() => {

    itemMovement.value =  JSON.parse(localStorage.getItem('salida') ?? JSON.stringify(itemMovement))

    listData()
    // listDataDetailLote()

    // getListProveedor()
    // getListTipoEnvase()
    getListVariedad()
    

})



let optionLotes = computed(() => {
    return listVariedad.value.filter((i: any) => 
        parseInt(i.producto_id) == parseInt(detail.value.variedad_id) &&
        parseFloat(i.stock_apto.toString()) > parseFloat(i.consumo_total.toString())
    ).map((item: any) => {
        return {
            value: item.detalle_ingreso_id,
            title: `${item.documento} - ${item.lote}`.toUpperCase(),
        };
    })
})


const listData = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/salidas-detalle/1-2/${itemMovement.value.id}`,
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

/* const listDataDetailLote = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/ingreso-detalle-lote/1/${itemMovement.id}`,
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            dataDetailLote.value = response.data.data
            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;

    }
}
 */


const getListProveedor = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/proveedor-centro/1/${itemMovement.value.centro_id}`,
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listProveedor = response.data.data
            
            optionProveedor.value = listProveedor.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.ruc} - ${item.nombre.toUpperCase()}`,
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



const getListTipoEnvase = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/tipoenvase/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listTipoEnvase = response.data.data

            optionTipoEnvase.value = listTipoEnvase.map((item: any) => {
                return {
                    value: item.producto_id,
                    title: `${item.producto}`.toUpperCase(),
                    peso: item.peso
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

const getListVariedad = async () => {

    isLoading.value = true

    const config = {
        method: "post",
        url: `/variedad-subgrupo`,
        data: {
            date: itemMovement.value.fecha,
            state: 1,
            subgrupo: itemMovement.value.subgrupo_id
        }
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listVariedad.value = response.data.data

           /*  optionVariedad.value = listVariedad.map((item: any) => {
                return {
                    value: item.producto_id,
                    title: `${item.abr_cultivo} - ${item.producto.toUpperCase()}`,
                };
            }); */



            optionVariedad.value = listVariedad.value.filter((item: any) => parseInt(item.subgrupo_id) == parseInt(itemMovement.value.subgrupo_id ?? "0")).map((item: any) => {
                return {
                    value: item.producto_id,
                    title: `${item.abr_cultivo} - ${item.producto}`.toUpperCase(),
                    serie_lote: item.serie_lote,
                    detalle_ingreso_id: item.detalle_ingreso_id
                };
            });

            // eliminar los variedades duplicadas de optionvariedad
            let variedades = []
            let variedades_id = []
            for (let item of optionVariedad.value){
                if (!variedades_id.includes(item.value)){
                    variedades_id.push(item.value)
                    variedades.push(item)
                }
            }
            optionVariedad.value = variedades

            detail.value.variedad_id = null
            detail.value.movimiento_detalle_id = null
            

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
    isDrawerVisible.value = true
    // dialog.value = true

    idSelect.value = item.id

    if (refFormDialog.value != null)
        refFormDialog.value.reset();

    detail.value = {...item}    

    id.value = item.id
    state_id.value = item.estado

    // filterDataLoteDetalle.value = dataDetailLote.value.filter((i: any) => parseInt(i.movimiento_detalle_id) == parseInt(item.id ?? '0'))

    // itemDetailMovement.value=[...filterDataLoteDetalle.value]

    // for (let index=0; index < itemDetailMovement.value.length; index++){
    //     setPesoEnvase(index)
    // }


    // optionGrupoLote.value= []

}

const onNew = () => {
    accion.value = 1

    // dialog.value = true
    isDrawerVisible.value = true


    if (refForm.value != null)
        refForm.value.reset();

    id.value = null

    // itemDetailMovement.value= []
    // optionGrupoLote.value= []

    detail.value = {...detail_defaul}

    // onNewDetialMovement()


}


const onSubmitCreateLote = async () => {
    const isValid = await refForm.value.validate();
    if (!isValid.valid) return;


    isSnackbarVisible.value = false


    let data = {
        movimiento: itemMovement.value.id, 
        movimiento_detalle: detail.value.movimiento_detalle_id, 
        fecha: detail.value.fecha, 
        stock_consumo: detail.value.stock_consumo, 
        merma: detail.value.merma, 
        procesado: detail.value.procesado, 
        respiracion_ptje: detail.value.respiracion_ptje, 
        respiracion_kg: detail.value.respiracion_kg, 
        consumo_total: detail.value.consumo_total, 
    }


    const config = {
        method: "post",
        url: "/salidas-detalle-create/",
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            await listData()
            await getListVariedad()
            onInputed(detail.value)

            stateSnackbar.value = 'success'
            titleSnackbar.value = accion.value == 1 ? 'Registro creado con exito' : 'Registro actualizado con exito'
            
            isDrawerVisible.value = false
            // dialog.value = false
            // refFormDialog.value.reset();

        } else {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = accion.value == 1 ? 'Error al crear el registro' : 'Error al actualizar el registro'
        }
    } catch (error) {
        if (error.response.status == 409) {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = error.response.data.message_user

        } else {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = accion.value == 1 ? 'Error al crear el registro' : 'Error al actualizar el registro'
        }
    } finally {
        isSnackbarVisible.value = true

    }
}



const onDelete = async (item: any) => {


    let values = await messagePopupConfirm({
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
        url: "/salidas-detalle-update-state/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            isDrawerVisible.value = false
            // listData()
            await listData()
            await getListVariedad()
            // listDataDetailLote()

            stateSnackbar.value = 'success'
            titleSnackbar.value = 'Registro eliminado con exito'
        }
    } catch (error) {
        stateSnackbar.value = 'danger'
        titleSnackbar.value = 'Error al eliminar el registro'
    } finally {
        isSnackbarVisible.value = true
    }

}

const onColSelected = (item: any) => {
    radioSearch.value = item
}


const onInputed = (item: any) => {


    idSelect.value = item.id

    // listDetailMovement.value = dataDetail.value.filter((item: any) => parseInt(item.movimiento_id) == (itemMovement.value.id ?? 0));

    // filterDataLoteDetalle.value = dataDetailLote.value.filter((i: any) => parseInt(i.movimiento_detalle_id) == parseInt(item.id ?? '0'))

}








const onColSelectedDetail = (item: any) => {
    radioSearchDetailLote.value = item

}




const deleteItemDetail = (item, index) =>{
    
    itemDetailMovement.value.splice(index, 1)

    optionGrupoLote.value = []

    let cont=0

    for (let index=0; index < itemDetailMovement.value.length; index++){
        cont++
        optionGrupoLote.value.push(cont)

        if ( parseInt(itemDetailMovement.value[index].gruposublote) > itemDetailMovement.value.length){
            itemDetailMovement.value[index].gruposublote = itemDetailMovement.value.length.toString()
        }

    }

}

const onNewDetialMovement = () =>{

    itemDetailMovement.value.push({...detail_defaul})
    optionGrupoLote.value = []

    let cont=0
    for (let index=0; index < itemDetailMovement.value.length; index++){
        // itemDetailMovement.value[index].id = cont+1
        itemDetailMovement.value[index].gruposublote = cont+1
        cont++
        optionGrupoLote.value.push(cont)
    }
   
}

const onCalcItemDetail = (item, index:number) =>{


    let cantidad = parseFloat(itemDetailMovement.value[index].cantidad_envase)
    let peso_bruto = parseFloat(itemDetailMovement.value[index].peso_bruto)
    let peso_envase = parseFloat(itemDetailMovement.value[index].peso_envase)
    let peso_balanza = parseFloat(itemDetailMovement.value[index].peso_balanza)


    itemDetailMovement.value[index].peso_neto_guia = (peso_bruto - (cantidad * peso_envase)).toFixed(2)
    itemDetailMovement.value[index].peso_neto_planta = (peso_balanza - (cantidad * peso_envase)).toFixed(2)
    
    let peso_net_planta=  parseFloat(itemDetailMovement.value[index].peso_neto_planta.toString())
    
    itemDetailMovement.value[index].peso_promedio_jaba = (peso_net_planta / cantidad).toFixed(2)
    
    
    let peso_neto_guia = parseFloat(itemDetailMovement.value[index].peso_neto_guia.toString())

    itemDetailMovement.value[index].diferencia_peso_guia = peso_neto_guia - peso_net_planta
    
    let diferencia_peso_guia =  parseFloat(itemDetailMovement.value[index].diferencia_peso_guia.toString())


    itemDetailMovement.value[index].porcentaje = ((diferencia_peso_guia / peso_bruto) * 100).toFixed(2)


    
   
}

/* const setPesoEnvase = () =>{

    let tipoenvase = optionTipoEnvase.value.filter((item: any) => parseInt(item.value) == parseInt(.tipo_envase_id))

    itemDetailMovement.value[index].peso_envase = tipoenvase.length > 0 ? tipoenvase[0].peso : 0
} */


const onCalLotesPesoNeto = () =>{

        
    let itemLote = listVariedad.value.filter((i: any) => parseInt(i.detalle_ingreso_id) == parseInt(detail.value.movimiento_detalle_id))

    detail.value.stock_consumo = itemLote.length > 0 ? itemLote[0].stock_apto - itemLote[0].consumo_total : 0

    detail.value.minFecha = itemLote.length > 0 ? itemLote[0].fecha_inspeccion : null

    minDate.value= detail.value.minFecha

    onCalcItemDetailMerma()
    onCalcItemDetailProcesado()
    onCalcItemDetailRespiracion()


}


const onCalcItemDetailMerma  = () =>{

    let peso_neto = parseFloat((detail.value.stock_consumo ?? "0").toString())
    let procesado = parseFloat((detail.value.procesado ?? "0").toString())
    detail.value.maxmema = peso_neto - procesado

    onCalConsumtoTotalStock()

}


const onCalcItemDetailProcesado = () =>{

    let peso_neto = parseFloat((detail.value.stock_consumo ?? "0").toString())
    let merma = parseFloat((detail.value.merma ?? "0").toString())
    detail.value.maxprocesado = peso_neto - merma

    onCalConsumtoTotalStock()

}

const onCalcItemDetailRespiracion = () =>{

    let peso_neto = parseFloat((detail.value.stock_consumo ?? "0").toString())
    let merma = parseFloat((detail.value.merma ?? "0").toString())
    let procesado = parseFloat((detail.value.procesado ?? "0").toString())
    let respiracion = parseFloat((detail.value.respiracion_ptje ?? "0").toString())


    detail.value.maxrespiracion = (100 * (peso_neto - (merma + procesado)))/peso_neto  //((peso_neto - merma - procesado)/procesado) * 100

    detail.value.respiracion_kg = peso_neto  *  (respiracion / 100)

    onCalConsumtoTotalStock()
}


const onCalConsumtoTotalStock = () =>{

    let peso_neto = parseFloat((detail.value.stock_consumo ?? "0").toString())
    let merma = parseFloat((detail.value.merma ?? "0").toString())
    let procesado = parseFloat((detail.value.procesado ?? "0").toString())
    let respiracion_kg = parseFloat((detail.value.respiracion_kg ?? "0").toString())

    let consumo_total =  merma + procesado + respiracion_kg
    detail.value.consumo_total  = (consumo_total).toFixed(2)
    detail.value.stock  =  (peso_neto - consumo_total).toFixed(2)

}


const maxValidatorMerma = (value, max) => {
    return value <=max || `No exeder ${max.toFixed(2)}`;
}


const maxValidatorProcesado = (value, max) => {
    //return 0> value <= max || `No exeder ${max.toFixed(2)}`

    if (value <=0) {
        return `No bajar de 0`;
    }
    if (value > max) {
        return `No exeder ${max.toFixed(2)}`;
    }
    return true;

}

const maxValidatorRespiracion = (value, max) => {
    return value <= parseFloat(max.toFixed(3)) || `No exeder ${max.toFixed(3)}`
}

const maxValidatorDuplciado = (value, index) => {

    let item = itemDetailMovement.value.filter((i: any) => parseInt(i.movimiento_detalle_id) == parseInt(value) && parseInt(i.id) != index )


    return item.length <= 0  || `No se puede duplicar el lote`;
}


const onSetValRespiracion = () =>{
    detail.value.respiracion_ptje = detail.value.maxrespiracion.toFixed(3)
    

    onCalcItemDetailRespiracion()
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
                        <VBtn icon size="small" @click="router.go(-1)"
                            style="background-color: transparent !important; box-shadow: none;">
                            <VIcon size="22" icon="tabler-arrow-big-left" color="primary" />
                            <VTooltip activator="parent" location="end">
                                Volver a las Ingresos
                            </VTooltip>
                        </VBtn>
                        DETALLE DE SALIDAS DE MATERIA PRIMA DOCUMENTO: {{ itemMovement.documento }}
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



                            <VBtn prepend-icon="tabler-plus" @click="onNew()">
                                Nuevo
                            </VBtn>

                            <!-- <VBtn variant="tonal" color="secondary" prepend-icon="tabler-screen-share"
                                @click="downloadExcel()">
                                Exportar
                            </VBtn> -->
                        </div>
                    </VCardText>

                    <VDivider />

                    <VRow>
                        <VCol cols="12">
                            <DataTableCustom 
                                :colums="columns"
                                :data="data"

                                :on-delete="onDelete" 
                                
                                :on-col="onColSelected" 
                                :is-loading="isLoading" 
                                :search-query="searchQuery"
                                
                                :row-per-page="rowPerPage" 
                                :filters="filters" 
                                

                                :icon-input="'tabler-eye'"
                                
                                :id-select="idSelect"

                                no-deleted-first="true"
                                >
                                <!-- :on-input="onInputed" -->
                                <!-- :on-edit="onEdit" -->
                                
                            </DataTableCustom>
                        </VCol>
                    </VRow>

                </VCard>
            </VCol>

      
        </VRow>


        
        <VNavigationDrawer temporary :width="400" location="end" class="scrollable-content"
            :model-value="isDrawerVisible" @update:model-value=" isDrawerVisible = false">

            <div class="d-flex align-center pa-6 pb-1">
                <h6 class="text-h6">
                    Nuevo detalle de ingreso
                </h6>

                <VSpacer />

                <VBtn variant="tonal" color="default" icon size="32" class="rounded"
                    @click=" isDrawerVisible = false">
                    <VIcon size="18" icon="tabler-x" />
                </VBTn>
            </div>

            <PerfectScrollbar :options="{ wheelPropagation: false }">
                <VCard flat>
                    <VCardText>

                        <VForm ref="refForm"  @submit.prevent="onSubmitCreateLote">
                            <VRow>
                                <VCol cols="12">
                                    <VAutocomplete v-model="detail.variedad_id"  :rules="[requiredValidator]"   label="VARIEDAD" :items="optionVariedad" clearable 
                                    @update:model-value="detail.movimiento_detalle_id=null; detail.fecha=null" />

                                </VCol>
                             
                                <VCol cols="12">
                                    <VAutocomplete v-model="detail.movimiento_detalle_id"  :rules="[requiredValidator]"   :items="optionLotes" 
                                    @update:model-value="detail.fecha=null; onCalLotesPesoNeto()" label="LOTE" clearable />
                                </VCol>


                                <VCol cols="12">
                                    <AppDateTimePicker 
                                    v-model="detail.fecha" clearable label="Seleccionar Fecha"  class="date-time-picker" 
                                    :config="configSelectFecha" 
                                    :rules="[requiredValidator]" />
                                </VCol>


                                <VCol cols="12">

                                    <VTextField type="number"  v-model="detail.stock_consumo"  disabled :rules="[requiredValidator]"  label="STOCK A CONSUMIR" />
                                </VCol>

                                <VCol  cols="12">
                                    <VTextField type="number"  v-model="detail.merma"   :rules="[requiredValidator,maxValidatorMerma(detail.merma, detail.maxmema)]" @update:model-value="onCalcItemDetailMerma(); onCalcItemDetailProcesado(); onCalcItemDetailRespiracion()" :min="0" :max="detail.maxmema" :label="`MERMA: 0 - ${detail.maxmema.toFixed(2)}`"/>
                                </VCol>
                               
                                <VCol  cols="12">
                                    <VTextField type="number"  v-model="detail.procesado"  :rules="[requiredValidator, maxValidatorProcesado(detail.procesado, detail.maxprocesado)]" :min="1" :max="detail.maxprocesado"   @update:model-value="onCalcItemDetailProcesado(); onCalcItemDetailMerma(); onCalcItemDetailRespiracion()"  :label="`PROCESADO: 1 - ${detail.maxprocesado.toFixed(2)}`"  />
                                </VCol>

                                <VCol  cols="12">
                                    <VTextField type="number"  v-model="detail.respiracion_ptje"  :rules="[requiredValidator, maxValidatorRespiracion(detail.respiracion_ptje, detail.maxrespiracion)]" :min="1" :max="detail.maxrespiracion"   @update:model-value="onCalcItemDetailProcesado(); onCalcItemDetailMerma(); onCalcItemDetailRespiracion()"  :label="`RESPIRACION %: 0 - ${detail.maxrespiracion.toFixed(2)}`"  />
                                </VCol>

                                <VCol  cols="12" class="text-right">
                                    <VBtn  size="x-small" color="success" @click="onCalcItemDetailRespiracion(); onSetValRespiracion()">
                                        consumo total
                                    </VBtn>
                                </VCol>
                               
                                <VCol  cols="12">
                                    <VTextField  type="number" disabled v-model="detail.respiracion_kg"  :rules="[requiredValidator]" label="RESPIRACION KG" />
                                </VCol>
                                
                                <VCol  cols="12">
                                    <VTextField  type="number" disabled v-model="detail.consumo_total"  :rules="[requiredValidator]" label="CONSUMO_TOTAL" />
                                </VCol>

                                <VCol  cols="12">
                                    <VTextField  type="number" disabled v-model="detail.stock"  :rules="[requiredValidator]" label="STOCK"/>
                                </VCol>
                               
                              
                                
                                <VCol cols="12">
                                    <VBtn type="submit" class="me-3">
                                        {{ accion === 1 ? 'Guardar' : 'Editar' }}
                                    </VBtn>
                                    <VBtn type="reset" variant="tonal" color="secondary"
                                        @click=" isDrawerVisible = false">
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

.col-variedad {
  inline-size: 350px;
}

.col-proveedor {
  inline-size: 430px;
}

.col-tipo-envase {
  inline-size: 218px;
}

.col-peso-envase {
  inline-size: 100px;
}

.col-cantidad-envase {
  inline-size: 100px;
}

.col-peso-bruto {
  inline-size: 100px;
}

.col-peso-neto-guia {
  inline-size: 100px;
}

.col-peso-balanza {
  inline-size: 100px;
}

.col-peso-neto-planta {
  inline-size: 100px;
}

.col-peso-promedio-jaba {
  inline-size: 150px;
}

.col-diferencia-peso-guia {
  inline-size: 150px;
}

.col-porcentaje {
  inline-size: 170px;
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

</style>
<route lang="yaml">
meta:
    action: manage
    subject: packing_detalle_salidas
</route>
