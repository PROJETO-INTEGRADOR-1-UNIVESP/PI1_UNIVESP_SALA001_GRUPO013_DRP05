import pandas as pd
import unidecode
import io

def process_excel(file):
    df = pd.read_excel(file)
    df.columns = [unidecode.unidecode(col.upper()) for col in df.columns]
    df['ID'] = df['ORGAO UN.ORC/EXEC'].astype(str) + df['FUNC/SUB/PROG PROJ/ATIVIDADE'].astype(str) + df['CATEGORIAELEMENTO'].astype(str) + df['DESCRICAO'].astype(str) + df['FR;APL/VAR'].astype(str) + df['FICHA'].astype(str)
    return df