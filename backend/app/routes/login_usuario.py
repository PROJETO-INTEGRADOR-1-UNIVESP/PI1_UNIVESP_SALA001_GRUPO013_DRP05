from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.models.schemas import UsuarioLogin
import bcrypt

router = APIRouter(prefix="/auth")

@router.post("/login")
async def login(usuario: UsuarioLogin):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (usuario.username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        if not bcrypt.checkpw(usuario.password.encode('utf-8'), user['senha'].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Senha incorreta")

        return {"access_token": "47951AFF8B5C85F0612A8C44315053F57F1DED0CFAF00DA0172E310CD3A6C2D1", "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer login: {str(e)}")
