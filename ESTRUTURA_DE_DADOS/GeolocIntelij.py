import os
from pathlib import Path
from dotenv import load_dotenv
import googlemaps
from googlemaps import Client 
ZONAS_CRITICAS = {
    "ZONA_ANIL": {
        "nome": "Comunidade Ribeirinha - Rio Anil (Risco de Enchente)",
        "limites": {"lat_min": -2.535, "lat_max": -2.520, "lng_min": -44.290, "lng_max": -44.260}
    },
    "ZONA_BACANGA": {
        "nome": "Área de Palafitas - Rio Bacanga (Risco de Enchente)",
        "limites": {"lat_min": -2.570, "lat_max": -2.545, "lng_min": -44.310, "lng_max": -44.285}
    },
    "VILA_MARANHAO": {
        "nome": "Vila Maranhão (Vulnerabilidade Socioeconômica)",
        "limites": {"lat_min": -2.620, "lat_max": -2.580, "lng_min": -44.370, "lng_max": -44.320}
    }
}

contador_api = 0  


caminho_projeto = Path(__file__).resolve().parent
load_dotenv(dotenv_path=caminho_projeto / ".env")

# Busca a sua chave exata: GEOCODEAPI_KEY
API_KEY = os.getenv('GEOCODEAPI_KEY')

def inicializar_gmaps(): #1 ocorrência
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

def buscar_endereco(gmaps_client, endereco_curto): #2 ocorrência
    # gmaps = gmaps_client, endereco_curto = o que vai 
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

def extrair_dados_limpos(resultado_google): #4 ocorrência
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
def buscar_endereco_regiao_metropolitana(gmaps_client, endereco_curto, cidade): # 3 Ocorrência
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

def extrair_cidade_e_bairro(resultado_google): #5 ocorrência resultado_gooogle = res_bruto
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
def avaliar_prioridade_geografica(lat, lng):
    """
    Analisa se as coordenadas confirmadas pelo Google 
    estão dentro de áreas de risco real ou vulnerabilidade extrema.
    """
    for zona_id, info in ZONAS_CRITICAS.items():
        limites = info["limites"]
        if limites["lat_min"] <= lat <= limites["lat_max"] and \
           limites["lng_min"] <= lng <= limites["lng_max"]:
            return info["nome"], "ALTA" # Retorna o nome da zona e o nível de prioridade
            
    return "Área Urbana Comum", "NORMAL"
def gerar_url_mapa_estatico(lat, lng):
    """
    Gera um link de imagem do Google Maps para o endereço da família.
    """
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    config = f"center={lat},{lng}&zoom=16&size=600x300&maptype=roadmap"
    marcador = f"&markers=color:red%7Clabel:F%7C{lat},{lng}"
    return f"{base_url}{config}{marcador}&key={API_KEY}"

# No final do arquivo GeolocIntelij.py
if __name__ == "__main__":
    print("🌍 Módulo de Geolocalização carregado com sucesso.")
    test_gmaps = inicializar_gmaps()
    if test_gmaps:
        print("✅ Conexão com a API está ativa!")