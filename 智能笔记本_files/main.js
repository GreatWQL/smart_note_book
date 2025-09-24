import { createApp } from "/node_modules/.vite/deps/vue.js?v=61e9f511"
import App from "/src/App.vue"
import router from "/src/router/index.js?t=1758681432883"
import ElementPlus from "/node_modules/.vite/deps/element-plus.js?v=61e9f511"
import "/node_modules/element-plus/dist/index.css"
import "/src/styles/global.css"
import * as ElementPlusIconsVue from "/node_modules/.vite/deps/@element-plus_icons-vue.js?v=61e9f511"
import i18n from "/src/i18n/index.js?t=1758681432667"

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)
app.use(ElementPlus)
app.use(i18n)
app.mount('#app')