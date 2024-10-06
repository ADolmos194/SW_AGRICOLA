<script lang="ts" setup>
import { computed, defineProps, onMounted, ref, watchEffect } from 'vue';

const props = defineProps(['onEdit', 'onDelete', 'data', 'colums', 'onCol', 'isLoading', 'searchQuery', 'rowPerPage', 'filters', 'onSelected',  'onInput', 'onInputSecondary', 'id', 'iconInput', 'iconInputSecondary'])

let sortVariable = ref('')
let orderingTable = ref('asc')
let radioSearch = ref(props.colums[0].key)
let dataStates = ref([])
let dataBackup = ref([])
let dataComponent = ref([])
let dataTemp = ref([])
let filtersComponent = ref([])
let selectedItemsComponent = ref([]);

let searchQueryComponent = ref('')

let arrayDividido= []
//let rowPerPage= 10
let rowPerPageComponent= ref(10)
let totalData= 0

let textPaginationData= ref('')
let currentPage= ref(1)
let totalPage= ref(1)

let stateEdit = false
let stateDelete = false 
let stateInput = false
let stateInputSecondary = false
let stateSelected = false

let ids = ref([])


const edited = (itemCol) => {
    props.onEdit(itemCol)
}

const deleted = (itemCol) => {
    props.onDelete(itemCol)
}

const inputed = (itemCol) => {
    props.onInput(itemCol)
}

const inputedSecondary = (itemCol) => {
    props.onInputSecondary(itemCol)
}



const selectAllComputed = computed({
  get: () => {
    props.onSelected(selectedItemsComponent.value)
    return selectedItemsComponent.value.length === dataComponent.value.length;
  },
  set: (value) => {
    if (value) {
      selectedItemsComponent.value = dataComponent.value.map(item => item.id);
    } else {
      selectedItemsComponent.value = [];  
    }
    //props.onSelected(selectedItemsComponent.value)
  },
});


const toggleSelectAll = ()=> {
    if (selectAllComputed) {
        selectedItemsComponent.value = dataComponent.value.map(item => {
            let state = []

            for (const id of ids.value) {
                state.push(item[id])
                
            }
            return state.length > 1 ? state : state[0]

            //item.id
        } );
    } else {
        selectedItemsComponent.value = [];
    }
}



const searchFilter = () =>{

    dataComponent.value = dataBackup.value;


    var dataFind = dataComponent.value;
    var dataFindTemp = [];


    for (const filter of filtersComponent.value) {

        if (dataFind.length<=0){
            break
        }

        dataFindTemp = dataFind.filter((item) => {
            //return item[filter.key].toLowerCase().indexOf(filter.value !== null ? filter.value : '') !== -1;

            if (filter.value !== null &&  filter.value !== '')
                return (item[filter.key] ?? '').toString() === (filter.value ?? '').toString() 
            else
                return true

        });
    
        dataFind = dataFindTemp
    }

    dataComponent.value  = dataFind
    dataStates.value = dataFind

    searchTable()


}

const sortTable = (column) => {

    if (orderingTable.value === 'asc') {
        var arrayOrdenado = dataComponent.value.sort((a, b) => {
            return a[column].toString().localeCompare(b[column], 'en', { numeric: true })
        })
    } else if (orderingTable.value === 'desc') {
        var arrayOrdenado = dataComponent.value.sort((a, b) => {
            return b[column].toString().localeCompare(a[column], 'en', { numeric: true })
        })
    }

    dataComponent.value = arrayOrdenado
    dividirArray()
}

const searchTable = () => {

    dataComponent.value = dataStates.value

    var resultSearch = dataComponent.value.filter((item) => {
        return item[radioSearch.value].toString().toLowerCase().indexOf(searchQueryComponent.value.toLowerCase()) !== -1;
    });

    dataComponent.value = resultSearch;


    /* if (selectedItemsComponent.value.length >= dataComponent.value.length) {
        toggleSelectAll()
    } else {
        selectedItemsComponent.value = []
    } */


    dividirArray()
}

