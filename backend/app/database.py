import mysql.connector
from passlib.context import CryptContext

# Configuração do banco de dados MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "univesp123",
    "database": "importador_db"
}

# Contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para obter a conexão com o banco de dados
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Função para hashear a senha
def hash_password(senha: str) -> str:
    return pwd_context.hash(senha)

# Função para verificar a senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar um novo usuário
def create_user(nome: str, email: str, senha: str):
    hashed_password = hash_password(senha)
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha)
            VALUES (%s, %s, %s)
        """, (nome, email, hashed_password))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()  # Se algo falhar, desfazemos a operação
        raise Exception(f"Erro ao criar usuário: {err}")
    finally:
        cursor.close()
        conn.close()

# Função para obter um usuário pelo nome
def get_user_by_username(nome: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE nome = %s", (nome,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return {"id": user[0], "nome": user[1], "email": user[2], "senha": user[3]}
    return None
