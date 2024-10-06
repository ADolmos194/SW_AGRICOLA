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
let radioSearch = ref('fecha')
let isDrawerVisible = ref(false)
let accion = ref(1)
const refForm = ref(null);

let filters = ref([])

let isLoadingIngresoInspeccion = ref(false)



let state_placa= ref(false)

// let isLoadingDetail = ref(false)
// let searchQueryDetail = ref('')
// let rowPerPageDetail = ref(10)
// let filtersDetail = ref([])
// let radioSearchDetail = ref('lote')

let dialog = ref(false)


let columns = ref([


    { key: "fecha", name: "fecha", order: true, search: true, class: 'text-center' },
    { key: "documento", name: "Lote", order: true, search: true, class: 'text-center' },
    { key: "clase_movimiento", name: "Clase Movimiento", order: true, search: true, class: 'text-center' },
    { key: "tipodocumento", name: "Tipo Documento", order: true, search: true, class: 'text-center' },
    { key: "campania", name: "campaña", order: true, search: true, class: 'text-center' },
    { key: "centro", name: "centro", order: true, search: true, class: 'text-center' },
    { key: "almacen", name: "almacen", order: true, search: true, class: 'text-center' },
    { key: "subgrupo", name: "Categoria", order: true, search: true, class: 'text-center' },
    { key: "vehiculo", name: "vehiculo", order: true, search: true, class: 'text-center' },
    { key: "transportista", name: "transportista", order: true, search: true, class: 'text-center' },
    { key: "fecha_creacion", name: "fecha_creacion", order: true, search: true, class: 'text-center' },

    // { key: "procedencia", name: "procedencia", order: true, search: true, class: 'text-center' },
    // { key: "guia_remicion", name: "guia remicion", order: true, search: true, class: 'text-center' },
    // { key: "guia_transportista", name: "guia transportista", order: true, search: true, class: 'text-center' },
    // { key: "proveedor", name: "proveedor", order: true, search: true, class: 'text-center' },
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
let dataDetail = ref([])
let listDetailMovement = ref([])


let selectedItems = ref([])

let listYear = []
let listCenter = []
let listWarehouse = ref([])
let listTypeMov=ref([])
let listTypeDoc=ref([])
let listIngresoInspeccionState= ref([])

// let listDepartamento=ref([])
// let listProvincia=ref([])
// let listDepartamentoCenter=ref([])
// let listDistritoCenter=ref([])

let listProvinciaCenter=ref([])
let listDistrito=ref([])

let listProveedor=ref([])
let listTransportista=[]
let listAgricultores=ref([])
let config_almacen_subgrupo=ref([])

let listTipoEnvase=[]
let listVariedad=[]




let optionYear = ref([])
// let optionSociety = ref([])
let optionCenter = ref([])
let optionState = ref([
    { value: 1, title: 'Activo' },
    { value: 2, title: 'Inactivo' },
])
let optionTypeInput= ref([
    { value: "I", title: 'Ingreso' },
    { value: "S", title: 'Salida' },
])

// let optionDepartamento = ref([])

let optionProvincia = ref([])

let optionProveedor = ref([])
let optionTransportista = ref([])
let optionAgricultures = ref([])
let optionTipoEnvase = ref([])
let optionVariedad = ref([])
// let option_config_almacen_subgrupo = ref([])


let typeInput= ref('I')
let typeMov= ref(null)
let typeDoc= ref(null)

let departamento= ref(null)
let provincia= ref(null)
let distrito= ref(null)
let vehiculo= ref(null)
let transportista= ref(null)
let guia_transportista= ref(null)
let config_almacen_subgrupo_id= ref(null)

let guia_remicion= ref(null)

// let society_id = ref(null)

let year_id = ref(null)
let center_id = ref(null)
let warehouse_id = ref(null)
let dateEntry = ref(null)
let state_id = ref(null)
let id = ref(null)

let documento_correlativo = ref(null)



let isSnackbarVisible = ref(null)
let titleSnackbar = ref(null)
let stateSnackbar = ref(null)




const optionWareHouse = computed(() => {
    return listWarehouse.value.filter((item: any) => parseInt(item.centro_id) == parseInt(center_id.value ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.almacen} - ${item.subgrupo}`.toUpperCase(),
            almacen_id: item.almacen_id,
            subgrupo_id: item.subgrupo_id
        };
    });
});


let option_config_almacen_subgrupo = computed(() => {
    return config_almacen_subgrupo.value.filter((item: any) => parseInt(item.almacensubgrupo_id) == parseInt(warehouse_id.value ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.clase_movimiento} ${item.tipomovimiento} - ${item.tipodocumento}`.toUpperCase(),
            almacensubgrupo_id: item.almacensubgrupo_id,
            tipodocumento_id: item.tipodocumento_id,
            tipomovimiento_id: item.tipomovimiento_id,
        };
    });
});


// let optionTypeMov = computed(() => {
//     return listTypeMov.value.filter((item: any) => item.tipomov == (typeInput.value ?? '')).map((item: any) => {
//         return {
//             value: item.id,
//             title: `${item.nombre}`.toUpperCase(),
//         };
//     });
// });

