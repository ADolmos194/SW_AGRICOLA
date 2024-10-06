<script lang="ts" setup>
import { defineProps, onMounted, ref, watchEffect } from 'vue'

const props = defineProps(['visible', 'title', 'closeVisible', 'state'])

let isSnackbarVisible= ref(null)
let iscloseVisible= ref(null)

onMounted(() => {
    isSnackbarVisible.value = props.visible
    iscloseVisible.value = props.closeVisible
})

watchEffect(() => {
    isSnackbarVisible.value = props.visible
    iscloseVisible.value = props.closeVisible
})

</script>

<template>
    
    <!-- Snackbar -->
    <VSnackbar
        v-model="isSnackbarVisible"
        multi-line
        :color="props.state"
        location="top end"
    >

    
    <VIcon class="mr-2" 
            :icon= "props.state === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'"
    />
    {{ props.title }}
 <!--    <span style="color: #414141;">

    </span> -->
    
        <template #actions>
            <!-- :color="props.state" -->
            <VBtn
                v-if="iscloseVisible"
                color="#fff"
                variant="tonal"
                @click="isSnackbarVisible = false"
            >
                Cerrar
            </VBtn>
        </template>
    </VSnackbar>  
</template>
