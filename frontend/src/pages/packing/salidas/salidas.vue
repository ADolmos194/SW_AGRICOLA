<script lang="ts" setup>

import { messagePopupConfirm } from '@/functionsGlobals.js';
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
let radioSearch = ref('fecha_creacion')
let isDrawerVisible = ref(false)
let accion = ref(1)
const refForm = ref(null);

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


    // { key: "fecha", name: "fecha", order: true, search: true, class: 'text-center' },
    { key: "fecha_creacion", name: "fecha creacion", order: true, search: true, class: 'text-center' },
    { key: "documento", name: "Documento", order: true, search: true, class: 'text-center' },
    { key: "clase_movimiento", name: "Clase Movimiento", order: true, search: true, class: 'text-center' },
    { key: "tipodocumento", name: "Tipo Documento", order: true, search: true, class: 'text-center' },
    { key: "campania", name: "campaña", order: true, search: true, class: 'text-center' },
    { key: "centro", name: "centro", order: true, search: true, class: 'text-center' },
    { key: "almacen", name: "almacen", order: true, search: true, class: 'text-center' },
    { key: "subgrupo", name: "Categoria", order: true, search: true, class: 'text-center' },

    // { key: "procedencia", name: "procedencia", order: true, search: true, class: 'text-center' },
    // { key: "guia_remicion", name: "guia remicion", order: true, search: true, class: 'text-center' },
    // { key: "guia_transportista", name: "guia transportista", order: true, search: true, class: 'text-center' },
    // { key: "proveedor", name: "proveedor", order: true, search: true, class: 'text-center' },
    // { key: "vehiculo", name: "vehiculo", order: true, search: true, class: 'text-center' },
    // { key: "transportista", name: "transportista", order: true, search: true, class: 'text-center' },
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

let listDepartamento=ref([])
let listProvincia=ref([])
let listDistrito=ref([])

let listDepartamentoCenter=ref([])
let listProvinciaCenter=ref([])
let listDistritoCenter=ref([])
let listProveedor=ref([])
let listVehiculo=[]
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
let optionDepartamento = ref([])
let optionProveedor = ref([])
let optionVehiculo = ref([])
let optionTipoEnvase = ref([])
let optionVariedad = ref([])
let optionLotes = ref([])
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

// let society_id = ref(null)Z

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


let optionProvincia = computed(() => {
    return listProvinciaCenter.value.filter((item: any) => item.departamento == (departamento.value ?? '')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.cod} - ${item.descripcion}`.toUpperCase(),
            departamento_id: item.departamento,
        };
    });
});


let optionDistrito = computed(() => {
    return listDistritoCenter.value.filter((item: any) => parseInt(item.provincia_id) == parseInt(provincia.value ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.cod} - ${item.distrito}`.toUpperCase(),
            distrito_id: item.distrito_id,
            provincia_id: item.provincia_id,
        };
    });
});




let itemMovement = ref({
    id: 1,
    distrito_centro_id: 1,
    distrito_id: 224,
    distrito: "",
    provincia_id: 25,
    provincia: "",
    departamento_id: 2,
    departamento: "",
    procedencia: "",
    almacen_mov_doc_subgrupo_id: 2,
    almacen_subgrupo_id: 2,
    almacen_id: 1,
    almacen: "",
    subgrupo_id: 1,
    subgrupo: "",
    centro_id: 1,
    centro: "",
    fecha: "",
    // guida_remicion: "",
    // guia_tranportista: "",
    // proveedor_centro_id: 1,
    // proveedor_id: 1,
    proveedor: "",
    vehiculo_id: 1,
    vehiculo: "",
    transportista_id: 2,
    transportista: "",
    campania_id: 1,
    campania: 2024,
    inspeccion: false,
    estado: 1
})

let detail = {
    id: null,
    movimiento_id: null,
    movimiento_detalle_id: null,
    serie: "",
    lote: "",
    lote_serie: '',
    grupo_id: null,
    grupo: "",
    subgrupo_id: null,
    subgrupo: "",
    cultivo_id: null,
    cultivo: "",
    variedad_id: null,
    variedad: "",
    stock_consumo: 0,
    merma: 0,
    procesado: 0,
    respiracion_ptje: 0,
    respiracion_kg: 0,
    consumo_total: 0,
    stock: 0,
    stock_apto: 0,
    fecha: null,
    estado: 1,
    maxmema: 0,
    maxprocesado: 0,
    maxrespiracion: 0,
    minFecha: null,
    lotes: []
}

