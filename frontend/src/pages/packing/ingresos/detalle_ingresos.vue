<script lang="ts" setup>

import { messagePopup, messagePopupConfirm } from '@/functionsGlobals.js';
import snackbar from "@/layouts/components/SnackBar.vue";
import DataTableCustom from "../../../layouts/components/DataTableCustomv2.vue";

import axios from "@axios";
import { requiredValidator } from '@validators';
import moment from 'moment';
import { defineProps, onMounted, ref } from 'vue';
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

let isLoadingSalidasLote = ref(false)
let dataLotesSalidas = ref([])

// let isLoadingDetail = ref(false)
// let searchQueryDetail = ref('')
// let rowPerPageDetail = ref(10)
// let filtersDetail = ref([])
// let radioSearchDetail = ref('lote')

let dialog = ref(false)


let columns = ref([
    
    {
        key: 'inspeccion', name: 'INSPECCION', order: true, search: false, class: 'text-center', alias: true, itemsAlias:
            [
                {
                    alias: 'INSP',
                    color: 'success',
                    key: true,
                },
                {
                    alias: 'SIN INSP',
                    color: 'secondary',
                    key: false,
                },
            ]
    },

    {key: "lote", name: "Correlativo", order:true, search: true, class: 'text-center'},
    {key: "stock", name: "Stock", order:true, search: true, class: 'text-center'},
    {key: "stock_apto", name: "Stock apto", order:true, search: true, class: 'text-center'},
    {key: "variedad", name: "variedad", order:true, search: true, class: 'text-center'},
    {key: "cultivo", name: "cultivo", order:true, search: true, class: 'text-center'},
    {key: "subgrupo", name: "sub grupo", order:true, search: true, class: 'text-center'},
    {key: "grupo", name: "grupo", order:true, search: true, class: 'text-center'},
    // {key: "cantidad", name: "cantidad", order:true, search: true, class: 'text-center'},
   
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


let columnsDetailLote = ref([

    {key: "sublote", name: "N°", order:true, search: true, class: 'text-center'},
    {key: "proveedor", name: "proveedor", order:true, search: true, class: 'text-center'},
    {key: "agricultor", name: "agricultor", order:true, search: true, class: 'text-center'},
    {key: "destino", name: "destino", order:true, search: true, class: 'text-center'},
    {key: "guia_remicion", name: "guia_remicion", order:true, search: true, class: 'text-center'},
    {key: "guia_transportista", name: "guia_transportista", order:true, search: true, class: 'text-center'},
    {key: "procedencia", name: "procedencia", order:true, search: true, class: 'text-left'},
    {key: "tipo_envase", name: "tipo envase", order:true, search: true, class: 'text-center'},
    {key: "peso_envase2", name: "peso envase", order:true, search: true, class: 'text-center'},
    {key: "cantidad_envase", name: "cantidad", order:true, search: true, class: 'text-center'},
    {key: "peso_guia", name: "peso guia", order:true, search: true, class: 'text-center'},
    {key: "peso_bruto", name: "peso bruto", order:true, search: true, class: 'text-center'},
    // {key: "peso_balanza", name: "peso balanza", order:true, search: true, class: 'text-center'},
    {key: "peso_neto", name: "peso neto", order:true, search: true, class: 'text-center'},
    {key: "peso_promedio_jaba", name: "peso promedio envase", order:true, search: true, class: 'text-center'},
    {key: "diferencia_peso_guia", name: "diferencia peso guia", order:true, search: true, class: 'text-center'},
    {key: "porcentaje", name: "%", order:true, search: true, class: 'text-center'},
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
let listAgricultores=[]
let listVariedad=[]
let listProvinciaCenter= []
let listDistrito= ref([])

let optionState = ref([
    { value: 1, title: 'Activo' },
    { value: 2, title: 'Inactivo' },
])

let optionProvincia = ref([])
let optionAgricultures = ref([])
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
    peso_guia: 0,
    // peso_balanza: 0,
    peso_neto: 0,
    
    peso_promedio_jaba: 0,
    diferencia_peso_guia: 0,
    porcentaje: 0,
    
    estado: 1,
    gruposublote: 1,
    proveedor_centro_id: null,
    proveedor_id: null,
    proveedor: '',

    guia_remicion: '',
    provincia_id: null,
    provincia: '',
    distrito_id: null,
    distrito: '',

    guia_transportista: '',
    inspeccion: false,
    no_apta_tamanio: 0,
    pasmado: 0,
    sobre_maduro: 0,
    pequenio: 0,
    otros: 0,
    fecha_inspeccion: null,
    
    stock: 0,
    stock_apto: 0,

    agricultor_id: null,
    agricultor: '',

    observacion_inspeccion: '',
    merma_produccion: 0,
    observacion_produccion: '',

    destino: '',

    distritos: []
    
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
    peso_guia: 0,
    // peso_balanza: 0,
    peso_neto: 0,
    
    peso_promedio_jaba: 0,
    diferencia_peso_guia: 0,
    porcentaje: 0,

    estado: 1,
    gruposublote: 1,
    proveedor_id: null,
    // proveedor_id: null,
    proveedor: '',

    guia_remicion: '',
    provincia_id: null,
    provincia: '',
    distrito_id: null,
    distrito: '',
    guia_transportista: '',
    inspeccion: false,
    no_apta_tamanio: 0,
    pasmado: 0,
    sobre_maduro: 0,
    pequenio: 0,
    otros: 0,
    fecha_inspeccion: null,

    stock: 0,
    stock_apto: 0,

    agricultor_id: null,
    agricultor: '',

    observacion_inspeccion: '',
    merma_produccion: 0,
    observacion_produccion: '',

    destino: '',
    distritos: []

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
    fecha: null,
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

    itemMovement.value =  JSON.parse(localStorage.getItem('ingreso') ?? JSON.stringify(itemMovement))

    listData()
    listDataDetailLote()

    getListProveedor()
    getListAgricultor()
    getListTipoEnvase()
    getListVariedad()
    getListProvincia()
    getListDistrito()
    

})



/* let optionDistrito =  computed(() => { 
    return listDistrito.value.filter((item: any) => parseInt(item.provincia_id) == parseInt(detail.value.provincia_id ?? '0')).map((item: any) => {
    return {
        value: item.id,
        title: `${item.cod} - ${item.descripcion}`.toUpperCase(),
        distrito_id: item.id,
        provincia_id: item.provincia_id,
    };
})
}) */




const listData = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/ingreso-detalle/1-2/${itemMovement.value.id}`,
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

const listDataDetailLote = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/ingreso-detalle-lote/1/${itemMovement.value.id}`,
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
                    title: `${item.ruc == null ? '': item.ruc.toString()} - ${item.nombre}`.toUpperCase(), // `${item.ruc} - ${item.nombre.toUpperCase()}`,
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

const getListAgricultor = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/agricultores-centro/1/${itemMovement.value.centro_id}`,
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listAgricultores = response.data.data
            
            optionAgricultures.value = listAgricultores.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.codigo == null ? '': item.codigo.toString() + " /"} ${item.nombre}`.toUpperCase(),  //`${item.ruc == null ? '': item.ruc.toString() + "-" } ${item.nombre}`.toUpperCase(),
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
        method: "get",
        url: `/variedad-subgrupo/1/${itemMovement.value.subgrupo_id}`,
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listVariedad = response.data.data

            optionVariedad.value = listVariedad.map((item: any) => {
                return {
                    value: item.producto_id,
                    title: `${item.abr_cultivo} - ${item.producto.toUpperCase()}`,
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

const getListProvincia = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/provincia-centro/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            
            listProvinciaCenter = response.data.data
            
           

            optionProvincia.value = listProvinciaCenter.filter((item: any) => item.centro_id == (itemMovement.value.centro_id ?? '')).map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.departamento} - ${item.descripcion}`.toUpperCase(),
                    departamento_id: item.departamento,
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


const getListDistrito = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/distrito/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listDistrito.value = response.data.data
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


const setDistritos = (index) =>{

    
    itemDetailMovement.value[index].distrito_id=null

    if (itemDetailMovement.value[index].provincia_id == null) {
        itemDetailMovement.value[index].distritos=[]
        return
    }


    itemDetailMovement.value[index].distritos = listDistrito.value.filter((item: any) => parseInt(item.provincia_id) == parseInt(itemDetailMovement.value[index].provincia_id ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.cod} - ${item.descripcion}`.toUpperCase(),
            distrito_id: item.id,
            provincia_id: item.provincia_id,
        };
    })

}

