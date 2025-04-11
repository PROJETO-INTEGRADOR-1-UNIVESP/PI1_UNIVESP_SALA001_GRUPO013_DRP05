from fastapi import FastAPI
from app.routes import upload, dados, cadastro_usuario, login_usuario
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Idealmente, substitua "*" por domínios confiáveis
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Incluindo as rotas
app.include_router(upload.router)
app.include_router(dados.router)
app.include_router(cadastro_usuario.router)
app.include_router(login_usuario.router)

@app.get("/")
def home():
    return {"message": "API Importador de Planilhas rodando!"}