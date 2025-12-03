import { createApp } from 'vue'
import { inject } from "@vercel/analytics"
import App from './App.vue'
import router from './router'
import './main.css'

inject()

const app = createApp(App)

app.use(router)

app.mount('#app')
