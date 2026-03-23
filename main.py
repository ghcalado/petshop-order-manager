from app.database import criar_tabelas
from app.core import db_cadastrar_produto, db_listar_produtos
# ... outros imports ...

def menu_principal():
    # Aqui você mantém seus inputs e prints, chamando as funções da pasta /app
    pass

if __name__ == "__main__":
    criar_tabelas()
    menu_principal()
