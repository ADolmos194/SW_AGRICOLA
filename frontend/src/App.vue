<script setup>
import { useAppAbility } from '@/plugins/casl/useAppAbility';
import { useThemeConfig } from '@core/composable/useThemeConfig';
import { hexToRgb } from '@layouts/utils';
import { useTheme } from 'vuetify';


const {
    syncInitialLoaderTheme,
    syncVuetifyThemeWithTheme: syncConfigThemeWithVuetifyTheme,
    isAppRtl,
} = useThemeConfig()

const { global } = useTheme()

const route = useRoute()
const router = useRouter()
const ability = useAppAbility()


// ℹ️ Sync current theme with initial loader theme
syncInitialLoaderTheme()
syncConfigThemeWithVuetifyTheme()


const login = () => {
    //const { accessToken, userData, userAbilities } = r.data
    const userData= { "id":1,"fullName":"John Doe","username":"johndoe","avatar":"/src/assets/images/avatars/avatar-1.png","email":"admin@demo.com","role":"admin" }
    const userAbilities = [ 
        { "action":"manage","subject":"all" },
        { "action":"manage","subject":"packing_ingresos" },
        { "action":"manage","subject":"packing_salidas" },
        { "action":"manage","subject":"packing_detalle_salidas" },
        { "action":"manage","subject":"packing_detalle_ingresos" },
     ]
    const accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mn0.cat2xMrZLn0FwicdGtZNzL7ifDTAKWB0k1RurSWjdnw"

    localStorage.setItem('userAbilities', JSON.stringify(userAbilities))
    ability.update(userAbilities)
    localStorage.setItem('userData', JSON.stringify(userData))
    localStorage.setItem('accessToken', JSON.stringify(accessToken))
    router.replace(route.query.to ? String(route.query.to) : '/')

    /*axios.post('/auth/login', {
       ,
        email: email.value,
    password: password.value

    }).then(r => {
        // Redirect to `to` query if exist or redirect to index route
    }).catch(e => {
        const { errors: formErrors } = e.response.data

        errors.value = formErrors
        console.error(e.response.data)
    })*/
}

//login()




</script>

<template>
    <VLocaleProvider :rtl="isAppRtl">
        <!-- ℹ️ This is required to set the background color of active nav link based on currently active global theme's primary -->
        <VApp :style="`--v-global-theme-primary: ${hexToRgb(global.current.value.colors.primary)}`">
            <RouterView />
        </VApp>
    </VLocaleProvider>
</template>
