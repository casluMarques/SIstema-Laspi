from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
import qrcode
import os

app = FastAPI()

DB_NAME = "amostras.db"

class Amostra(BaseModel):
    nome: str
    fabricante: str
    processo: int
    data_entrada: str
    tipo: str
    descricao: str

@app.post("/amostras/")
def criar_amostra(amostra: Amostra):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO amostras (nome, fabricante, processo, data_entrada, tipo, descricao)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (amostra.nome, amostra.fabricante, amostra.processo, amostra.data_entrada, amostra.tipo, amostra.descricao))
    conn.commit()
    amostra_id = cursor.lastrowid
    conn.close()
    
    # Gerando o QR Code com o ID
    qr = qrcode.make(f"http://localhost:8501/?id={amostra_id}")
    # verifica se a pasta existe
    os.makedirs("qrcodes", exist_ok=True)
    qr.save(f"qrcodes/amostra_{amostra_id}.png")

    return {"id": amostra_id, "qr_code": f"qrcodes/amostra_{amostra_id}.png"}

@app.get("/amostras/{amostra_id}")
def get_amostra(amostra_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM amostras WHERE id=?", (amostra_id,))
    amostra = cursor.fetchone()
    conn.close()

    if not amostra:
        return {"erro": "amostra nao encontrada"}

    return {
        "id": amostra[0],
        "nome": amostra[1],
        "fabricante": amostra[2],
        "processo": amostra[3],
        "data_entrada": amostra[4],
        "tipo": amostra[5],
        "descricao": amostra[6]
    }