const  dividirArray = ()=>  {
    totalData = dataComponent.value.length;

    arrayDividido = [];

    for (let i = 0; i < dataComponent.value.length; i += Number(rowPerPageComponent.value)) {
        let pedazo = dataComponent.value.slice(i, i + Number(rowPerPageComponent.value));
        arrayDividido.push(pedazo);
    }


    if (arrayDividido.length<1){
        currentPage.value = arrayDividido.length;
    }else{
        if (currentPage.value>arrayDividido.length){
            currentPage.value= arrayDividido.length
        }else{
            currentPage.value=  currentPage.value <= 0 ? 1: currentPage.value 
        }
    }

    /* if (Number(currentPage.value) > Number(arrayDividido.length) || Number(currentPage.value) === 0) {
        
        currentPage.value = arrayDividido.length;
    } */

    totalPage.value = Math.ceil(Number(totalData) / Number(rowPerPageComponent.value));

    paginationData()

}

const  paginationData = () => {
    dataTemp.value = [];
    textPaginationData.value = '';

    if (arrayDividido[currentPage.value - 1] != undefined) {

        dataTemp.value = arrayDividido[currentPage.value - 1];

        const firstIndex = dataTemp.value.length ? (currentPage.value - 1) * rowPerPageComponent.value + 1 : 0
        const lastIndex = dataTemp.value.length + (currentPage.value - 1) * rowPerPageComponent.value

        textPaginationData.value = `Mostrando ${firstIndex} a ${lastIndex} de ${totalData} entradas`
    }

}



onMounted(() => {
    //dataTemp.value= props.data 
    dataBackup.value = props.data
    dataComponent.value= props.data  
    dataStates.value = props.data
    radioSearch.value = props.colums[0].key
    rowPerPageComponent.value = props.rowPerPage
    filtersComponent.value = props.filters

    if (props.onEdit){
        stateEdit= true
    }

    if (props.onDelete){
        stateDelete=true
    }

    if (props.onInput){
        stateInput=true
    }
    
    if (props.onInputSecondary){
        stateInputSecondary=true
    }
    
    if (props.onSelected){
        stateSelected=true
    }

    

    if (!props.id){
        ids.value =['id']
    }else{
        ids.value = props.id 
    }

    //searchFilter()
})


watchEffect(() => {
    
    filtersComponent.value = []
    if (JSON.stringify(filtersComponent.value) !== JSON.stringify(props.filters)){
        filtersComponent.value= props.filters
        searchFilter()
    }

    if (JSON.stringify(dataBackup.value) != JSON.stringify(props.data) || searchQueryComponent.value != props.searchQuery || rowPerPageComponent.value != props.rowPerPage) {
        dataComponent.value = props.data
        dataBackup.value = props.data
        dataStates.value = props.data
        searchQueryComponent.value = props.searchQuery
        
        if (rowPerPageComponent.value != props.rowPerPage){
            rowPerPageComponent.value = props.rowPerPage
            dividirArray()
        }else{
            searchFilter()
        }
    }
    



})


const clikSearch = (itemCol) => {
    radioSearch.value = itemCol.key
    props.onCol(itemCol.name)
    searchTable()
}

const resolveStateColor = (value, itemsSate) =>{
    let state = ''

    for (const item of itemsSate) {
        if (value.toString() === item.key.toString()){
            state = item.color
            break
        }
        
    }
    return state
}

const resolveStateAlias = (value, itemsSate) =>{
    let state = ''

    for (const item of itemsSate) {
        if (value.toString() === item.key.toString()){
            state = item.alias
            break
        }
        
    }
    return state
}

const resolveItemsid = (item) =>{
    let state = []

    for (const id of ids.value) {
        state.push(item[id])
        
    }
    return state.length > 1 ? state : state[0]
}



</script>


