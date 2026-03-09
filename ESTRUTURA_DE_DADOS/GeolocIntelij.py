import os
from pathlib import Path
from dotenv import load_dotenv
import googlemaps
from googlemaps import Client # Ajuda o VS Code a reconhecer os método

contador_api = 0  # Variável global para contar as chamadas

# 1. CONFIGURAÇÃO DE AMBIENTE
# Localiza o .env na mesma pasta deste arquivo
caminho_projeto = Path(__file__).resolve().parent
load_dotenv(dotenv_path=caminho_projeto / ".env")

# Busca a sua chave exata: GEOCODEAPI_KEY
API_KEY = os.getenv('GEOCODEAPI_KEY')

def inicializar_gmaps():
    """
    Cria e retorna o cliente do Google Maps usando a chave do .env.
    """
    if not API_KEY:
        print("❌ ERRO: GEOCODEAPI_KEY não encontrada no .env")
        return None
    
    try:
        # O uso de ': Client' resolve o erro visual de 'atributo desconhecido'
        gmaps: Client = googlemaps.Client(key=API_KEY)
        return gmaps
    except Exception as e:
        print(f"❌ Erro ao conectar com Google Maps: {e}")
        return None

def buscar_endereco(gmaps_client, endereco_curto): # gmaps = gmaps_client, endereco_curto = o que vai 
    """
    Recebe um endereço simples e retorna os dados geográficos de São Luís.
    """
    global contador_api

    if not gmaps_client:
        return None
    contador_api += 1 ### SOMA +1
    print(f"\n[INFO] Chamada à API nº: {contador_api} (Limite diário sugerido: 200)") ### PRINTA O AVISO
        
    # Força a busca dentro do contexto de São Luís para evitar erros
    busca = f"{endereco_curto}, São Luís, MA, Brasil"
    
    try:
        return gmaps_client.geocode(busca)
    except Exception as e:
        print(f"❌ Erro na busca de geolocalização: {e}")
        return None

def extrair_dados_limpos(resultado_google):
    """
    Transforma o retorno bruto do Google em um dicionário simples (Unificação Inteligente).
    """
    if not resultado_google:
        return None
        
    dados = resultado_google[0]
    
    # Busca o nome oficial do bairro nos componentes do endereço
    bairro_oficial = "Não Identificado"
    for componente in dados['address_components']: #O(n)
        if 'sublocality_level_1' in componente['types']:
            bairro_oficial = componente['long_name']
            
    return {
        "bairro": bairro_oficial,
        "lat": dados['geometry']['location']['lat'],
        "lng": dados['geometry']['location']['lng'],
        "endereco_formatado": dados['formatted_address']
    }
def buscar_endereco_regiao_metropolitana(gmaps_client, endereco_curto, cidade):
    """
    Agora recebe a 'cidade' como argumento para buscar em SLZ, Paço ou Ribamar.
    """
    if not gmaps_client:
        return None
        
    # Ex: "Maiobão, Paço do Lumiar, MA, Brasil"
    busca = f"{endereco_curto}, {cidade}, MA, Brasil"
    
    try:
        return gmaps_client.geocode(busca)
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        return None

def extrair_cidade_e_bairro(resultado_google):
    """
    Extrai tanto o Bairro quanto a Cidade oficial (Município).
    """
    if not resultado_google:
        return None
        
    dados = resultado_google[0]
    bairro = "Não Identificado"
    cidade = "Não Identificado"
    
    for componente in dados['address_components']:
        if 'sublocality_level_1' in componente['types']:
            bairro = componente['long_name']
        if 'administrative_area_level_2' in componente['types']:
            cidade = componente['long_name']
            
    return {
        "bairro": bairro,
        "cidade": cidade,
        "lat": dados['geometry']['location']['lat'],
        "lng": dados['geometry']['location']['lng']
    }

# No final do arquivo GeolocIntelij.py
if __name__ == "__main__":
    print("🌍 Módulo de Geolocalização carregado com sucesso.")
    test_gmaps = inicializar_gmaps()
    if test_gmaps:
        print("✅ Conexão com a API está ativa!")