// let optionTypeDoc = computed(() => {
//     return listTypeDoc.value.filter((item: any) => item.tipodoc == (typeInput.value ?? '')).map((item: any) => {
//         return {
//             value: item.id,
//             title: `${item.nombre}`.toUpperCase(),
//         };
//     });
// });


/* let optionProvincia = computed(() => {
    return listProvinciaCenter.value.filter((item: any) => item.centro_id == (center_id.value ?? '')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.departamento} - ${item.descripcion}`.toUpperCase(),
            departamento_id: item.departamento,
        };
    });
});
 */
/* 
let optionDistrito = computed(() => {
    return listDistritoCenter.value.filter((item: any) => parseInt(item.provincia_id) == parseInt(provincia.value ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.cod} - ${item.descripcion}`.toUpperCase(),
            distrito_id: item.id,
            provincia_id: item.provincia_id,
        };
    });
});

 */
/* 
let optionProveedor  = computed(() => {  
    return listProveedor.value.filter((item: any) => parseInt(item.centro_id) == parseInt(center_id.value ?? '0')).map((item: any) => {
    return {
        value: item.id,
        title: `${item.ruc} - ${item.nombre}`.toUpperCase(),
        proveedor_id: item.proveedor_id,
    };
}); */



let itemMovement = ref({
    id: 0,
    // distrito_centro_id: 1,
    // distrito_id: 224,
    // distrito: "",
    // provincia_id: 25,
    // provincia: "",
    // departamento_id: 2,
    // departamento: "",
    // procedencia: "",
    almacen_mov_doc_subgrupo_id: null,
    almacen_subgrupo_id: null,
    almacen_id: null,
    almacen: "",
    subgrupo_id: null,
    subgrupo: "",
    centro_id: null,
    centro: "",
    // guida_remicion: "",
    fecha: "",
    // proveedor_centro_id: 1,
    // proveedor_id: 1,
    // proveedor: "",
    // vehiculo_id: null,
    vehiculo: "",
    transportista_id: null,
    transportista: "",
    campania_id: null,
    campania: 2024,
    inspeccion: false,
    estado: 1
})

let detail = {
    id: 1,
    movimiento_id: 1,
    lote: "",
    sublote: "",
    grupo_id: 1,
    grupo: "",
    subgrupo_id: 1,
    subgrupo: "",
    cultivo_id: 1,
    cultivo: "",
    variedad_id: null,
    variedad: "",

    tipo_envase_id: null,
    tipo_envase: "",
    peso_envase: 0,
    cantidad_envase: 1,
    peso_bruto: 0,
    peso_guia: 0,
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
    guia_transportista: '',
    inspection: false,
    no_apta: 0,
    pasmado: 0,
    sobre_maduro: 0,
    pequenio: 0,
    otros: 0,

    provincia_centro_id: null,
    distrito_id: null,
    distrito: "",
    distritos:[],
    provincia_id: null,
    provincia: "",
    departamento_id: null,
    departamento: "",
    procedencia: "",
    disabled: false,
    guia_tranportista: "",
    agricultor_id: null,
    agricultor: "",
    destino: "",
}


let itemDetailMovement = ref([])
let optionGrupoLote = ref([])

onMounted(() => {

    // packingPlant =  JSON.parse(localStorage.getItem('packing_plant') ?? JSON.stringify(packingPlant))

    listData()

    // getListTypeMov()
    // getListTypeDoc()
    getListConfigAlmaceSubGrupo()

    getListYear()
    getListCenter()
    getListWarehouse()
    
    // getListDepartamento()
    getListProvincia()
    getListDistrito()

    getListProveedor()
    getListTransportistas()

    getListTipoEnvase()
    getListVariedad()

    getListAgricultos()

    /*  
     getListSociety()
     getListCrop() */

})


// let optionCenter = computed(() => {
//     return listCenter.value.filter((item: any) => parseInt(item.sociedadpais) == parseInt(society_id.value ?? '0')).map((item: any) => {
//         return {
//             value: item.id,
//             title: `${item.abreviatura} - ${item.nombre}`.toUpperCase(),
//         };
//     });
// });




const listData = async (idselect = 0) => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/ingreso/1-2`,
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            data.value = response.data.data

            id.value = idselect

            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}




const getListTypeMov = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/tipomovimiento/1`,
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listTypeMov.value = response.data.data
            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    }
}

const getListTypeDoc = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/tipodocumento/1`,
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listTypeDoc.value = response.data.data
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
        listCenter = response.data.data

        optionCenter.value = listCenter.map((item: any) => {
            return {
                value: item.id,
                title: `${item.abreviatura} - ${item.nombre}`.toUpperCase(),
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



const getListWarehouse = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/almacen/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listWarehouse.value = response.data.data
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
            
            listProvinciaCenter.value = response.data.data
            
           /*  optionProvincia.value = listProvincia.map((item: any) => {
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


const getListProveedor = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/proveedor/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listProveedor.value = response.data.data
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

const getListTransportistas = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/transportista/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listTransportista = response.data.data
            
            optionTransportista.value = listTransportista.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.ruc} - ${item.nombre}`,
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

