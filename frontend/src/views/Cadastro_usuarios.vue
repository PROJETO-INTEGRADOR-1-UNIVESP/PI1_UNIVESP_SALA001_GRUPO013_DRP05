<template>
  <div class="cadastro_usuario">
    <h2>Cadastro de Usuário</h2>
    <form @submit.prevent="CadastrarUsuario">
      <div>
        <label for="username">Usuário:</label>
        <input type="text" v-model="usuario.username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="usuario.email" required />
      </div>
      <div>
        <label for="senha">Senha:</label>
        <input type="password" v-model="usuario.senha" required />
      </div>
      <button type="submit">Cadastrar</button>
    </form>
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
        email: '',
        password: '',
      },
      erro: '',
    }
  },
  methods: {
    async CadastrarUsuario() {
      try {
        const response = await axios.post('http://localhost:8000/auth/register', this.usuario)
        this.showAlert()
      } catch (err) {
        this.erro = err.response.data.detail
        console.error('Erro ao fazer login:', err)
      }
    },
    showAlert() {
      alert('Usuário cadastrado com sucesso!')
    },
  },
}
</script>

<style scoped>
.cadastro_usuario {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
</style>
