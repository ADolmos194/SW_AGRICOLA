<script setup>
import { useAppAbility } from '@/plugins/casl/useAppAbility'
import { axiosInsAuth } from '@axios'
import { VForm } from 'vuetify/components'

import { useGenerateImageVariant } from '@core/composable/useGenerateImageVariant'
import { default as authV2LoginIllustrationBorderedLight, default as authV2LoginIllustrationLight } from '@images/pages/fondo1.jpg'
import { default as authV2LoginIllustrationBorderedDark, default as authV2LoginIllustrationDark } from '@images/pages/fondo2.jpg'
import authV2MaskDark from '@images/pages/misc-mask-dark.png'
import authV2MaskLight from '@images/pages/misc-mask-light.png'
import { VNodeRenderer } from '@layouts/components/VNodeRenderer'
import { themeConfig } from '@themeConfig'
import {
requiredValidator
} from '@validators'


const route = useRoute()
const router = useRouter()
const ability = useAppAbility()

const authThemeImg = useGenerateImageVariant(authV2LoginIllustrationLight, authV2LoginIllustrationDark, authV2LoginIllustrationBorderedLight, authV2LoginIllustrationBorderedDark, true)
const authThemeMask = useGenerateImageVariant(authV2MaskLight, authV2MaskDark)

const errors = ref({
    email: undefined,
    password: undefined,
})

const refVForm = ref()
const isPasswordVisible = ref(false)
const email = ref('')
const password = ref('')
const rememberMe = ref(false)


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

const login2 = () => {

    const me = this;

    var data = JSON.stringify({
        "username": email.value,
        "password": password.value,
    })

    var config = {
        method: 'post',
        url: '/api-token/',
        data: data,
        headers: { 'Content-Type': 'application/json' },
    }

    axiosInsAuth(config).then(r => {

        var key = r.data.access.split('.')
        var datos = JSON.parse(decodeURIComponent(escape(window.atob(key[1]))))

        console.log(datos)

        var menu = ''
        var habilidades = []
        var permisos = []
        var pos = 0


        for (let value of datos.permisos) {

            if (pos !== 0) {
                if (value.smenu !== menu) {
                    habilidades.push({ action: permisos, subject: menu })
                    permisos = []
                }
            }

            permisos.push(value.spermiso)

            menu = value.smenu
            pos++

            if (pos === datos.permisos.length) {
                habilidades.push({ action: permisos, subject: menu })
            }
        }



        habilidades.push({ action: ["manage"], subject: 'index' }, { action: 'read', subject: 'Auth' })


        const userData = {
            "id": datos.user_id,
            "fullName": datos.name,
            "username": datos.username,
            "avatar": "",
            "email": datos.email,
            "role": datos.rol,
        }

        /*  habilidades.push({ action: ["manage"], subject: 'home' }, { action: "manage", subject: 'packing' }, { action: "manage", subject: 'packing-recep' }, { action: ["manage"], subject: 'packing-home' }, { action: 'read', subject: 'Auth' })
      */
        localStorage.setItem('userAbilities', JSON.stringify(habilidades))
        ability.update(habilidades)
        localStorage.setItem('userData', JSON.stringify(userData))
        localStorage.setItem('accessToken', JSON.stringify(r.data.access))

        //router.replace('/packing/home')
        router.replace(route.query.to ? String(route.query.to) : '/')



    }).catch(e => {
        const { errors: formErrors } = e.response.data

        errors.value = formErrors
        //console.error(e.response.data)
    })
}

const onSubmit = () => {
    refVForm.value?.validate().then(({ valid: isValid }) => {
        if (isValid)
            login()
    })
}
</script>

<template>
    <VRow
        no-gutters
        class="auth-wrapper"
    >
        <VCol
            lg="8"
            class="d-none d-lg-flex"
        >
            <div class="position-relative auth-bg rounded-lg w-100 ma-8 me-0">
                <div class="d-flex align-center justify-center w-100 h-100">
                    <VImg
                        max-width="1500"
                        :src="authThemeImg"
                        class="auth-illustration mt-16 mb-2"
                    />
                </div>

                <VImg
                    :src="authThemeMask"
                    class="auth-footer-mask"
                />
            </div>
        </VCol>

        <VCol
            cols="12"
            lg="4"
            class="d-flex align-center justify-center"
        >
            <VCard
                flat
                :max-width="500"
                class="mt-12 mt-sm-0 pa-4"
            >
                <VCardText>
                    <VNodeRenderer
                        :nodes="themeConfig.app.logo"
                        class="mb-6"
                    />

                    <h5 class="text-h5 font-weight-semibold mb-1">
                        Bienvenido a {{ themeConfig.app.title }}! 👋🏻
                    </h5>
                    <p class="mb-0">
                        Inicia sesión en tu cuenta
                    </p>
                </VCardText>

                <VCardText>
                    <VForm ref="refVForm" @submit.prevent="onSubmit">
                        <VRow>
                            <!-- email -->
                            <VCol cols="12">
                                <VTextField
                                    v-model="email"
                                    label="Usuario"
                                    type="email"
                                    :rules="[requiredValidator]"
                                />
                            </VCol>

                            <!-- password -->
                            <VCol cols="12">
                                <VTextField
                                    v-model="password"
                                    label="Password"
                                    :rules="[requiredValidator]"
                                    :type="isPasswordVisible ? 'text' : 'password'"
                                    :append-inner-icon="isPasswordVisible ? 'tabler-eye-off' : 'tabler-eye'"
                                    @click:append-inner="isPasswordVisible = !isPasswordVisible"
                                />

                                <br>

                                <VBtn
                                    block
                                    type="submit"
                                >
                                    Login
                                </VBtn>
                            </VCol>

                            <!-- create account -->

                        </VRow>
                    </VForm>
                </VCardText>
            </VCard>
        </VCol>
    </VRow>
</template>

<style lang="scss">
@use "@core/scss/template/pages/page-auth.scss";
</style>

<route lang="yaml">
meta:
    layout: blank
    action: read
    subject: Auth
    redirectIfLoggedIn: true
</route>