const getListAgricultos = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/agricultores/1`,
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listAgricultores.value = response.data.data
            
           /*  optionAgricultures.value = listAgricultores.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.ruc == null ? '': item.ruc.toString() + "-" } ${item.nombre}`,
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

/* const getTransportista = () =>{

    let filterTransportista = listTransportista.filter((item: any) => parseInt(item.id) == parseInt(vehiculo.value ?? '0'))
    
    transportista.value =filterTransportista.length > 0 ? `${filterTransportista[0].ruc} - ${filterTransportista[0].proveedor}` : ""
} */


const getListConfigAlmaceSubGrupo = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/config-almacen-subgrupo/1/I",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            config_almacen_subgrupo.value = response.data.data

           
            
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
        url: "/variedad/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listVariedad = response.data.data

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

    await getListIngresoInspeccionState(item.id)


    year_id.value = item.campania_id
    center_id.value = item.centro_id

    centerFilters()


    warehouse_id.value = item.almacen_subgrupo_id
    config_almacen_subgrupo_id.value= item.almacen_mov_doc_subgrupo_id
    dateEntry.value = item.fecha
    guia_remicion.value= item.guia_remicion



    departamento.value= item.departamento_id
    provincia.value= item.provincia_id
    distrito.value= item.distrito_centro_id
    vehiculo.value= item.vehiculo
    transportista.value= item.transportista_id
    guia_transportista.value= item.guia_transportista

    documento_correlativo.value= item.documento


    state_id.value = item.estado


    itemDetailMovement.value= []
    optionGrupoLote.value= []



}

const getListIngresoInspeccionState = async (id) => {

    // isLoading.value = true
    isLoadingIngresoInspeccion.value = true

    const config = {
        method: "get",
        url: `/ingreso-inspeccion-state/${id}`,
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listIngresoInspeccionState.value = response.data.data
            
           
            // isLoading.value = false

        } else {
            // isLoading.value = false;
        }
    } catch (error) {
        // isLoading.value = false;
    }finally{
        isLoadingIngresoInspeccion.value = false
    }
}

const onNew = () => {
    accion.value = 1

    dialog.value = true

    // isDrawerVisible.value = true

    if (refForm.value != null)
        refForm.value.reset();

    id.value = null
    year_id.value = null
    center_id.value = null
    warehouse_id.value = null
    config_almacen_subgrupo_id.value= null
    dateEntry.value = moment().format('YYYY-MM-DD')
    guia_remicion.value= null

    isLoadingIngresoInspeccion.value = false

    listIngresoInspeccionState.value= []



    departamento.value= null
    provincia.value= null
    distrito.value= null
    vehiculo.value= null
    transportista.value= null
    guia_transportista.value= null
    documento_correlativo.value= null


    itemDetailMovement.value= []
    optionGrupoLote.value= []

    state_placa.value = false

    onNewDetialMovement()


}


