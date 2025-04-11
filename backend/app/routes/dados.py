from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.models.schemas import DadosImportados

router = APIRouter(prefix="/enviar-dados")

@router.post("/")
async def enviar_dados(data: list[DadosImportados]):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print(data)
        for row in data:
            id_value = row.ID
            valores = (
                id_value, row.ORGAO_UN_ORC_EXEC, row.FUNC_SUB_PROG_PROJ_ATIVIDADE,
                row.CATEGORIA_ELEMENTO, row.DESCRICAO, row.FR, row.APL_VAR,
                row.FICHA, row.VL_DOTACAO
            )
            print(valores)
            cursor.execute("SELECT COUNT(*) FROM dados_importados WHERE id = %s", (id_value,))
            if cursor.fetchone()[0] > 0:
                print("inicio")
                cursor.execute("""
                    UPDATE dados_importados SET
                    ORGAO_UN_ORC_EXEC = %s, FUNC_SUB_PROG_PROJ_ATIVIDADE = %s,
                    CATEGORIA_ELEMENTO = %s, DESCRICAO = %s, FR = %s, APL_VAR = %s,
                    FICHA = %s, VL_DOTACAO = %s
                    WHERE id = %s
                """, valores[1:] + (id_value,))
            else:
                cursor.execute("""
                    INSERT INTO dados_importados (id, ORGAO_UN_ORC_EXEC, FUNC_SUB_PROG_PROJ_ATIVIDADE,
                    CATEGORIA_ELEMENTO, DESCRICAO, FR, APL_VAR, FICHA, VL_DOTACAO)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, valores)

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Dados inseridos/atualizados com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar dados: {str(e)}")
