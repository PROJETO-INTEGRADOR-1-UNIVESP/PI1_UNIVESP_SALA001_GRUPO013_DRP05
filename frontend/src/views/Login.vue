<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="fazerLogin">
      <div>
        <label for="username">Usuário:</label>
        <input type="text" v-model="usuario.username" required />
      </div>
      <div>
        <label for="password">Senha:</label>
        <input type="password" v-model="usuario.password" required />
      </div>
      <button type="submit">Entrar</button>
    </form>
    <button @click="cadastrar_usuario">CADASTRAR NOVO USUARIO!</button>
    <p v-if="erro" style="color: red">{{ erro }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      usuario: {
        username: '',
        password: '',
      },
      erro: '',
    }
  },
  methods: {
    async fazerLogin() {
      try {
        const response = await axios.post('http://localhost:8000/auth/login', this.usuario)
        localStorage.setItem('token', response.data.access_token)
        this.$router.push('/Importacao')
      } catch (err) {
        this.erro = 'Usuário ou senha inválidos'
        console.error('Erro ao fazer login:', err)
      }
    },
    async cadastrar_usuario() {
      this.$router.push('/Cadastro_usuarios')
    },
  },
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
</style>
