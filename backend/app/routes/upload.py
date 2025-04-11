from fastapi import APIRouter, UploadFile, File, HTTPException
import io
import pandas as pd
import unidecode
import re
import json

router = APIRouter(prefix="/upload")

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Ler o arquivo
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), header=0)

        # LOG: Imprimir as colunas antes da normalização
        print("Colunas originais:", df.columns.tolist())

        # Normalizar os nomes das colunas
        df.columns = [
            re.sub(r'[^A-Z0-9]', '_', unidecode.unidecode(col).upper().strip())  # Substitui caracteres especiais por "_"
            .replace("__", "_")  # Remove duplos underscores
            for col in df.columns
        ]

        # LOG: Imprimir as colunas após a normalização
        print("Colunas normalizadas:", df.columns.tolist())

        # Criar um mapeamento para corrigir nomes de colunas específicas
        column_mapping = {
            "ORGAO_UN_ORC_EXEC": "ORGAO_UN_ORC_EXEC",
            "FUNC_SUB_PROG_PROJ_ATIVIDADE": "FUNC_SUB_PROG_PROJ_ATIVIDADE",
            "CATEGORIA_ELEMENTO": "CATEGORIA_ELEMENTO",
            "DESCRICAO": "DESCRICAO",
            "FR": "FR",
            "APL_VAR": "APL_VAR",
            "FICHA": "FICHA",
            "VL_DOTACAO": "VL_DOTACAO"
        }
        
        # Aplicar as correções de nome de coluna
        df.rename(columns=column_mapping, inplace=True)

        # Selecionando apenas colunas de tipo string
        df_colunas = df.select_dtypes(include=['object']).columns

        # Aplicando strip() nas colunas de texto
        for col in df_colunas:
            df[col] = df[col].str.strip()

        df[['FR', 'APL_VAR', 'FICHA']] = df[['FR', 'APL_VAR', 'FICHA']].astype(str)
        df['VL_DOTACAO'] = df['VL_DOTACAO'].astype(float)

        df['ID'] = (
            df['ORGAO_UN_ORC_EXEC'].astype(str) + 
            df['FUNC_SUB_PROG_PROJ_ATIVIDADE'].astype(str) + 
            df['CATEGORIA_ELEMENTO'].astype(str) + 
            df['FR'].astype(str) + 
            df['APL_VAR'].astype(str) + 
            df['FICHA'].astype(str)
        )

        # LOG: Imprimir colunas finais após ajustes
        print("Colunas ajustadas finais:", df.columns.tolist())

        # Definir as colunas esperadas
        required_columns = [
            "ORGAO_UN_ORC_EXEC", "FUNC_SUB_PROG_PROJ_ATIVIDADE", 
            "CATEGORIA_ELEMENTO", "DESCRICAO", "FR", "APL_VAR", "FICHA", "VL_DOTACAO"
        ]

        # Verificar se as colunas estão no DataFrame
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Colunas ausentes: {missing_columns}")

        # Converter DataFrame para uma estrutura JSON mantendo os tipos
        result = json.loads(df.to_json(orient="records"))

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar arquivo: {str(e)}")