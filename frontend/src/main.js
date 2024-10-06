/* eslint-disable import/order */
import '@/@iconify/icons-bundle'
import App from '@/App.vue'
import ability from '@/plugins/casl/ability'
import i18n from '@/plugins/i18n'
import layoutsPlugin from '@/plugins/layouts'
import vuetify from '@/plugins/vuetify'
import { loadFonts } from '@/plugins/webfontloader'
import router from '@/router'
import '@styles/styles.scss'
import { abilitiesPlugin } from '@casl/vue'
import '@core/scss/template/index.scss'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import "vue-search-select/dist/VueSearchSelect.css"
// import VMask from 'v-mask';
import { MaskInput } from "vue-mask-next";
import VueApexCharts from 'vue3-apexcharts'

loadFonts()
// Create vue app
const app = createApp(App)

app.use(vuetify)
app.use(createPinia())
app.use(router)
app.use(layoutsPlugin)
// app.use(VMask);
// app.directive('maska', vMaska); 
app.component("MaskInput", MaskInput)
app.component('Apexchart', VueApexCharts)
app.use(i18n)
app.use(abilitiesPlugin, ability, {
    useGlobalProperties: true,
})

// Mount vue app
app.mount('#app')