const onSubmit = async () => {

    valuePlcata()

    if (!state_placa.value) return;


    if ((dateEntry.value ?? "").toString().length <=0) {
        messagePopup('warning', 'Fecha de ingreso es requerido')
        return
    }

    const isValid = await refForm.value.validate();
    if (!isValid.valid) return;


    

    isSnackbarVisible.value = false

    let details = []

    for (let item of itemDetailMovement.value){

        let detail = {
            guia_remicion: item.guia_remicion,
            guia_transportista: item.guia_transportista,
            distrito_id: item.distrito_id,

            variedad: item.variedad_id,
            tipo_envase: item.tipo_envase_id,
            cantidad_envase: item.cantidad_envase,
            peso_envase: item.peso_envase,

            peso_guia: item.peso_guia,
            peso_bruto: item.peso_bruto,
            peso_neto: item.peso_neto,
            // peso_balanza: item.peso_balanza,
            
            peso_promedio_jaba: item.peso_promedio_jaba,
            diferencia_peso_guia: item.diferencia_peso_guia,
            porcentaje: item.porcentaje,
            
            proveedor: item.proveedor_centro_id,
            agricultor_id: item.agricultor_id,
            destino: item.destino,
            grupo_lote: item.gruposublote,
            inspection: item.inspection,
            fruta_no_apta: item.no_apta,         
            pasmado: item.pasmado,
            sobre_maduro: item.sobre_maduro,
            pequenio: item.pequenio,
            otros: item.otros
        }

        details.push(detail)

    }

    


    let data = {
        fecha: dateEntry.value,
        campania: year_id.value,
        vehiculo: vehiculo.value.toString().toUpperCase(),
        transportista: transportista.value,
        almance_mov_doc: config_almacen_subgrupo_id.value,
        estado: accion.value == 1 ? 1 : state_id.value,
        details: details
        // guia_transportista: guia_transportista.value,
        // guia_remicion: guia_remicion.value,
        // distrito_centro: distrito.value,
    }

    console.log(data);
    
    


    const config = {
        method: accion.value == 1?  "post": "put",
        url:  accion.value == 1? "/ingreso/create/": "/ingreso/update/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            isDrawerVisible.value = false
            
            listData(response.data.data.id)
            stateSnackbar.value = 'success'
            titleSnackbar.value = accion.value == 1 ? 'Registro creado con exito' : 'Registro actualizado con exito'
            dialog.value = false
            refForm.value.reset();

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
        isDrawerVisible.value = false
        dateEntry.value = false

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

        if (error.response.status == 409) {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = error.response.data.message_user

        } else {
            stateSnackbar.value = 'danger'
            titleSnackbar.value = 'Error al eliminar el registro'
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

const downloadExcelDetail = async () => {

    const config = {
        method: "post",
        maxBodyLength: Infinity,
        url: "/ingreso-detalle/download-excel/",
        headers: { 'Content-Type': 'multipart/form-data', },
        responseType: 'arraybuffer'
    };


    try {
        const response = await axios(config);

        if (response.status == 200) {
            const fileURL = window.URL.createObjectURL(new Blob([response.data]));

            const fileLink = document.createElement('a');
            fileLink.href = fileURL;
            fileLink.setAttribute('download', "ingresos-detallado.xlsx");
            document.body.appendChild(fileLink);
            fileLink.click();

        }
    } catch (error) {
        console.log("error ");
    }
}


const centerFilters = () => {


    warehouse_id.value= null
    config_almacen_subgrupo_id.value= null
    departamento.value= null
    provincia.value= null
    distrito.value= null

    

    // listDistritoCenter.value =  listDistrito.value.filter((item: any) => parseInt(item.centro_id) == parseInt(center_id.value ?? '0'))

    optionProvincia.value = listProvinciaCenter.value.filter((item: any) => item.centro_id == (center_id.value ?? '')).map((item: any) => {
            return {
                value: item.id,
                title: `${item.departamento} - ${item.descripcion}`.toUpperCase(),
                departamento_id: item.departamento,
            };
        });

    optionProveedor.value  = listProveedor.value.filter((item: any) => parseInt(item.centro_id) == parseInt(center_id.value ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.ruc == null ? '': item.ruc.toString()} - ${item.nombre}`.toUpperCase(),
            proveedor_id: item.proveedor_id,
        }
    })
 
    optionAgricultures.value  = listAgricultores.value.filter((item: any) => parseInt(item.centro_id) == parseInt(center_id.value ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.codigo == null ? '': item.codigo.toString() + " /"} ${item.nombre}`.toUpperCase(),
            proveedor_id: item.proveedor_id,
        }
    })
    


   /*  let filterProvincia = []

    for (let item of listDistritoCenter.value){
        for (let prov of listProvincia.value){
            if (parseInt(item.provincia_id) == parseInt(prov.id)){
                filterProvincia.push(prov)
                break
            }
        }
    } */

  /*   let filterProvinciaid= 0
    listProvinciaCenter.value= []

    for (let item of filterProvincia){
        if (parseInt(item.id) != filterProvinciaid){
            filterProvinciaid = parseInt(item.id)
            listProvinciaCenter.value.push(item)
        }
    }


    let filterDepartamento = []

    for (let item of listProvinciaCenter.value){
        for (let dep of listDepartamento.value){
            if (parseInt(item.departamento) == parseInt(dep.id)){
                filterDepartamento.push(dep)
                break
            }
        }
    }

    let filterDepartamentoid= 0
    listDepartamentoCenter.value=[]

    for (let item of filterDepartamento){
        if (parseInt(item.id) != filterDepartamentoid){
            filterDepartamentoid = parseInt(item.id)
            listDepartamentoCenter.value.push(item)
        }
    }

    optionDepartamento.value = listDepartamentoCenter.value.map((item: any) => {
        return {
            value: item.id,
            title: `${item.cod} - ${item.descripcion}`.toUpperCase(),
            pais_id: item.pais,
        };
    });
 */

}

/* 
const changeConfigAlmacenSubGrupo = () => {
    
    let list =  config_almacen_subgrupo.filter((item: any) => parseInt(item.almacensubgrupo_id) == parseInt(warehouse_id.value ?? '0') && parseInt(item.tipodocumento_id) == parseInt(typeDoc.value ?? '0') && parseInt(item.tipomovimiento_id) == parseInt(typeMov.value ?? '0'))

    config_almacen_subgrupo_id.value = list.length > 0 ? list[0].id : null

} */

const changeSubGrupo = () => {
    
    let list =  listWarehouse.value.filter((item: any) => parseInt(item.id) == parseInt(warehouse_id.value))


    let id_subgrupo  = list.length > 0 ? list[0].subgrupo_id : 0

    optionVariedad.value = listVariedad.filter((item: any) => parseInt(item.subgrupo_id) == id_subgrupo).map((item: any) => {
        return {
            value: item.producto_id,
            title: `${item.abr_cultivo} - ${item.producto}`.toUpperCase(),
        };
    });

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

    itemDetailMovement.value.push({...detail})
    // optionGrupoLote.value = []

    let index = itemDetailMovement.value.length - 1
    let cont=itemDetailMovement.value.length


    itemDetailMovement.value[index].id = cont
    itemDetailMovement.value[index].gruposublote = cont
    
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
        itemDetailMovement.value[index].proveedor_centro_id = itemDetailMovement.value[index-1].proveedor_centro_id
        itemDetailMovement.value[index].agricultor_id = itemDetailMovement.value[index-1].agricultor_id
    }

    optionGrupoLote.value.push(cont)



  /*   for (let index=0; index < itemDetailMovement.value.length; index++){

        cont++
        optionGrupoLote.value.push(cont)
    } */
   
}

