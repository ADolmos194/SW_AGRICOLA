import { canNavigate } from "@layouts/plugins/casl"
import { setupLayouts } from 'virtual:generated-layouts'
import { createRouter, createWebHistory } from 'vue-router'
import routes from '~pages'
import { isUserLoggedIn } from "./utils"

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            redirect: (to) => {
                // return  { name: "index" }

                const userData = JSON.parse(localStorage.getItem("userData") || "{}")
                const userRole = userData && userData.role ? userData.role : null

                if (userRole != null) {
                    return  { name: "index" }
                }

                /* if (userRole === "Administrador") return { name: "home" };
                if (userRole === "client") return { name: "access-control" }; */
                return { name: "login", query: to.query }
            },
        },
        ...setupLayouts(routes),
    ],

    scrollBehavior() {
        return { top: 0 }
    },
})


// Docs: https://router.vuejs.org/guide/advanced/navigation-guards.html#global-before-guards
router.beforeEach((to) => {
    // return "/"
    
    const isLoggedIn = isUserLoggedIn()


    if (canNavigate(to)) {
        if (to.meta.redirectIfLoggedIn && isLoggedIn) return "/"
    } else {
        if (isLoggedIn) return { name: "not-authorized" }
        else
            return {
                name: "login",
                query: { to: to.name !== "index" ? to.fullPath : undefined },
            }
    }
})

export default router
