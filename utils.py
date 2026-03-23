import urllib.parse
from datetime import datetime

def gerar_link_whatsapp(numero, nome_lojista, itens, total):
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
    # ... sua lógica de gerar_mensagem_whatsapp ...
    mensagem = f"Pedido de {nome_lojista} em {timestamp}..." 
    return f"https://wa.me/{numero}?text={urllib.parse.quote(mensagem)}"
