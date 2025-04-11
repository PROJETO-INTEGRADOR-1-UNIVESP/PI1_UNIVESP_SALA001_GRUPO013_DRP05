import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Cadastro_usuarios from '../views/Cadastro_usuarios.vue'
import Importacao from '../views/Importacao.vue'

const routes = [
  { path: '/', redirect: '/Login' },
  { path: '/Login', component: Login },
  { path: '/Cadastro_usuarios', component: Cadastro_usuarios },
  { path: '/Importacao', component: Importacao },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
