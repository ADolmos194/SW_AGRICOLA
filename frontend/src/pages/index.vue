<script lang="ts" setup>
import AuditoriaPorDiaService from '@/services/servicio_auditoria/AuditoriaPorDiaService';
import { ref, onMounted } from 'vue'

let titleSnackbar = ref(null)
let stateSnackbar = ref(null)
let isLoading = ref(false)

// Variables para almacenar las cantidades
const creaciones = ref(0)
const actualizaciones = ref(0)
const eliminaciones = ref(0)
const fechaActual = ref('')

const ListaDatos = async () => {
    isLoading.value = true

    try {
        const response = await AuditoriaPorDiaService.getAuditoriasPorDia()

        console.log(response) // Verifica el formato de la respuesta
        
        if (response && response.code === 200) {
            const data = response.data
            
            creaciones.value = data.creaciones
            actualizaciones.value = data.actualizaciones
            eliminaciones.value = data.eliminaciones
            fechaActual.value = data.fecha_actual
        }

    } catch (error) {
        titleSnackbar.value = `Error al cargar la cantidad de registro por día: ${error}`
    } finally {
        isLoading.value = false
    }
}

// Llamar la función al montar el componente
onMounted(() => {
    ListaDatos()
})
</script>

<template>
    <v-container>
        <v-row>
            <!-- Card 1: Creaciones -->
            <v-col cols="4">
                <v-card>
                    <v-card-title>Creaciones</v-card-title>
                    <v-card-text>{{ creaciones }} registros</v-card-text>
                    <v-card-subtitle>{{ fechaActual }}</v-card-subtitle>
                </v-card>
            </v-col>

            <!-- Card 2: Actualizaciones -->
            <v-col cols="4">
                <v-card>
                    <v-card-title>Actualizaciones</v-card-title>
                    <v-card-text>{{ actualizaciones }} registros</v-card-text>
                    <v-card-subtitle>{{ fechaActual }}</v-card-subtitle>
                </v-card>
            </v-col>

            <!-- Card 3: Eliminaciones -->
            <v-col cols="4">
                <v-card>
                    <v-card-title>Eliminaciones</v-card-title>
                    <v-card-text>{{ eliminaciones }} registros</v-card-text>
                    <v-card-subtitle>{{ fechaActual }}</v-card-subtitle>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<style scoped>
.v-card {
    text-align: center;
    background-color: #ffffff;
}
</style>


<route lang="yaml">
meta:
    action: manage
    subject: index
</route>
