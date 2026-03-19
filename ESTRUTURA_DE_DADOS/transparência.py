import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Configuração robusta do caminho para Windows 11
caminho_projeto = Path(__file__).resolve().parent
load_dotenv(dotenv_path=caminho_projeto / ".env")

def buscar_beneficios_municipio(codigo_ibge, mes_ano):
    # 1. Busca e limpa a chave
    token = os.getenv('CHAVE_TRANSPARENCIA')
    
    if not token:
        print("❌ ERRO: Chave não encontrada no .env. Verifique o nome da variável.")
        return None

    headers = {"chave-api-dados": token.strip()}
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/novo-bolsa-familia-por-municipio"
    
    params = {
        "mesAno": mes_ano, 
        "codigoIbge": codigo_ibge,
        "pagina": 1
    }

    try:
        print(f"📡 Consultando Governo: {mes_ano} | IBGE: {codigo_ibge}...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            if not dados:
                print("⚠️ API respondeu 200, mas a lista de dados está VAZIA.")
                return None
            print(f"✅ Sucesso: {len(dados)} registros encontrados!")
            return dados
        else:
            print(f"⚠️ Erro API: Status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Falha de conexão: {e}")
        return None