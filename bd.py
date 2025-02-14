import sqlite3

DB_NAME = "amostras.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipamentos (
    processo INTEGER PRIMARY NOT NULL,
    nome TEXT NOT NULL,
    fabricante TEXT NOT NULL,
    data_entrada TEXT,
    tipo TEXT,
    descricao TEXT
)
    """)
    conn.commit()
    conn.close()

create_table()