// let columnsListDetail = [
//     "ACCION",
//     "VARIEDAD",
//     "TIPO_ENVASE",
//     "PESO_ENVASE",
//     "CANTIDAD_ENVASE",
//     "PESO_BRUTO",
//     "PESO_NETO_GUIA",
//     "PESO_BALANZA",
//     "PESO_NETO_PLANTA",
//     "PESO_PROMEDIO_JABA",
//     "DIFERENCIA_PESO_GUIA",
//     "PORCENTAJE"
// ]

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
    // getListProvincia()
    // getListDistrito()

    // getListProveedor()
    // getListVehiculo()
    // getListTipoEnvase()
    dateEntry.value = moment().format('YYYY-MM-DD')
    getListVariedad()
    /*  
     getListSociety()
     getListCrop() */


    // console.log(moment().format('YYYY-MM-DD HH:mm:ss'));
    

})


// let optionCenter = computed(() => {
//     return listCenter.value.filter((item: any) => parseInt(item.sociedadpais) == parseInt(society_id.value ?? '0')).map((item: any) => {
//         return {
//             value: item.id,
//             title: `${item.abreviatura} - ${item.nombre}`.toUpperCase(),
//         };
//     });
// });




const listData = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: `/salidas/1-2`,
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

const getListDepartamento = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/departamento/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listDepartamento.value = response.data.data
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
        url: "/provincia/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listProvincia.value = response.data.data
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

