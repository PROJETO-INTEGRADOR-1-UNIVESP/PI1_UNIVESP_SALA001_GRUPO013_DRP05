<template>
  <div>
    <h2>Importar Planilha Orçamento Municipal</h2>
    <input type="file" @change="uploadFile" />

    <p v-if="carregando">Carregando arquivo...</p>

    <div
      v-if="dados.length"
      style="
        max-height: 400px;
        overflow: auto;
        border: 1px solid #ccc;
        margin-top: 16px;
        margin-bottom: 16px;
      "
    >
      <table style="width: 100%; border-collapse: collapse">
        <thead style="position: sticky; top: 0; background: #f9f9f9">
          <tr>
            <th
              v-for="col in colunas"
              :key="col"
              style="border: 1px solid #ddd; padding: 8px; text-align: left; font-weight: bold"
            >
              {{ col }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(linha, index) in dados" :key="index">
            <td v-for="col in colunas" :key="col" style="border: 1px solid #ddd; padding: 8px">
              {{ linha[col] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <button @click="enviarDados" :disabled="enviando">
      {{ enviando ? 'Enviando...' : 'Enviar Dados' }}
    </button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      dados: [],
      colunas: [],
      carregando: false,
      enviando: false,
    }
  },
  methods: {
    async uploadFile(event) {
      const file = event.target.files[0]
      if (!file) return

      this.carregando = true

      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await axios.post('http://localhost:8000/upload/', formData)
        if (!response.data || !Array.isArray(response.data) || response.data.length === 0) {
          console.error('Nenhum dado retornado do backend.')
          this.carregando = false
          return
        }

        this.dados = response.data
        this.colunas = Object.keys(this.dados[0]).map((col) => col.trim())
      } catch (error) {
        console.error('Erro ao fazer upload:', error)
      } finally {
        this.carregando = false
      }
    },
    async enviarDados() {
      this.enviando = true
      try {
        await axios.post('http://localhost:8000/enviar-dados/', this.dados)
        alert('Dados enviados com sucesso!')
      } catch (error) {
        console.error('Erro ao enviar dados:', error)
        alert('Falha ao enviar os dados. Verifique o console para mais detalhes.')
      } finally {
        this.enviando = false
      }
    },
  },
}
</script>