<template>
    
    <VTable class="text-no-wrap">
        <thead>
            <tr>

                <th v-if="stateSelected" scope="col">
                    <VCheckbox v-model="selectAllComputed" @click.native="toggleSelectAll" />
                </th>
                
                <th v-if="stateEdit || stateDelete" scope="col">
                    <span class="text-capitalize text-base font-weight-semibold">OPCIONES</span>
                </th>

                <th v-for="cols in props.colums" scope="col">
                    

                    <template v-if="cols.order">
                        <VAvatar :color="sortVariable === cols.key ? 'primary' : 'secondary'"
                            :icon="orderingTable === 'asc' && sortVariable === cols.key ? 'tabler-arrow-big-up-lines' : 'tabler-arrow-big-down-lines'"
                            variant="tonal" size="30" class="me-4 cursor-pointer"
                            @click="sortVariable = cols.key; orderingTable === 'asc' ? orderingTable = 'desc' : orderingTable = 'asc'; sortTable(cols.key)" />
                    </template>

                    <template v-if="cols.search">
                        <span
                            :class="radioSearch === cols.key ? 'text-capitalize text-base cursor-pointer font-weight-semibold text-columna-seleccionado' : 'text-capitalize text-base cursor-pointer font-weight-semibold'"
                            @click="clikSearch(cols)">{{ cols.name.toUpperCase() }}</span>
                    </template>
                    <template v-else>
                        <span class="text-capitalize text-base font-weight-semibold">{{ cols.name }}</span>
                    </template>
                </th>


            </tr>
        </thead>
        <tbody v-if="!props.isLoading">
            
            
            <tr v-for="   item    in    dataTemp   " :key="item.id">
                
                 <td v-if="stateSelected" class="text-center">
                     <VCheckbox v-model="selectedItemsComponent"  :value="resolveItemsid(item)" />
                 </td>
                 
                <td v-if="stateDelete || stateEdit || stateInput || stateInputSecondary" class="text-center" style="width: 5rem;">
                    <VBtn v-if="stateEdit"  icon size="x-small" color="primary" variant="text"
                        @click="edited(item)">
                        <VIcon size="22" icon="tabler-edit" />
                    </VBtn>
                    <VBtn v-if="stateDelete" icon size="x-small" color="error" variant="text"
                        @click="deleted(item)">
                        <VIcon size="22" icon="tabler-trash" />
                    </VBtn>
                    
                    <VBtn v-if="stateInput" icon size="x-small" color="success" variant="text"
                        @click="inputed(item)">
                        <VIcon size="22" :icon="props.iconInput? props.iconInput : 'tabler-transfer-in'" />
                    </VBtn>
                    
                    <VBtn v-if="stateInputSecondary" icon size="x-small" color="warning" variant="text"
                        @click="inputedSecondary(item)">
                        <VIcon size="22" icon="tabler-transfer-in" />
                    </VBtn>


                    
                </td>
                <template v-for="col in props.colums">
                    <td  :class="col.class">

                        <template v-if="!col.hasOwnProperty('alias')">
                            <span  class="text-base">{{ item[col.key] }}</span>
                        </template>
                        <template v-else>
                            <VChip v-if ="col.alias" label :color="resolveStateColor(item[col.key], col.itemsAlias ?? [])" size="small"
                                class="text-capitalize">
                                {{ resolveStateAlias(item[col.key], col.itemsAlias ?? []) }}
                            </VChip>
                            <span v-else class="text-base">{{ item[col.key] }}</span>
                        </template>
                    </td>

                </template>

            
            </tr>

        </tbody>

        <tbody v-if="isLoading">
            <tr>
                <td colspan="15" style=" position: relative; height: 120px;text-align: center;">
                    <span class="loader"></span>
                    <VProgressCircular indeterminate color="secondary" />
                    <h3 style=" margin-top: 7px;color: #9b9b9b;">Cargando datos...</h3>
                </td>
            </tr>
        </tbody>

         <tfoot
            v-show="!dataTemp.length && isLoading === false || dataTemp === null && isLoading === false">
            <tr>
                <td colspan="7" class="text-center">
                    No hay registros para mostrar
                </td>
            </tr>
        </tfoot>
        </VTable>

        <VDivider />

        <VCardText class="d-flex align-center flex-wrap justify-space-between gap-4 py-3 px-5">
            <span class="text-sm text-disabled">
                {{ textPaginationData }}
            </span>

            <VPagination v-model="currentPage" size="small" :total-visible="5" :length="totalPage"
                @click=" dividirArray()" />
        </VCardText>


</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.text-columna-seleccionado {
  color: #0d60c6 !important;
  font-weight: bold !important;
}
</style>
