from pydantic import BaseModel

class DadosImportados(BaseModel):
    ID: str
    ORGAO_UN_ORC_EXEC: str
    FUNC_SUB_PROG_PROJ_ATIVIDADE: str
    CATEGORIA_ELEMENTO: str
    DESCRICAO: str
    FR: str
    APL_VAR: str
    FICHA: str
    VL_DOTACAO: float

# Novos modelos para o cadastro e login de usuário

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str

class UsuarioLogin(BaseModel):
    username: str
    password: str