const getListVehiculo = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/vehiculos/1",
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listVehiculo = response.data.data
            
            optionVehiculo.value = listVehiculo.map((item: any) => {
                return {
                    value: item.id,
                    title: `${item.nombre} - ${item.proveedor_abreviatura}`,
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

const getTransportista = () =>{

    let filterTransportista = listVehiculo.filter((item: any) => parseInt(item.id) == parseInt(vehiculo.value ?? '0'))
    
    transportista.value =filterTransportista.length > 0 ? `${filterTransportista[0].ruc} - ${filterTransportista[0].proveedor}` : ""
}


const getListConfigAlmaceSubGrupo = async () => {

    isLoading.value = true

    const config = {
        method: "get",
        url: "/config-almacen-subgrupo/1/S",
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

    // isLoading.value = true
    isSnackbarVisible.value = true

    stateSnackbar.value = 'danger'
    titleSnackbar.value =  'Cargando stocks de lotes a la fecha....' 

    const config = {
        method: "post",
        url: "/variedad-ingresos",
        data: {
            date: dateEntry.value,
            state: 1
        }
        //headers: { 'Content-Type': 'multipart/form-data', },
    };

    try {
        const response = await axios(config);
        if (response.status == 200) {
            listVariedad = response.data.data

            // stateSnackbar.value = 'success'
            // titleSnackbar.value = accion.value == 1 ? 'Registro creado con exito' : 'Registro actualizado con exito'

            isLoading.value = false
        } else {
            isLoading.value = false;
        }
    } catch (error) {
        isLoading.value = false;
    } finally{
        isSnackbarVisible.value = false
    }
}





const onEdit = (item: any) => {


    accion.value = 2
    // isDrawerVisible.value = true

    dialog.value = true

    if (refForm.value != null)
        refForm.value.reset();

    id.value = item.id


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
    vehiculo.value= item.vehiculo_id
    transportista.value= item.transportista
    guia_transportista.value= item.guia_transportista

    documento_correlativo.value= item.documento


    state_id.value = item.estado


    itemDetailMovement.value= []
    optionGrupoLote.value= []



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
    // dateEntry.value = moment().format('YYYY-MM-DD')
    guia_remicion.value= null



    departamento.value= null
    provincia.value= null
    distrito.value= null
    vehiculo.value= null
    transportista.value= null
    guia_transportista.value= null
    documento_correlativo.value= null


    itemDetailMovement.value= []
    optionGrupoLote.value= []

    onNewDetialMovement()


}


const onSubmit = async () => {
    const isValid = await refForm.value.validate();
    if (!isValid.valid) return;

    isSnackbarVisible.value = false


    let details = []

    for (let item of itemDetailMovement.value){

        let detail = {
            movimiento_detalle: item.movimiento_detalle_id,
            fecha: item.fecha,
            stock_consumo: item.stock_consumo,
            merma: item.merma,
            procesado: item.procesado,
            respiracion_ptje: item.respiracion_ptje,
            respiracion_kg: item.respiracion_kg,
            consumo_total: item.consumo_total,
        }

        details.push(detail)

    }

    


    let data = {
        fecha: null,
        campania: year_id.value,
        // vehiculo: vehiculo.value,
        // distrito_centro: distrito.value,
        almance_mov_doc: config_almacen_subgrupo_id.value,
        // guia_remicion: guia_remicion.value,
        // guia_transportista: guia_transportista.value,
        details: details,
        estado: accion.value == 1 ? 1 : state_id.value
    }

    


    const config = {
        method: accion.value == 1?  "post": "put",
        url:  accion.value == 1? "/salidas/create/": "/salidas/update/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            isDrawerVisible.value = false

            id.value= response.data.data.id
            
            await listData()
            await updateLotes()

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
        // dateEntry.value = false

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
        url: "/salidas/update-state/" + id.value.toString(),
        data: data,
    };

    try {
        const response = await axios(config);
        if (response.status == 201 || response.status == 200) {
            isDrawerVisible.value = false
            await listData()
            await updateLotes()

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
    console.log(item)
}


const onInputed = (item: any) => {

    router.push({ name: 'packing-salidas-detalle_salidas'});
    localStorage.setItem('salida', JSON.stringify(item))

}


const downloadExcel = async () => {

    const config = {
        method: "post",
        maxBodyLength: Infinity,
        url: "/salidas/download-excel/",
        headers: { 'Content-Type': 'multipart/form-data', },
        responseType: 'arraybuffer'
    };


    try {
        const response = await axios(config);

        if (response.status == 200) {
            const fileURL = window.URL.createObjectURL(new Blob([response.data]));

            const fileLink = document.createElement('a');
            fileLink.href = fileURL;
            fileLink.setAttribute('download', "salidas.xlsx");
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
        url: "/salidas-detalle/download-excel/",
        headers: { 'Content-Type': 'multipart/form-data', },
        responseType: 'arraybuffer'
    };


    try {
        const response = await axios(config);

        if (response.status == 200) {
            const fileURL = window.URL.createObjectURL(new Blob([response.data]));

            const fileLink = document.createElement('a');
            fileLink.href = fileURL;
            fileLink.setAttribute('download', "salidas-detallado.xlsx");
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

    
    listDistritoCenter.value =  listDistrito.value.filter((item: any) => parseInt(item.centro_id) == parseInt(center_id.value ?? '0'))

    optionProveedor.value =  listProveedor.value.filter((item: any) => parseInt(item.centro_id) == parseInt(center_id.value ?? '0')).map((item: any) => {
        return {
            value: item.id,
            title: `${item.ruc} - ${item.nombre}`.toUpperCase(),
            proveedor_id: item.proveedor_id,
        };
    });


    let filterProvincia = []

    for (let item of listDistritoCenter.value){
        for (let prov of listProvincia.value){
            if (parseInt(item.provincia_id) == parseInt(prov.id)){
                filterProvincia.push(prov)
                break
            }
        }
    }

    let filterProvinciaid= 0
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

    for (let index=0; index < itemDetailMovement.value.length; index++){
        itemDetailMovement.value[index].variedad_id = null
        itemDetailMovement.value[index].movimiento_detalle_id = null
        itemDetailMovement.value[index].lotes = []
    }

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
    optionGrupoLote.value = []

    let cont=0
    for (let index=0; index < itemDetailMovement.value.length; index++){
        itemDetailMovement.value[index].id = index
        // itemDetailMovement.value[index].gruposublote = cont+1
        cont++
        optionGrupoLote.value.push(cont)
    }
   
}

const onCalLotesVariedad = (item, index:number) =>{

    // optionLotes.value = listVariedad.filter((i: any) => parseInt(i.producto_id) == parseInt(item.variedad_id)).map((item: any) => {
    //     return {
    //         value: item.detalle_ingreso_id,
    //         title: `${item.serie_lote}`.toUpperCase(),
    //     };
    // });
    itemDetailMovement.value[index].movimiento_detalle_id = null

    itemDetailMovement.value[index].lotes= []
    
    itemDetailMovement.value[index].lotes = listVariedad.filter((i: any) => 
        parseInt(i.producto_id) == parseInt(item.variedad_id) && 
        parseFloat(i.stock_apto.toString()) > parseFloat(i.consumo_total.toString())).map((item: any) => {
            return {
                value: item.detalle_ingreso_id,
                title: `${item.documento} - ${item.lote}`.toUpperCase(),
            };
    });


    onCalLotesPesoNeto(item, index)


   /*  let detalle=[]
    // quiero comparar itemDetailMovement.value y optionLotes por el campo movimiento_detalle_id y value respectivamente y solo obtener los item  que optionlotes que no estan en  itemDetailMovement.value
    for (let item of optionLotes.value){
        let itemLote = itemDetailMovement.value.filter((i: any) => parseInt(i.movimiento_detalle_id) == parseInt(item.value))
        if (itemLote.length == 0){
            detalle.push(item)
        }
    }
    optionLotes.value = detalle */

}

const onCalLotesPesoNeto = (item, index:number) =>{

    
    let itemLote = listVariedad.filter((i: any) => parseInt(i.detalle_ingreso_id) == parseInt(itemDetailMovement.value[index].movimiento_detalle_id))

    //sumar consumo tatal de itemlote con propiedades de arreglos
    let consumo_total = itemLote.reduce((a, b) => parseFloat(a) + parseFloat(b.consumo_total), 0)


    itemDetailMovement.value[index].stock_consumo = itemLote.length > 0 ?   itemLote[0].stock_apto - consumo_total : 0 // itemLote[0].consumo_total : 0

    itemDetailMovement.value[index].minFecha = itemLote.length > 0 ? itemLote[0].fecha_inspeccion : null

    minDate.value= itemDetailMovement.value[index].minFecha

    onCalcItemDetailMerma(item, index)
    onCalcItemDetailProcesado(item, index)
    onCalcItemDetailRespiracion(item, index)


}


const onCalcItemDetailMerma  = (item, index:number) =>{

    let peso_neto = parseFloat(itemDetailMovement.value[index].stock_consumo)
    let procesado = parseFloat(itemDetailMovement.value[index].procesado)
    itemDetailMovement.value[index].maxmema = peso_neto - procesado

    onCalConsumtoTotalStock(index)

}

const onCalcItemDetailProcesado = (item, index:number) =>{

    let peso_neto = parseFloat(itemDetailMovement.value[index].stock_consumo)
    let merma = parseFloat(itemDetailMovement.value[index].merma)
    itemDetailMovement.value[index].maxprocesado = peso_neto - merma

    onCalConsumtoTotalStock(index)

}



const onCalcItemDetailRespiracion = (item, index:number) =>{

    let peso_neto = parseFloat(itemDetailMovement.value[index].stock_consumo)
    let merma = parseFloat(itemDetailMovement.value[index].merma)
    let procesado = parseFloat(itemDetailMovement.value[index].procesado)
    let respiracion = parseFloat(itemDetailMovement.value[index].respiracion_ptje)


    itemDetailMovement.value[index].maxrespiracion =  (100 * (peso_neto - (merma + procesado)))/peso_neto // ((peso_neto - merma - procesado)/procesado) * 100

    itemDetailMovement.value[index].respiracion_kg = peso_neto *  (respiracion / 100)

    onCalConsumtoTotalStock(index)
 }

 const onSetValRespiracion = (item, index) =>{
    itemDetailMovement.value[index].respiracion_ptje = itemDetailMovement.value[index].maxrespiracion.toFixed(3)
    

    onCalcItemDetailRespiracion(item, index)
 }

 const onCalConsumtoTotalStock = (index:number) =>{

    let peso_neto = parseFloat(itemDetailMovement.value[index].stock_consumo)
    let merma = parseFloat(itemDetailMovement.value[index].merma)
    let procesado = parseFloat(itemDetailMovement.value[index].procesado)
    let respiracion_kg = parseFloat(itemDetailMovement.value[index].respiracion_kg)
    
    let consumo_total =  merma + procesado + respiracion_kg
    itemDetailMovement.value[index].consumo_total  = (consumo_total).toFixed(2)
    itemDetailMovement.value[index].stock  =  (peso_neto - consumo_total).toFixed(2)


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

const updateLotes = async () =>{
    await getListVariedad()
    changeSubGrupo()

    // for (let index=0; index < itemDetailMovement.value.length; index++){
    //     itemDetailMovement.value[index].variedad_id = null
    //     itemDetailMovement.value[index].movimiento_detalle_id = null
    //     itemDetailMovement.value[index].lotes = []
    // }

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
                        
                        SALIDAS DE MATERIA PRIMA
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
            max-width="1500"
            class="custom-dialog"
            persistent 
            no-click-animation 
        >

            <VCard>
                <VForm ref="refForm" @submit.prevent="onSubmit">
                    <VToolbar dense flat>
                        <VToolbarTitle>
                            {{ accion == 1 ? 'NUEVA SALIDA' : 'EDITAR SALIDA DOC ' + documento_correlativo  }}

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

                            <VCol cols="12">
                                
                                <h5 class="mb-4">Salida de Materia Prima</h5>
                                <VRow>
                                    <VCol cols="4">
                                        <VSelect v-model="year_id" label="Seleccionar Campaña" :rules="[requiredValidator]"
                                            clearable :items="optionYear"  :disabled="accion==2" />
                                    </VCol>
                                    <VCol cols="4">
                                        <VSelect v-model="center_id" label="Seleccionar Centro" :rules="[requiredValidator]"
                                            clearable :items="optionCenter" :disabled="accion==2" @update:model-value="centerFilters" />
                                    </VCol>
                                    <VCol cols="4">
                                        <VSelect v-model="warehouse_id" label="Seleccionar Alamcen" :rules="[requiredValidator]"
                                            clearable :items="optionWareHouse" :disabled="accion==2"  @update:model-value="changeSubGrupo()"/>
                                    </VCol>
                                 
                                    <VCol cols="4">
                                        <VSelect v-model="config_almacen_subgrupo_id" label="Seleccionar Tipo de Movimiento - Documento" :rules="[requiredValidator]"
                                            clearable :items="option_config_almacen_subgrupo" :disabled="accion==2"/>
                                    </VCol>
                                 <!-- 
                                    <VCol cols="4">
                                        <AppDateTimePicker 
                                        v-model="dateEntry" clearable label="Seleccionar Fecha"  class="date-time-picker" 
                                        :config="{dateFormat: 'Y-m-d', maxDate: new Date(), allowInput: true}"  @change="updateLotes()" 
                                        :rules="[requiredValidator]" />
                                    </VCol> -->


                                    <VCol v-if="accion==2" cols="4">
                                        <VSelect v-model="state_id" label="Estado" :rules="[requiredValidator]" :items="optionState"  />
                                    </VCol>

                                </VRow>

                            </VCol>
                            
                        </VRow>
    
                        <VRow v-if="accion==1" justify="space-between">

                            <VCol cols="12">
                               
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
                                                    <div class="col-variedad">
                                                        <div class="title pb-2">VARIEDAD</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement"  class="item-detail">
                                                                    <VAutocomplete v-model="itemDetailMovement[index].variedad_id"  :rules="[requiredValidator]"   label="VARIEDAD" :items="optionVariedad"
                                                                        @update:model-value="onCalLotesVariedad(item, index)" 
                                                                    />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                               
                                                <li class="list-detail-column">
                                                    <div class="col-lote">
                                                        <div class="title pb-2">LOTE</div>
                                                        <div >
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VAutocomplete v-model="itemDetailMovement[index].movimiento_detalle_id"  :rules="[requiredValidator, maxValidatorDuplciado(itemDetailMovement[index].movimiento_detalle_id, index)]"   :items="itemDetailMovement[index].lotes"
                                                                     @update:model-value="onCalLotesPesoNeto(item, index)"
                                                                    />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                
                                                <li class="list-detail-column">
                                                    <div class="col-fecha">
                                                        <div class="title pb-2">FECHA</div>
                                                        <div >
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <AppDateTimePicker 
                                                                        v-model="itemDetailMovement[index].fecha"  label="Seleccionar Fecha"  class="date-time-picker" 
                                                                        :config="configSelectFecha" 
                                                                        :rules="[requiredValidator]" />
                                                                    
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>


                                              
                                                <li class="list-detail-column">
                                                    <div class="col-pesoneto">
                                                        <div class="title pb-2">STOCK A CONSUMIR</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"  v-model="itemDetailMovement[index].stock_consumo"  disabled :rules="[requiredValidator]"  />
                                                                </li>

                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                               
                                                <li class="list-detail-column">
                                                    <div class="col-merma">
                                                        <div class="title pb-2">MERMA</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"  v-model="itemDetailMovement[index].merma"   :rules="[requiredValidato,maxValidatorMerma(itemDetailMovement[index].merma, itemDetailMovement[index].maxmema)]" @update:model-value="onCalcItemDetailMerma(item, index); onCalcItemDetailProcesado(item, index); onCalcItemDetailRespiracion(item, index)" :min="0" :max="maxmema" :label="`0 - ${itemDetailMovement[index].maxmema.toFixed(2)}`"/>
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div  class="col-pesoneto">
                                                        <div class="title pb-2">PROCESADO</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"  v-model="itemDetailMovement[index].procesado"  :rules="[requiredValidator, maxValidatorProcesado(itemDetailMovement[index].procesado, itemDetailMovement[index].maxprocesado)]" :min="1" :max="maxprocesado"   @update:model-value="onCalcItemDetailProcesado(item, index); onCalcItemDetailMerma(item, index); onCalcItemDetailRespiracion(item, index)"  :label="`0 - ${itemDetailMovement[index].maxprocesado.toFixed(2)}`" />
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div  class="col-pesoneto">
                                                        <div class="title pb-2">RESPIRACION_%</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number"   v-model="itemDetailMovement[index].respiracion_ptje"   :rules="[requiredValidator, maxValidatorRespiracion(itemDetailMovement[index].respiracion_ptje, itemDetailMovement[index].maxrespiracion)]" @update:model-value="onCalcItemDetailRespiracion(item, index);onCalcItemDetailMerma(item, index); onCalcItemDetailProcesado(item, index)" :min="0" :max="maxrespiracion" suffix="%"   :label="`0 - ${itemDetailMovement[index].maxrespiracion.toFixed(3)}`"/>
                                                                </li>
                                                                
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div  class="col-pesoneto">
                                                        <div class="title pb-2">RESPIRACION_KG</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField  type="number" disabled v-model="itemDetailMovement[index].respiracion_kg"  :rules="[requiredValidator]" />
                                                                </li>
                                                               
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                
                                                <li class="list-detail-column">
                                                    <div  class="col-pesoneto">
                                                        <div class="title pb-2">CONSUMO_TOTAL</div>
                                                        <div>
                                                            <ul>
                                                                <li  v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField  type="number" disabled v-model="itemDetailMovement[index].consumo_total"  :rules="[requiredValidator]" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                
                                                <li class="list-detail-column">
                                                    <div class="col-stock"> 
                                                        <div class="title pb-2">STOCK</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VTextField type="number" disabled v-model="itemDetailMovement[index].stock"  displbled  :rules="[requiredValidator]" />
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li class="list-detail-column">
                                                    <div>
                                                        <div class="title pb-2">CALCULAR</div>
                                                        <div>
                                                            <ul>
                                                                <li v-for=" (item, index) in itemDetailMovement" class="item-detail">
                                                                    <VBtn  size="x-small" color="success" @click="onCalcItemDetailRespiracion(item, index); onSetValRespiracion(item, index)">
                                                                        consumo total
                                                                    </VBtn>
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

.col-lote {
  inline-size: 290px;
}

.col-merma {
  inline-size: 176px;
}

.col-pesoneto {
  inline-size: 176px;
}

.col-stock {
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

.col-fecha {
  inline-size: 182px;
}

</style>

<route lang="yaml">
meta:
    action: manage
    subject: packing_salidas
</route>
