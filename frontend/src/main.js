import './assets/main.css';

import { createApp } from 'vue';
import App from './App.vue';  // Importando o App.vue corretamente
import router from './router';

const app = createApp(App);
app.use(router);
app.mount('#app');
