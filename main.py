import sqlite3
import urllib.parse
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ================== CONFIGURATIONS (SECURE) ==================
# These values are pulled from your local .env file.
# On GitHub, your real secrets will remain hidden.
SENHA_LOJISTA   = os.getenv('SENHA_LOJISTA', '1234')
SENHA_ADMIN     = os.getenv('SENHA_ADMIN', 'admin_password')
NUMERO_VENDEDOR = os.getenv('NUMERO_VENDEDOR', '5500000000000')

# ================== DATABASE SETUP ==================
db_connection = sqlite3.connect('rspetlins.db')
cursor = db_connection.cursor()

def criar_tabelas():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nome     TEXT NOT NULL,
            preco    REAL NOT NULL,
            unidade  TEXT,
            categoria TEXT,
            ativo    INTEGER DEFAULT 1
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_lojista TEXT,
            data         TEXT,
            total        REAL,
            status       TEXT DEFAULT 'enviado'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id      INTEGER,
            produto_nome   TEXT,
            quantidade     INTEGER,
            preco_unitario REAL,
            subtotal       REAL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        )
    ''')
    db_connection.commit()

# ================== AUTHENTICATION ==================
def fazer_login():
    print("\n=== Rs Pet Lins — Order System ===")
    nome = input("Your Name: ").strip()
    print(f"Welcome, {nome}!")
    return nome

def verificar_senha(perfil='lojista'):
    senha_correta = SENHA_ADMIN if perfil == 'admin' else SENHA_LOJISTA
    tentativas = 0

    while tentativas < 3:
        senha = input("Password: ")
        if senha == senha_correta:
            print("Access granted!")
            return True
        tentativas += 1
        chances = 3 - tentativas
        if chances > 0:
            print(f"Incorrect password. {chances} attempt(s) left.")
        else:
            print("Access denied. System locked!")
    return False

# ================== PRODUCT MANAGEMENT ==================
def cadastrar_produto():
    while True:
        print("\n--- New Product ---")
        nome      = input("Product Name: ").strip()
        unidade   = input("Unit (ex: 1kg, pack): ").strip()
        categoria = input("Category: ").strip()

        try:
            preco = float(input("Price (ex: 12.90): "))
            cursor.execute(
                "INSERT INTO produtos (nome, preco, unidade, categoria) VALUES (?, ?, ?, ?)",
                (nome, preco, unidade or 'un', categoria or 'General')
            )
            db_connection.commit()
            print(f"Product '{nome}' registered successfully!")
        except ValueError:
            print("[ERROR] Invalid price. Use dot instead of comma.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

        if input("Register another? (y/n): ").lower() != 'y':
            break

def ver_produtos():
    print("\n" + "="*20 + " CATALOG " + "="*20)
    cursor.execute("SELECT id, nome, unidade, preco, categoria FROM produtos WHERE ativo = 1")
    produtos = cursor.fetchall()

    if not produtos:
        print("No products found.")
        return []

    for p in produtos:
        print(f"[{p[0]}] {p[1]} - {p[2]}  |  R$ {p[3]:.2f}  |  {p[4]}")
        print("-" * 45)

    return produtos

# ================== ORDERING SYSTEM ==================
def montar_pedido(nome_lojista):
    itens = []
    print("\n--- Building your order ---")
    print("Enter 0 to skip a product.\n")

    produtos = ver_produtos()
    if not produtos:
        return

    for p in produtos:
        pid, nome, unidade, preco, categoria = p
        try:
            qtd = int(input(f"Qty for '{nome}' (R$ {preco:.2f}): "))
            if qtd > 0:
                subtotal = qtd * preco
                itens.append({
                    'nome': f"{nome} - {unidade}",
                    'qtd': qtd,
                    'preco_unitario': preco,
                    'subtotal': subtotal
                })
        except ValueError:
            continue

    if not itens:
        print("Cart is empty. Order cancelled.")
        return

    total = sum(item['subtotal'] for item in itens)
    
    print("\n" + "="*20 + " ORDER SUMMARY " + "="*20)
    for item in itens:
        print(f"  {item['nome']} x{item['qtd']}  =  R$ {item['subtotal']:.2f}")
    print(f"\n  TOTAL: R$ {total:.2f}")
    print("=" * 45)

    if input("\nConfirm and generate WhatsApp link? (y/n): ").lower() == 'y':
        salvar_pedido(nome_lojista, itens, total)
        link = gerar_link_whatsapp(nome_lojista, itens, total)
        print(f"\nOrder saved! Copy this link:\n\n{link}\n")
    else:
        print("Order cancelled.")

def gerar_mensagem_whatsapp(nome_lojista, itens, total):
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
    linhas = [
        "*Pedido — Rs Pet Lins*",
        "─────────────────────",
        f"Lojista: {nome_lojista}",
        f"Data: {timestamp}",
        "─────────────────────",
    ]
    for item in itens:
        linhas.append(f"• {item['nome']} x{item['qtd']}  →  R$ {item['subtotal']:.2f}")
    linhas += [
        "─────────────────────",
        f"*Total: R$ {total:.2f}*",
        "",
        "_Sent via Rs Pet System_"
    ]
    return "\n".join(linhas)

def gerar_link_whatsapp(nome_lojista, itens, total):
    mensagem = gerar_mensagem_whatsapp(nome_lojista, itens, total)
    return f"https://wa.me/{NUMERO_VENDEDOR}?text={urllib.parse.quote(mensagem)}"

def salvar_pedido(nome_lojista, itens, total):
    data = datetime.now().strftime('%d/%m/%Y %H:%M')
    cursor.execute(
        "INSERT INTO pedidos (nome_lojista, data, total) VALUES (?, ?, ?)",
        (nome_lojista, data, total)
    )
    pedido_id = cursor.lastrowid
    for item in itens:
        cursor.execute(
            "INSERT INTO itens_pedido (pedido_id, produto_nome, quantidade, preco_unitario, subtotal) VALUES (?, ?, ?, ?, ?)",
            (pedido_id, item['nome'], item['qtd'], item['preco_unitario'], item['subtotal'])
        )
    db_connection.commit()

# ================== MENUS ==================
def ver_pedidos():
    print("\n" + "="*20 + " ORDERS HISTORY " + "="*20)
    cursor.execute("SELECT id, nome_lojista, data, total, status FROM pedidos ORDER BY id DESC")
    for ped in cursor.fetchall():
        print(f"Order #{ped[0]} | {ped[2]} | Total: R$ {ped[3]:.2f}")

def menu_admin():
    if not verificar_senha('admin'): return
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1- Add Product | 2- View Products | 3- View Orders | 0- Back")
        op = input("Choice: ")
        if op == '0': break
        elif op == '1': cadastrar_produto()
        elif op == '2': ver_produtos()
        elif op == '3': ver_pedidos()

def menu_lojista(nome):
    while True:
        print(f"\n--- Hello, {nome} ---")
        print("1- New Order | 2- My History | 0- Logout")
        op = input("Choice: ")
        if op == '0': break
        elif op == '1': montar_pedido(nome)
        elif op == '2': ver_pedidos()

def menu_principal():
    while True:
        print("\n=== RS PET LINS ===")
        print("1- Client Login | 2- Admin Panel | 0- Exit")
        op = input("Choice: ")
        if op == '0': break
        elif op == '1':
            nome = fazer_login()
            if verificar_senha('lojista'): menu_lojista(nome)
        elif op == '2': menu_admin()

# ================== EXECUTION ==================
if __name__ == "__main__":
    criar_tabelas()
    menu_principal()
    db_connection.close()