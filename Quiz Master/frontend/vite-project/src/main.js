import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'; // Import Pinia
const pinia = createPinia(); // Create Pinia instance
const app = createApp(App)
app.use(pinia); // Register Pinia
app.use(router);
app.mount('#app')