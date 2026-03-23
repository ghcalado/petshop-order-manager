from .database import get_connection

def db_cadastrar_produto(nome, preco, unidade, categoria):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, preco, unidade, categoria) VALUES (?, ?, ?, ?)",
        (nome, preco, unidade, categoria)
    )
    conn.commit()
    conn.close()

def db_listar_produtos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, unidade, preco, categoria FROM produtos WHERE ativo = 1")
    produtos = cursor.fetchall()
    conn.close()
    return produtos
