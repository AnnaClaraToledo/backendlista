from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ===== CORS (permite conectar no HTML) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== CONEXÃO MYSQL =====
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",        # coloca sua senha do MySQL se tiver
    database="lista"    # seu banco (você disse que é "lista")
)

cursor = conexao.cursor(dictionary=True)

# ===== MODELO =====
class Pessoa(BaseModel):
    nome: str
    mensagem: str

# ===== SALVAR PRESENÇA =====
@app.post("/confirmar")
def confirmar(pessoa: Pessoa):
    sql = "INSERT INTO lista (nome, mensagem) VALUES (%s, %s)"
    valores = (pessoa.nome, pessoa.mensagem)

    cursor.execute(sql, valores)
    conexao.commit()

    return {"status": "ok"}

# ===== LISTAR MENSAGENS =====
@app.get("/mensagens")
def mensagens():
    cursor.execute("SELECT nome, mensagem FROM lista ORDER BY id DESC")
    resultado = cursor.fetchall()

    return resultado