const onCalcItemDetail = (item, index:number) =>{


    let cantidad = parseFloat(itemDetailMovement.value[index].cantidad_envase)
    let peso_bruto = parseFloat(itemDetailMovement.value[index].peso_bruto)
    let peso_envase = parseFloat(itemDetailMovement.value[index].peso_envase)
    // let peso_balanza = parseFloat(itemDetailMovement.value[index].peso_balanza)


    itemDetailMovement.value[index].peso_neto = (peso_bruto - (cantidad * peso_envase)).toFixed(2)
    // itemDetailMovement.value[index].peso_neto_planta = (peso_balanza - (cantidad * peso_envase)).toFixed(2)
    
    let peso_neto=  parseFloat(itemDetailMovement.value[index].peso_neto.toString())
    
    itemDetailMovement.value[index].peso_promedio_jaba = cantidad == 0 ? "0" :  (peso_neto / cantidad).toFixed(2)
    
    
    let peso_guia = parseFloat(itemDetailMovement.value[index].peso_guia.toString())

    itemDetailMovement.value[index].diferencia_peso_guia = peso_guia - peso_neto
    
    let diferencia_peso_guia =  parseFloat(itemDetailMovement.value[index].diferencia_peso_guia.toString())


    itemDetailMovement.value[index].porcentaje = ((diferencia_peso_guia / peso_bruto) * 100).toFixed(2)
}

const setPesoEnvase = (index) =>{

    let tipoenvase = optionTipoEnvase.value.filter((item: any) => parseInt(item.value) == parseInt(itemDetailMovement.value[index].tipo_envase_id))

    itemDetailMovement.value[index].peso_envase = tipoenvase.length > 0 ? tipoenvase[0].peso : 0
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

const  setGrupoLote = (index) =>{


    let grupo = itemDetailMovement.value[index].gruposublote

    let index_grupo = itemDetailMovement.value.findIndex((item: any) => parseInt(item.gruposublote) == parseInt(grupo) && parseInt(item.id) != parseInt(itemDetailMovement.value[index].id))

    if (index_grupo != -1){
        // itemDetailMovement[index].gruposublote = itemDetailMovement.value.length.toString()

        itemDetailMovement.value[index].guia_remicion =itemDetailMovement.value[index_grupo].guia_remicion
        itemDetailMovement.value[index].guia_transportista =itemDetailMovement.value[index_grupo].guia_transportista
        itemDetailMovement.value[index].provincia_id = itemDetailMovement.value[index_grupo].provincia_id

        itemDetailMovement.value[index].distritos = listDistrito.value.filter((item: any) => parseInt(item.provincia_id) == parseInt(itemDetailMovement.value[index].provincia_id ?? '0')).map((item: any) => {
            return {
                value: item.id,
                title: `${item.cod} - ${item.descripcion}`.toUpperCase(),
                distrito_id: item.id,
                provincia_id: item.provincia_id,
            };
        })

        itemDetailMovement.value[index].distrito_id = itemDetailMovement.value[index_grupo].distrito_id
        itemDetailMovement.value[index].variedad_id = itemDetailMovement.value[index_grupo].variedad_id
        itemDetailMovement.value[index].proveedor_centro_id = itemDetailMovement.value[index_grupo].proveedor_centro_id
        itemDetailMovement.value[index].agricultor_id = itemDetailMovement.value[index_grupo].agricultor_id
        itemDetailMovement.value[index].disabled=true
        
        
    }else{
        itemDetailMovement.value[index].disabled=false

    }

}

const  setGrupoLoteValues = (index_grupo) =>{


    let grupo = itemDetailMovement.value[index_grupo].gruposublote

    // let index_grupo = itemDetailMovement.value.findIndex((item: any) => parseInt(item.gruposublote) == parseInt(grupo) && parseInt(item.id) != parseInt(itemDetailMovement.value[i].id))

    if (index_grupo != -1){
        // itemDetailMovement[index].gruposublote = itemDetailMovement.value.length.toString()
        // buscar todos los que tienen el mismo grupo y copiar los valores
        for (let index=0; index < itemDetailMovement.value.length; index++){
            if (parseInt(itemDetailMovement.value[index].gruposublote) == parseInt(grupo) && index != index_grupo){
                //itemDetailMovement.value[index].guia_remicion =itemDetailMovement.value[index_grupo].guia_remicion.toString().toUpperCase()
                //itemDetailMovement.value[index].guia_transportista =itemDetailMovement.value[index_grupo].guia_transportista.toString().toUpperCase()
                //itemDetailMovement.value[index].provincia_id = itemDetailMovement.value[index_grupo].provincia_id

               /*  itemDetailMovement.value[index].distritos = listDistrito.value.filter((item: any) => parseInt(item.provincia_id) == parseInt(itemDetailMovement.value[index].provincia_id ?? '0')).map((item: any) => {
                    return {
                        value: item.id,
                        title: `${item.cod} - ${item.descripcion}`.toUpperCase(),
                        distrito_id: item.id,
                        provincia_id: item.provincia_id,
                    };
                }) */

               // itemDetailMovement.value[index].distrito_id = itemDetailMovement.value[index_grupo].distrito_id
                itemDetailMovement.value[index].variedad_id = itemDetailMovement.value[index_grupo].variedad_id
                // itemDetailMovement.value[index].proveedor_centro_id = itemDetailMovement.value[index_grupo].proveedor_centro_id
                // itemDetailMovement.value[index].agricultor_id = itemDetailMovement.value[index_grupo].agricultor_id
                // itemDetailMovement.value[index].disabled=true
            }
        }    
    // }else{
    //     itemDetailMovement.value[i].disabled=false

    }

}


const minValidatorRespiracion = (value) => {
    return value > 0 || `Mayor que 0`
}

const valuePlcata = () =>{

    if (vehiculo.value == null || vehiculo.value.toString().length < 7){
        state_placa.value= false
    }else{
        state_placa.value= true

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
                        
                        INGRESOS DE MATERIA PRIMA
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


                        <!-- <div class="me-3">

                            <VBtn color="secondary"
                                :to="{ name: 'proyswarm-prospeccioncentropoblados-prospeccion_centro_poblado_updatemasivo' }">
                                Actualizacion Masiva de Empadronamiento
                            </VBtn>
                        </div>  -->

                        <VSpacer />

                        <div class="app-user-search-filter d-flex align-center flex-wrap gap-4">

                            <div style="width: 30rem;">
                                <VTextField v-model="searchQuery" :placeholder="'Buscar por ' + radioSearch"
                                    density="compact" @input="searchQuery = searchQuery.toUpperCase()" />
                            </div>



                            <VBtn prepend-icon="tabler-plus" @click="onNew()">
                                Nuevo
                            </VBtn>

                            <VBtn variant="tonal" color="secondary" prepend-icon="tabler-screen-share"
                                @click="downloadExcel()">
                                Exportar
                            </VBtn>
                            <VBtn variant="tonal" color="secondary" prepend-icon="tabler-screen-share"
                                @click="downloadExcelDetail()">
                                Exportar Detallado
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
                                
                                :on-input="onInputed"
                                :icon-input="'tabler-eye'"
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
            <VCard v-if="isLoadingIngresoInspeccion">
                <VCardText>
                    <div class="center_loader">
                        <VProgressCircular indeterminate color="secondary" />
                        <h3 style=" margin-top: 7px;color: #9b9b9b;">Cargando datos...</h3>
                    </div>
                </VCardText>

            </VCard>

            <VCard v-else>
                <VForm ref="refForm" @submit.prevent="onSubmit">
                    <VToolbar dense flat>
                        <VToolbarTitle>
                            {{ accion == 1 ? 'NUEVO INGRESO' : 'EDITAR INGRESO DOC ' + documento_correlativo  }}

                            <VBtn v-if="config_almacen_subgrupo_id != null"
                                size="x-small"
                                color="success">
                                Configuracion Cargada
                            </VBtn>
                            
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

                            <VCol cols="6">
                                
                                <h5 class="mb-4">Almacenamiento de Materia Prima</h5>
                                <VRow>
                                    <VCol cols="12">
                                        <VSelect v-model="year_id" label="Seleccionar Campaña" :rules="[requiredValidator]"
                                            clearable :items="optionYear"  :disabled="accion==2" />
                                    </VCol>
                                    <VCol cols="12">
                                        <VSelect v-model="center_id" label="Seleccionar Centro" :rules="[requiredValidator]"
                                            clearable :items="optionCenter" :disabled="accion==2" @update:model-value="centerFilters" />
                                    </VCol>
                                    <VCol cols="12">
                                        <VSelect v-model="warehouse_id" label="Seleccionar Alamcen" :rules="[requiredValidator]"
                                            clearable :items="optionWareHouse" :disabled="accion==2"  @update:model-value="changeSubGrupo()"/>
                                    </VCol>
                                 
                                    <VCol cols="12">
                                        <VSelect v-model="config_almacen_subgrupo_id" label="Seleccionar Tipo de Movimiento - Documento" :rules="[requiredValidator]"
                                            clearable :items="option_config_almacen_subgrupo" :disabled="accion==2"/>
                                    </VCol>
                                 
                                 
                                  <!--   <VCol cols="12">
                                        <VTextField v-model="guia_remicion" label="Guia de remision" :rules="[requiredValidator]" />
                                    </VCol> -->

                                      
                                    <VCol v-if="accion==2" cols="12">
                                        <VSelect v-model="state_id" label="Estado" :rules="[requiredValidator]" :items="optionState"  />
                                    </VCol>


                                </VRow>

                            </VCol>
                            
                           
                            
                            <VCol cols="6">
                                <h5 class="mb-4">Transporte</h5>
                                <VRow>
                                   <!--  <VCol cols="12">
                                        <VAutocomplete v-model="departamento" label="Seleccionar Departamento" :rules="[requiredValidator]"
                                            clearable :items="optionDepartamento" @update:model-value="provincia=null; distrito=null" />
                                    </VCol>
                                    <VCol cols="12">
                                        <VAutocomplete v-model="provincia" label="Seleccionar Provincia" :rules="[requiredValidator]"
                                            clearable :items="optionProvincia" @update:model-value="distrito=null"/>
                                    </VCol>
                                    <VCol cols="12">
                                        <VAutocomplete v-model="distrito" label="Seleccionar Distrito" :rules="[requiredValidator]"
                                            clearable :items="optionDistrito" />
                                    </VCol> -->

                              
                                    <VCol cols="12">

                                        <VRow no-gutters>
                                            <VCol
                                                cols="12"
                                                md="3"
                                                class="d-flex align-items-center"
                                            >
                                                <label
                                                class="v-label text-body-2 text-high-emphasis"
                                                for="placa"
                                                >Placa de vehiculo: </label>
                                            </VCol>

                                            <VCol
                                                cols="12"
                                                md="9"
                                            >
                                                <MaskInput :rules="[requiredValidator]" class="mask-style" placeholder="###-###" v-model="vehiculo" mask="XXX-XXX" name="placa"
                                                :onchange="valuePlcata()"
                                                />
                                                <div v-if="!state_placa" class="mt-1 ml-1" style=" color: red;font-size: small;">Debe ingresar la placa </div>
                                            </VCol>
                                        </VRow>
                                        <!-- <VTextField v-model="vehiculo" label="Placa de Vehiculo"  v-mask="'###-####'" 
                                        :rules="[requiredValidator]" 
                                        @input="vehiculo = vehiculo.toUpperCase()"/> -->

                                       

                                        <!-- <input mask="(##) ####-####" v-model="phone" placeholder="Enter phone number"> -->

                                        <!-- <VAutocomplete v-model="vehiculo" label="Seleccionar Vehiculo" :rules="[requiredValidator]"
                                            clearable :items="optionTransportista" @update:model-value="getTransportista" /> -->
                                    </VCol>
                                    <VCol cols="12">
                                        <VAutocomplete v-model="transportista" label="Seleccionar Transportista" :rules="[requiredValidator]"
                                            clearable :items="optionTransportista" />
                                    </VCol>
                                    
                                 
                                   
                                    <VCol cols="12">
                                        <AppDateTimePicker v-model="dateEntry"  label="Seleccionar Fecha"  class="date-time-picker"
                                          :config="{dateFormat: 'Y-m-d', maxDate: new Date(), allowInput: true}"
                                        :rules="[requiredValidator]" :disabled="listIngresoInspeccionState.length > 0" />
                                    </VCol>

                                  
                                    
                                </VRow>
                            </VCol> 
                            

                        </VRow>
    
                        <VRow v-if="accion==1" justify="space-between">

                            <VCol cols="12">
                                <!-- <h5 class="mb-4">Detalles de movimiento</h5>

                                <VCol cols="12" class="pb-0">
                                    <VBtn prepend-icon="tabler-plus" @click="onNewDetialMovement()" size="x-small">
                                        Agregar Detalle
                                    </VBtn>
                                </VCol> -->

                                <br>
                                <VRow justify="space-between">
                                    <VCol>
                                        <h5 class="mb-4">DETALLES DE MOVIMIENTO</h5>
                                    </VCol>
                                    <VCol>
                                        <VCol cols="12" class="pb-0 pt-0 text-right" >
                                            <VBtn prepend-icon="tabler-plus" @click="onNewDetialMovement()" size="x-small">
                                                Agregar Detalle
                                            </VBtn>
                                        </VCol>
                                    </VCol>
                                </VRow>
                                <VDivider />

                                <VRow>
                                    <VCol cols="12" class="mt-3">   
                                        <div>
                                            <ul class="list-group list-detail">

                                                
                                                <li class="list-detail-column">
                                                    <div>
                                                        <div class="title pb-2">ACCION</div>
                                                        <div>
                                                            <ul>
                                                                
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">

                                                                    <VBtn v-if="index >0"  icon size="x-small" color="error" @click="deleteItemDetail(item, index)" >
                                                                        <VIcon size="22" icon="tabler-trash" />
                                                                    </VBtn>
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                               <li class="list-detail-column">
                                                    <div class="col-guia">
                                                        <div class="title pb-2">GUIA_REMISION</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <VTextField type="text"  v-model="itemDetailMovement[index].guia_remicion"  :rules="[requiredValidator]"   @input="itemDetailMovement[index].guia_remicion = itemDetailMovement[index].guia_remicion.toUpperCase()" @update:model-value="setGrupoLoteValues(index)"  />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>

                                               <li class="list-detail-column">
                                                    <div class="col-guia">
                                                        <div class="title pb-2">GUIA_TRANSPORTISTA</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <VTextField type="text"  v-model="itemDetailMovement[index].guia_transportista"   @input="itemDetailMovement[index].guia_transportista = itemDetailMovement[index].guia_transportista.toUpperCase()"  @update:model-value="setGrupoLoteValues(index)" />
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
                                                                    :items="optionProvincia" @update:model-value="setDistritos(index); setGrupoLoteValues(index)"  />
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
                                                                    :items="itemDetailMovement[index].distritos"  @update:model-value="setGrupoLoteValues(index)"/>
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>


                                                <li class="list-detail-column">
                                                    <div class="col-variedad">
                                                        <div class="title pb-2">VARIEDAD</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <VAutocomplete v-model="itemDetailMovement[index].variedad_id"  :rules="[requiredValidator]"   label="VARIEDAD" 
                                                                    :items="optionVariedad" :disabled="itemDetailMovement[index].disabled" @update:model-value="setGrupoLoteValues(index)"/>
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
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <!-- <VAutocomplete v-model="itemDetailMovement[index].variedad_id"  :rules="[requiredValidator]"   label="VARIEDAD" :items="optionVariedad"/> -->
                                                                    <VAutocomplete v-model="itemDetailMovement[index].proveedor_centro_id"  :rules="[requiredValidator]"
                                                                    clearable :items="optionProveedor"  @update:model-value="setGrupoLoteValues(index)"/>
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
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <!-- <VAutocomplete v-model="itemDetailMovement[index].variedad_id"  :rules="[requiredValidator]"   label="VARIEDAD" :items="optionVariedad"/> -->
                                                                    <VAutocomplete v-model="itemDetailMovement[index].agricultor_id" 
                                                                    clearable :items="optionAgricultures"  @update:model-value="setGrupoLoteValues(index)"/>
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
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <VTextField type="text"  v-model="itemDetailMovement[index].destino"   @input="itemDetailMovement[index].destino = itemDetailMovement[index].destino.toUpperCase()"  />

                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>

                                                <li class="list-detail-column">
                                                    <div class="">
                                                        <div class="title pb-2">AGRUPACION_LOTE</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" :key="index"   class="item-detail">
                                                                    <VSelect v-model="itemDetailMovement[index].gruposublote"  :items="optionGrupoLote" :rules="[requiredValidator]" label="G"  @update:model-value="setGrupoLote(index)" />
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
                                                                    <VTextField type="number"  v-model="itemDetailMovement[index].peso_guia"  :rules="[requiredValidator]"
                                                                    @update:model-value="onCalcItemDetail(item, index)"  :min="0"
                                                                    />
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
                                                                    <VAutocomplete  v-model="itemDetailMovement[index].tipo_envase_id"  :rules="[requiredValidator]" 
                                                                    :items="optionTipoEnvase" @update:model-value=" onCalcItemDetail(item, index); setPesoEnvase(index)"/>
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                               
                                              

                                                <li class="list-detail-column">
                                                    <div>
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
                                                                    <VTextField type="number"  v-model="itemDetailMovement[index].cantidad_envase"  :rules="[requiredValidator]" @update:model-value="onCalcItemDetail(item, index)" :min="0" />
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
                                                                    <VTextField type="number"  v-model="itemDetailMovement[index].peso_bruto"   :rules="[requiredValidator, minValidatorRespiracion]" @update:model-value="onCalcItemDetail(item, index)" :min="1" />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <!-- 
                                                <li class="list-detail-column">
                                                    <div>
                                                        <div class="title pb-2">PESO_BALANZA</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"   v-model="itemDetailMovement[index].peso_balanza"   :rules="[requiredValidator, minValidatorRespiracion]" @update:model-value="onCalcItemDetail(item, index)" :min="1"  />
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
                                               
                                             <!--    <li class="list-detail-column">
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
                                                </li> -->
                                               <!-- 
                                                <li class="list-detail-column">
                                                    <div>
                                                        <div class="title pb-2">INSPECCION</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VCheckbox  v-model="itemDetailMovement[index].inspection" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>

                                                <li class="list-detail-column">
                                                    <div>
                                                        <div class="title pb-2">FRUTA_NO_APTA_POR_TAMAÑO</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number" :disabled="!itemDetailMovement[index].inspection"  v-model="itemDetailMovement[index].no_apta"  suffix="%" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div class="col-porcentaje">
                                                        <div class="title pb-2">PASMADO</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"  :disabled="!itemDetailMovement[index].inspection"  v-model="itemDetailMovement[index].pasmado"  suffix="%" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div class="col-porcentaje">
                                                        <div class="title pb-2">SOBRE_MADURO</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"  :disabled="!itemDetailMovement[index].inspection"  v-model="itemDetailMovement[index].sobre_maduro"  suffix="%" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                             
                                                <li class="list-detail-column">
                                                    <div class="col-porcentaje">
                                                        <div class="title pb-2">PEQUEÑO</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number" :disabled="!itemDetailMovement[index].inspection"   v-model="itemDetailMovement[index].pequenio"  suffix="%" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div class="col-porcentaje">
                                                        <div class="title pb-2">OTROS</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"  :disabled="!itemDetailMovement[index].inspection"  v-model="itemDetailMovement[index].otros"  suffix="%" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li> -->
                                             
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
    subject: packing_ingresos
</route>

    