const setDistritos_edits = (index) =>{

    
    if (itemDetailMovement.value[index].provincia_id == null) {
        itemDetailMovement.value[index].distritos=[]
        return
    }


    itemDetailMovement.value[index].distritos = listDistrito.value.filter((item: any) => parseInt(item.provincia_id) == parseInt(itemDetailMovement.value[index].provincia_id ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.cod} - ${item.descripcion}`.toUpperCase(),
            distrito_id: item.id,
            provincia_id: item.provincia_id,
        };
    })

}

const listSalidaLote = async (id) => {

    isLoadingSalidasLote.value = true

    const config = {
        method: "get",
        url: `/salidas-lote/${id}`,
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            dataLotesSalidas.value = response.data.data
        }
    } catch (error) {
        console.log(error);
    }finally{
        isLoadingSalidasLote.value = false
    }
}





const onEdit = async (item: any) => {


    accion.value = 2
    // isDrawerVisible.value = true
    dialog.value = true

    idSelect.value = item.id

    dataLotesSalidas.value=[]

    if (refFormDialog.value != null)
        refFormDialog.value.reset();


    await listSalidaLote(item.id)

    detail.value = {...item}    

    if (!detail.value.inspeccion){
        detail.value.fecha_inspeccion = moment().format('YYYY-MM-DD')
    }

    id.value = item.id
    state_id.value = item.estado

    filterDataLoteDetalle.value = dataDetailLote.value.filter((i: any) => parseInt(i.movimiento_detalle_id) == parseInt(item.id ?? '0'))

    let list= []
    for (let item of filterDataLoteDetalle.value){
        list.push({...item})
    }
    // =[...dataDetailLote.value.filter((i: any) => parseInt(i.movimiento_detalle_id) == parseInt(item.id ?? '0'))]

    itemDetailMovement.value= []

    itemDetailMovement.value=list

    for (let index=0; index < itemDetailMovement.value.length; index++){
        setPesoEnvase(index)
        setDistritos_edits(index)
    }

    onCalcItemDetail2()

    optionGrupoLote.value= []

}

const onNew = () => {
    accion.value = 1

    dialog.value = true

    dataLotesSalidas.value=[]

    isLoadingSalidasLote.value = false


    if (refFormDialog.value != null)
        refFormDialog.value.reset();

    id.value = null

    itemDetailMovement.value= []
    optionGrupoLote.value= []

    detail.value = {...detail_defaul}

    detail.value.fecha_inspeccion = moment().format('YYYY-MM-DD')

    onNewDetialMovement()


}


const onSubmitCreateLote = async () => {


   
    if (detail.value.inspeccion){
        if ((detail.value.fecha_inspeccion ?? "").toString().length <=0) {
            messagePopup('warning', 'Fecha de ingreso es requerido')
            return
        }
    }
    
    const isValid = await refFormDialog.value.validate();
    if (!isValid.valid) return;


    let no_apta_tamanio = detail.value.inspeccion ? detail.value.no_apta_tamanio: 0
    let pasmado = detail.value.inspeccion ?  detail.value.pasmado: 0
    let sobre_maduro = detail.value.inspeccion ? detail.value.sobre_maduro: 0
    let pequenio = detail.value.inspeccion ?  detail.value.pequenio: 0
    let otros = detail.value.inspeccion ?  detail.value.otros: 0

    let suma = parseFloat(no_apta_tamanio.toString()) + parseFloat(pasmado.toString()) + parseFloat(sobre_maduro.toString()) + parseFloat(pequenio.toString()) + parseFloat(otros.toString())


    if (detail.value.stock < suma){
        messagePopup('warning', 'Stock no puede ser menor a la suma de los items de inspeccion')
        return
    }


    

    isSnackbarVisible.value = false


    let details = []

    for (let item of itemDetailMovement.value){

        let detail = {
            id: item.id,
            sublote: item.sublote,
            proveedor_id: item.proveedor_id,
            agricultor_id: item.agricultor_id,
            destino: item.destino,

            distrito: item.distrito_id,
            guia_remicion: item.guia_remicion,
            guia_transportista: item.guia_transportista,

            tipo_envase: item.tipo_envase_id,
            peso_envase: item.peso_envase,
            cantidad_envase: item.cantidad_envase,
            peso_bruto: item.peso_bruto,
            peso_guia: item.peso_guia,
            peso_neto: item.peso_neto,
            // peso_balanza: item.peso_balanza,
            peso_promedio_jaba: item.peso_promedio_jaba,
            diferencia_peso_guia: item.diferencia_peso_guia,
            porcentaje: item.porcentaje,
        }

        details.push(detail)

    }




    let data = {
        movimientoid: itemMovement.value.id,
        variedad: detail.value.variedad_id,
        // proveedor: detail.value.proveedor_id,
        // agricultor: detail.value.agricultor_id,
        inspeccion: detail.value.inspeccion,
        fecha_inspeccion: detail.value.inspeccion?  detail.value.fecha_inspeccion : null,
        fruta_no_apta: detail.value.inspeccion ? detail.value.no_apta_tamanio: 0,         
        pasmado: detail.value.inspeccion ?  detail.value.pasmado: 0,
        sobre_maduro: detail.value.inspeccion ? detail.value.sobre_maduro: 0,
        pequenio: detail.value.inspeccion ?  detail.value.pequenio: 0,
        otros: detail.value.inspeccion ?  detail.value.otros: 0,
        observacion_inspeccion:  detail.value.inspeccion ?  detail.value.observacion_inspeccion: null,
        merma_produccion: detail.value.inspeccion ?  detail.value.merma_produccion: 0,
        observacion_produccion:  detail.value.inspeccion ? detail.value.observacion_produccion:null,
        almance_subgrupo: itemMovement.value.almacen_subgrupo_id,
        estado: detail.value.estado,
        details: details
    }


    const config = {
        method: accion.value == 1? "post": "put",
        url: accion.value == 1? "/ingreso-detalle-create/": "/ingreso-detalle-update/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            await listData()
            await listDataDetailLote()
            onInputed(detail.value)

            stateSnackbar.value = 'success'
            titleSnackbar.value = accion.value == 1 ? 'Registro creado con exito' : 'Registro actualizado con exito'
            
            dialog.value = false
            refFormDialog.value.reset();

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
        // isDrawerVisible.value = false

    }
}



const onDelete = async (item: any) => {

    if (item.inspeccion){

        messagePopup("warning", 'No se puede eliminar un lote con inspeccion' )
        return
    }

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
        url: "/ingreso-detalle-update-state/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            isDrawerVisible.value = false
            listData()
            listDataDetailLote()

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

    filterDataLoteDetalle.value = dataDetailLote.value.filter((i: any) => parseInt(i.movimiento_detalle_id) == parseInt(item.id ?? '0'))

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

    onCalcItemDetail2()

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

    let index = itemDetailMovement.value.length - 1

    if (index > 0){
        itemDetailMovement.value[index].guia_remicion =itemDetailMovement.value[index-1].guia_remicion
        itemDetailMovement.value[index].guia_transportista =itemDetailMovement.value[index-1].guia_transportista
        itemDetailMovement.value[index].provincia_id = itemDetailMovement.value[index-1].provincia_id

        itemDetailMovement.value[index].distritos = listDistrito.value.filter((item: any) => parseInt(item.provincia_id) == parseInt(itemDetailMovement.value[index].provincia_id ?? '0')).map((item: any) => {
            return {
                value: item.id,
                title: `${item.cod} - ${item.descripcion}`.toUpperCase(),
                distrito_id: item.id,
                provincia_id: item.provincia_id,
            };
        })

        itemDetailMovement.value[index].distrito_id = itemDetailMovement.value[index-1].distrito_id
        itemDetailMovement.value[index].variedad_id = itemDetailMovement.value[index-1].variedad_id
        itemDetailMovement.value[index].proveedor_id = itemDetailMovement.value[index-1].proveedor_id
        itemDetailMovement.value[index].agricultor_id = itemDetailMovement.value[index-1].agricultor_id
    }
   
}

const onCalcItemDetail = (item, index:number) =>{


    let cantidad = parseFloat(itemDetailMovement.value[index].cantidad_envase)
    let peso_bruto = parseFloat(itemDetailMovement.value[index].peso_bruto)
    let peso_envase = parseFloat(itemDetailMovement.value[index].peso_envase)
    // let peso_balanza = parseFloat(itemDetailMovement.value[index].peso_balanza)


    itemDetailMovement.value[index].peso_neto = (peso_bruto - (cantidad * peso_envase)).toFixed(2)
    // itemDetailMovement.value[index].peso_neto_planta = (peso_balanza - (cantidad * peso_envase)).toFixed(2)
    
    let peso_neto=  parseFloat(itemDetailMovement.value[index].peso_neto.toString())
    
    itemDetailMovement.value[index].peso_promedio_jaba =  cantidad == 0 ? "0" : (peso_neto / cantidad).toFixed(2)
    
    
    let peso_guia = parseFloat(itemDetailMovement.value[index].peso_guia.toString())

    itemDetailMovement.value[index].diferencia_peso_guia = peso_guia - peso_neto
    let diferencia_peso_guia =  parseFloat(itemDetailMovement.value[index].diferencia_peso_guia.toString())


    itemDetailMovement.value[index].porcentaje = ((diferencia_peso_guia / peso_bruto) * 100).toFixed(2)

    

    onCalcItemDetail2()
}


const onCalcItemDetail2 = () =>{


    let suma_peson_neto=0

    for (let index=0; index < itemDetailMovement.value.length; index++){
        suma_peson_neto += parseFloat(itemDetailMovement.value[index].peso_neto)
    }

    detail.value.stock = suma_peson_neto

    let no_apta_tamanio = (detail.value.no_apta_tamanio ?? "").toString() == ""? 0 :  parseFloat((detail.value.no_apta_tamanio ?? "0").toString())
    let pasmado = (detail.value.pasmado ?? "").toString() == ""? 0 :  parseFloat((detail.value.pasmado ?? "0").toString())
    let sobre_maduro = (detail.value.sobre_maduro ?? "").toString() == ""? 0 :  parseFloat((detail.value.sobre_maduro ?? "0").toString())
    let pequenio = (detail.value.pequenio ?? "").toString() == ""? 0 :  parseFloat((detail.value.pequenio ?? "0").toString())
    let otros = (detail.value.otros ?? "").toString() == ""? 0 :  parseFloat((detail.value.otros ?? "0").toString())
    let merma_produccion = (detail.value.merma_produccion ?? "").toString() == ""? 0 :  parseFloat((detail.value.merma_produccion ?? "0").toString())



    let suma = no_apta_tamanio + pasmado + sobre_maduro + pequenio + otros + merma_produccion
    
    detail.value.stock_apto =detail.value.stock -  suma
}






const setPesoEnvase = (index) =>{

    let tipoenvase = optionTipoEnvase.value.filter((item: any) => parseInt(item.value) == parseInt(itemDetailMovement.value[index].tipo_envase_id))

    itemDetailMovement.value[index].peso_envase = tipoenvase.length > 0 ? tipoenvase[0].peso : 0
}

const minValidatorRespiracion = (value) => {
    return value > 0 || `Mayor que 0`
}

const minValidatorMayorCero = (value) => {
    return value >= 0 || `Mayor igual a 0`
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
                        DETALLE DE INGRESOS DE MATERIA PRIMA LOTE:  {{  itemMovement.documento }}
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
                                

                                :on-edit="onEdit"
                                :on-input="onInputed"
                                :icon-input="'tabler-eye'"

                                :id-select="idSelect"

                                no-deleted-first="true"
                                >
                                
                            </DataTableCustom>
                        </VCol>
                    </VRow>

                </VCard>
            </VCol>

            <VCol cols="12">
                <VCard>
                    <VCardTitle class="mb-3 mt-2">
                       
                        DETALLE DE LOTE 
                    </VCardTitle>

                    <VDivider />

                    <VCardText class="d-flex flex-wrap py-4 gap-4">

                        <div class="me-3" style="width: 80px;">
                            <VSelect v-model="rowPerPage" density="compact" variant="outlined"
                                :items="[10, 20, 30, 50]" />
                        </div>

                        <div class="me-3" style="width: 80px;">
                            <VBtn icon size="small" color="success" @click="listDataDetailLote">
                                <VIcon size="22" icon="tabler-analyze" />
                                <VTooltip activator="parent" location="end">
                                    Cargar Datos
                                </VTooltip>
                            </VBtn>
                        </div>


                      

                        <VSpacer />

                        <div class="app-user-search-filter d-flex align-center flex-wrap gap-4">

                            <div style="width: 30rem;">
                                <VTextField v-model="searchQueryDetailLote" :placeholder="'Buscar por ' + radioSearchDetailLote"
                                    density="compact" @input="searchQueryDetailLote = searchQueryDetailLote.toUpperCase()" />
                            </div>


                        </div>
                    </VCardText>

                    <VDivider />

                    <VRow>
                        <VCol cols="12">
                            <DataTableCustom 
                                :colums="columnsDetailLote"
                                :data="filterDataLoteDetalle"

                                
                                :on-col="onColSelectedDetail" 
                                :is-loading="isLoading" 
                                :search-query="searchQueryDetailLote"
                                
                                :row-per-page="rowPerPageDetailLote" 
                                :filters="filters" 
                                

                                >
                                
                            </DataTableCustom>
                        </VCol>
                    </VRow>

                </VCard>
            </VCol>

        </VRow>


        <VDialog
            v-model="dialog"
            max-width="1400"
            class="custom-dialog"
            persistent 
            no-click-animation 
        >   
            <VCard v-if="isLoadingDetailLote">
                <VCardText>
                    <div class="center_loader">
                        <VProgressCircular indeterminate color="secondary" />
                        <h3 style=" margin-top: 7px;color: #9b9b9b;">Cargando datos...</h3>
                    </div>
                </VCardText>

            </VCard>

            <VCard v-else>
                <VForm ref="refFormDialog" @submit.prevent="onSubmitCreateLote">
                    <VToolbar dense flat>
                        <VToolbarTitle>
                            {{ accion == 1 ? 'NUEVO LOTE DE INGRESO' : 'EDITAR LOTE: ' + ' ' + itemMovement.documento + '-' + detail.lote }}
                        </VToolbarTitle>
                        <VSpacer />
                    
                    
                        <VBtn v-if="dataLotesSalidas.length<=0"
                            color="primary"
                            prepend-icon="mdi-content-save"
                            type="submit"
                        >
                                GUARDAR
                        </VBtn>
                       
                        <div v-else style="color: #2bb82b;font-weight: bolder;">
                            LOTE CON SALIDAS
                        </div>
                        <VBtn
                            color="secondary"
                            prepend-icon="mdi-close-circle"
                            @click="dialog = false">
                            CANCELAR
                        </VBtn>

                    </VToolbar>
                    <VCardText>
                    
                        <VRow >

                            <VCol cols="6">
                                <VAutocomplete v-model="detail.variedad_id"  :rules="[requiredValidator]"   label="VARIEDAD" :items="optionVariedad"/>
                            </VCol>
                            <!-- <VCol cols="5">
                                <VAutocomplete v-model="detail.proveedor_centro_id"  :rules="[requiredValidator]" label="PROVEEDOR" clearable :items="optionProveedor" />
                            </VCol> -->
                            
                            <VCol v-if="accion==2" cols="3">
                                <VSelect v-model="detail.estado"  :rules="[requiredValidator]" label="ESTADO" :items="optionState" />
                            </VCol>
                            <VCol cols="3">
                                <VCheckbox  v-model="detail.inspeccion" label="Inspeccionar" @update:model-value="onCalcItemDetail2" :disabled="dataLotesSalidas.length>0" />
                            </VCol>

                          


                            <!-- <VCol :cols="6">
                                <VAutocomplete v-model="detail.agricultor_id" 
                                clearable :items="optionAgricultures"   label="AGRICULTOR*"/>

                            </VCol> -->

                          <!--   <VCol :cols="4">
                                <VAutocomplete v-model="detail.provincia_id"  :rules="[requiredValidator]" clearable 
                                :items="optionProvincia" label="PROCEDENCIA - PROVINCIA" />
                            </VCol>
                            <VCol :cols="5">
                                <VAutocomplete v-model="detail.distrito_id"  :rules="[requiredValidator]" clearable :items="optionDistrito" label="PROCEDENCIA - DISTRITO"  />
                            </VCol> -->
                          


                        </VRow>
                       
                        <VRow v-if="detail.inspeccion" class="mt-6">
                            <h5 class="mb-4 pl-3">Inspeccion</h5>
                            <VCol cols="12">
                                <VRow>
                                    <VCol cols="4">
                                        <VTextField v-model="detail.no_apta_tamanio"  :rules="[requiredValidator, minValidatorMayorCero]" @update:model-value="onCalcItemDetail2"   label="No Apta tamaño" type="number" :min="0"  suffix="KG"/>
                                    </VCol>
                                    <VCol cols="4">
                                        <VTextField v-model="detail.pasmado"  :rules="[requiredValidator, minValidatorMayorCero]" @update:model-value="onCalcItemDetail2" label="Pasmado"  type="number" :min="0"  suffix="KG"/>
                                    </VCol>
                                    <VCol cols="4">
                                        <VTextField v-model="detail.pequenio"  :rules="[requiredValidator, minValidatorMayorCero]" @update:model-value="onCalcItemDetail2" label="Pequeño"  type="number"  :min="0" suffix="KG" />
                                    </VCol>
                                    <VCol cols="4">
                                        <VTextField v-model="detail.sobre_maduro"  :rules="[requiredValidator, minValidatorMayorCero]" @update:model-value="onCalcItemDetail2" label="Sobre Maduro"  type="number" :min="0" suffix="KG"/>
                                    </VCol>
                                    <VCol cols="4">
                                        <VTextField v-model="detail.otros"  :rules="[requiredValidator, minValidatorMayorCero]" @update:model-value="onCalcItemDetail2" label="Otros"  type="number"  :min="0" suffix="KG" />
                                    </VCol>
                                
                                    
                                    <VCol cols="4">
                                        <AppDateTimePicker v-model="detail.fecha_inspeccion" label="Seleccionar Fecha"  class="date-time-picker"
                                            :config="{dateFormat: 'Y-m-d', allowInput: true, maxDate: new Date(), minDate: itemMovement.fecha}" 
                                            :rules="[requiredValidator]" />
                                    </VCol>
                                    
                                    <VCol cols="12">
                                        <VTextarea v-model="detail.observacion_inspeccion" label="Observacion*"  rows="2"   />
                                    </VCol>
                                
                                </VRow>
                            </VCol>
                          
                        </VRow>

                      
                        <VRow v-if="detail.inspeccion" class="mt-6">
                            <h5 class="mb-4 pl-3">Merma de Produccion</h5>
                            <VCol cols="12">
                                <VRow>
                                    <VCol cols="3">
                                        <VTextField v-model="detail.merma_produccion"  :rules="[requiredValidator, minValidatorMayorCero]" @update:model-value="onCalcItemDetail2"   label="Merma*" type="number" :min="0"  suffix="KG"/>
                                    </VCol>
                                    <VCol cols="9">
                                        <VTextarea v-model="detail.observacion_produccion"   label="Observacion*"  rows="2"  />
                                    </VCol>
                                    
                                
                                </VRow>
                            </VCol>
                          
                        </VRow>


    
                        <VRow justify="space-between">
                            
                            <VCol cols="12">
                                <br>

                                <VCardText class="d-flex flex-wrap py-4 gap-4">

                                    <div class="me-3" >
                                        <h5 class="mb-0">DETALLE DE LOTE</h5>
                                    </div>



                                    <VSpacer />

                                    <div class="app-user-search-filter d-flex align-center flex-wrap gap-4">

                                        <div>
                                            <h4 class="mb-0">Stock: {{ detail.stock.toFixed(2) }} </h4>
                                        </div>
                                        <div v-if="detail.inspeccion" >
                                            <h4 class="mb-0" > Stock Apto: {{ detail.stock_apto.toFixed(2) }} </h4>
                                        </div>



                                        <VBtn v-if="dataLotesSalidas.length<=0" repend-icon="tabler-plus" @click="onNewDetialMovement()" size="x-small">
                                            Agregar Detalle

                                        </VBtn>

   
                                    </div>
                                </VCardText>

                                <!-- <VRow justify="space-between">
                                    <VCol cols="3">
                                        <h5 class="mb-4">DETALLE DE LOTE</h5>
                                    </VCol>
                                    
                                    <VCol cols="6" class="text-right">

                                        <div>
                                            stock total: 0
                                        </div>

                                        <VBtn prepend-icon="tabler-plus" @click="onNewDetialMovement()" size="x-small">
                                            Agregar Detalle
                                        </VBtn>
                                       
                                    </VCol>
                                </VRow> -->

                                <VDivider />
                                <VRow>
                                    <VCol cols="12" class="mt-3" >
                                        <div>
                                            <ul class="list-group list-detail">

                                                
                                                <li class="list-detail-column">
                                                    <div>
                                                        <div class="title pb-2">ACCION</div>
                                                        <div>
                                                            <ul>
                                                                
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">

                                                                    <VBtn v-if="index >0 && accion==1"  icon size="x-small" color="error" @click="deleteItemDetail(item, index)" >
                                                                        <VIcon size="22" icon="tabler-trash" />
                                                                    </VBtn>
                                                                    <VBtn v-else-if = "item.id == null && accion==2"  icon size="x-small" color="error" @click="deleteItemDetail(item, index)" >
                                                                        <VIcon size="22" icon="tabler-trash" />
                                                                    </VBtn>
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>

                                                
                                                <li class="list-detail-column">
                                                    <div class="col-guia">
                                                        <div class="title pb-2">GUIA REMICION</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField v-model="itemDetailMovement[index].guia_remicion"  :rules="[requiredValidator]" 
                                                                    @input="itemDetailMovement[index].guia_remicion = itemDetailMovement[index].guia_remicion.toUpperCase()" 
                                                                    />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>

                                                <li class="list-detail-column">
                                                    <div class="col-guia">
                                                        <div class="title pb-2">GUIA TRANSPORTISTA*</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <!-- <VTextField type="text"  v-model="itemDetailMovement[index].destino"   
                                                                    @input="itemDetailMovement[index].destino = itemDetailMovement[index].destino.toUpperCase()" /> -->

                                                                    <VTextField v-model="itemDetailMovement[index].guia_transportista"  
                                                                        @input="itemDetailMovement[index].guia_transportista= itemDetailMovement[index].guia_transportista.toUpperCase()" 
                                                                        />

                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>


                                                <li class="list-detail-column">
                                                    <div class="col-provincia">
                                                        <div class="title pb-2">PROVINCIA</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <!-- <VTextField type="text"  v-model="itemDetailMovement[index].guia_transportista"  :rules="[requiredValidator]"/> -->
                                                                    <VAutocomplete v-model="itemDetailMovement[index].provincia_id"  :rules="[requiredValidator]" clearable 
                                                                    :items="optionProvincia" @update:model-value="setDistritos(index)"   />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                              
                                                <li class="list-detail-column">
                                                    <div class="col-provincia">
                                                        <div class="title pb-2">DISTRITO</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <!-- <VTextField type="text"  v-model="itemDetailMovement[index].guia_transportista"  :rules="[requiredValidator]"/> -->
                                                                    <VAutocomplete v-model="itemDetailMovement[index].distrito_id"  :rules="[requiredValidator]" clearable 
                                                                    :items="itemDetailMovement[index].distritos"  />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>

                                               

                                                <li class="list-detail-column">
                                                    <div class="col-proveedor">
                                                        <div class="title pb-2">PROVEEDOR</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <!-- <VTextField type="text"  v-model="itemDetailMovement[index].destino"   
                                                                    @input="itemDetailMovement[index].destino = itemDetailMovement[index].destino.toUpperCase()" /> -->

                                                                    <VAutocomplete v-model="itemDetailMovement[index].proveedor_id"  :rules="[requiredValidator]"
                                                                    clearable :items="optionProveedor" />

                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div class="col-proveedor">
                                                        <div class="title pb-2">AGRICULTOR</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                   <!--  <VTextField type="text"  v-model="itemDetailMovement[index].destino"   
                                                                    @input="itemDetailMovement[index].destino = itemDetailMovement[index].destino.toUpperCase()" /> -->

                                                                    <VAutocomplete v-model="itemDetailMovement[index].agricultor_id" 
                                                                    clearable :items="optionAgricultures"/>
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>


                                                <li class="list-detail-column">
                                                    <div class="col-kilos">
                                                        <div class="title pb-2">DESTINO</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="text"  v-model="itemDetailMovement[index].destino"   
                                                                    @input="itemDetailMovement[index].destino = itemDetailMovement[index].destino.toUpperCase()" />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>


                                                <li class="list-detail-column">
                                                    <div class="col-kilos">
                                                        <div class="title pb-2">PESO_GUIA</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"  v-model="itemDetailMovement[index].peso_guia"  :rules="[requiredValidator]" @update:model-value="onCalcItemDetail(item, index)" />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>

                                                
                                                <li class="list-detail-column col-tipo-envase">
                                                    <div class="col-tipo-envase">
                                                        <div class="title pb-2">TIPO_ENVASE</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <VAutocomplete  v-model="itemDetailMovement[index].tipo_envase_id"  :rules="[requiredValidator]" label="Tipo Envase" :items="optionTipoEnvase" @update:model-value="setPesoEnvase(index); onCalcItemDetail(item, index)"/>
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div class="col-kilos">
                                                        <div class="title pb-2">PESO_ENVASE</div>
                                                        <div >
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number" disabled v-model="itemDetailMovement[index].peso_envase"  :rules="[requiredValidator]"/>
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                              
                                                <li class="list-detail-column">
                                                    <div class="col-kilos">
                                                        <div class="title pb-2">CANTIDAD_ENVASE</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"  v-model="itemDetailMovement[index].cantidad_envase"  :rules="[requiredValidator]" @update:model-value="onCalcItemDetail(item, index)" />
                                                                </li>

                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                               
                                                <li class="list-detail-column">
                                                    <div class="col-kilos">
                                                        <div class="title pb-2">PESO_BRUTO</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"  v-model="itemDetailMovement[index].peso_bruto"   :rules="[requiredValidator, minValidatorRespiracion]" @update:model-value="onCalcItemDetail(item, index)" />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                
                                               <!--  <li class="list-detail-column">
                                                    <div>
                                                        <div class="title pb-2">PESO_BALANZA</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"   v-model="itemDetailMovement[index].peso_balanza"   :rules="[requiredValidator, minValidatorRespiracion]" @update:model-value="onCalcItemDetail(item, index)" />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li> -->
                                                <li class="list-detail-column">
                                                    <div class="col-kilos">
                                                        <div class="title pb-2">PESO_NETO</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField  type="number" disabled v-model="itemDetailMovement[index].peso_neto"  :rules="[requiredValidator]" />
                                                                </li>
                                                               
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                
                                                <li class="list-detail-column">
                                                    <div class="col-kilos">
                                                        <div class="title pb-2">PESO_PROMEDIO_JABA</div>
                                                        <div>
                                                            <ul>
                                                                <li  v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField  type="number" disabled v-model="itemDetailMovement[index].peso_promedio_jaba"  :rules="[requiredValidator]" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                
                                                <li class="list-detail-column">
                                                    <div class="col-kilos">
                                                        <div class="title pb-2">DIFERENCIA_PESO_GUIA</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number" disabled v-model="itemDetailMovement[index].diferencia_peso_guia"   :rules="[requiredValidator]" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div class="col-porcentaje">
                                                        <div class="title pb-2">PORCENTAJE</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number" disabled v-model="itemDetailMovement[index].porcentaje"   :rules="[requiredValidator]" suffix="%" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                            
                                               
                                                
                                             
                                            </ul>
                                          
                                        </div>
                                        
                                    </VCol>

                                </VRow>

                            </VCol>
                           
                        </VRow>

                    
                        
                        
                        
                    </VCardText>
                    
                    
                </VForm>    
            </VCard>
        </VDialog>

        <!-- 
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

                        <VForm ref="refForm"  @submit.prevent="onSubmitEdit">
                            <VRow>
                                <VCol v-if="accion==2" cols="12">
                                    <VTextField type="text" readonly v-model="detail.serie_lote"  :rules="[requiredValidator]" label="LOTE"/>

                                </VCol>
                             
                                <VCol cols="12">
                                    <VAutocomplete v-model="detail.variedad_id"  :rules="[requiredValidator]"   label="VARIEDAD" :items="optionVariedad"/>
                                </VCol>

                                <VCol cols="12">

                                    <VAutocomplete v-model="detail.proveedor_centro_id"  :rules="[requiredValidator]" clearable :items="optionProveedor" label="PROVEEDOR" />
                                </VCol>

                                <VCol  cols="12">
                                    <VCheckbox v-model="detail.inspeccion"  label="Inspeccionar" />
                                </VCol>

                                <template v-if="detail.inspeccion">
                                    <VCol  cols="12">
                                        <VTextField type="number" v-model="detail.no_apta_tamanio"  :rules="[requiredValidator]" label="Fruta no apta por tamaño" />
                                    </VCol>
                                    <VCol  cols="12">
                                        <VTextField type="number" v-model="detail.pasmado"  :rules="[requiredValidator]" label="Pasamado" />
                                    </VCol>
                                    <VCol  cols="12">
                                        <VTextField type="number" v-model="detail.sobre_maduro"  :rules="[requiredValidator]" label="Sobre Moduro" />
                                    </VCol>

                                    <VCol  cols="12">
                                        <VTextField type="number" v-model="detail.pequenio"  :rules="[requiredValidator]" label="Pequeño" />
                                    </VCol>
                                    <VCol cols="12">
                                        <VTextField type="number" v-model="detail.otros"  :rules="[requiredValidator]" label="Otros" />
                                    </VCol>
                                </template>
                                

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
        </VNavigationDrawer> -->

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

.col-variedad {
  inline-size: 350px;
}

.col-provincia {
  inline-size: 320px;
}

.col-distrito {
  inline-size: 320px;
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

.center_loader {
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>

<route lang="yaml">
meta:
    action: manage
    subject: packing_detalle_ingresos
</route>
