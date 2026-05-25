from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os

app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== CONEXÃO (SEGURA) =====
def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

# ===== MODELO =====
class Pessoa(BaseModel):
    nome: str
    mensagem: str

# ===== INSERIR =====
@app.post("/confirmar")
def confirmar(pessoa: Pessoa):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "INSERT INTO lista (nome, mensagem) VALUES (%s, %s)"
    cursor.execute(sql, (pessoa.nome, pessoa.mensagem))

    conexao.commit()
    cursor.close()
    conexao.close()

    return {"status": "ok"}

# ===== LISTAR =====
@app.get("/mensagens")
def mensagens():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT id, nome, mensagem FROM lista ORDER BY id DESC")
    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados