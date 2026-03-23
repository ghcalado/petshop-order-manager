import sqlite3

def get_connection():
    return sqlite3.connect('rspetlins.db')

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()
    # ... cole aqui todos os seus comandos CREATE TABLE IF NOT EXISTS ...
    conn.commit()
    conn.close()
