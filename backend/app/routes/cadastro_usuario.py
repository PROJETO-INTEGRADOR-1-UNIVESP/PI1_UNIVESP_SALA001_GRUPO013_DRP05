from fastapi import APIRouter, HTTPException
from app.database import create_user, get_user_by_username
from app.models.schemas import UsuarioCreate


router = APIRouter(prefix="/auth")

@router.post("/register")
async def register_user(usuario: UsuarioCreate):
    try:
        # Verificar se o usuário já existe
        user = get_user_by_username(usuario.username)
        print(user)
        if user:
            raise HTTPException(status_code=400, detail="Usuário já existe")

        # Cria o novo usuário
        create_user(usuario.username, usuario.email, usuario.password)

        return {"message": "Usuário criado com sucesso"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")