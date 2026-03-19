import os
from pathlib import Path
from dotenv import load_dotenv
import googlemaps
from googlemaps import Client 

# ZONAS CRÍTICAS E DE ALERTA (Unificação Inteligente)
# Definimos os polígonos exatos para Vermelho (Crítico), Amarelo (Alerta) e Azul (Comum).
# Focado na bacia do Rio Anil e Bacanga.

contador_api = 0  

# CONFIGURAÇÃO DE AMBIENTE
caminho_projeto = Path(__file__).resolve().parent
load_dotenv(dotenv_path=caminho_projeto / ".env")
API_KEY = os.getenv('GEOCODEAPI_KEY')

def inicializar_gmaps():
    if not API_KEY:
        print("❌ ERRO: GEOCODEAPI_KEY não encontrada no .env")
        return None
    try:
        gmaps: Client = googlemaps.Client(key=API_KEY)
        return gmaps
    except Exception as e:
        print(f"❌ Erro ao conectar com Google Maps: {e}")
        return None

def buscar_endereco_mestre(gmaps_client, endereco_curto, cidade="São Luís"):
    """Função unificada: Força o contexto de São Luís e conta chamadas."""
    global contador_api
    if not gmaps_client: return None
    contador_api += 1
    busca = f"{endereco_curto}, {cidade}, MA, Brasil"
    try:
        print(f"📡 Chamada API Google #{contador_api}: {busca}")
        return gmaps_client.geocode(busca)
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        return None

def extrair_cidade_e_bairro(resultado_google):
    if not resultado_google: return None
    dados = resultado_google[0]
    bairro, cidade = "Não Identificado", "Não Identificado"
    for componente in dados['address_components']:
        if 'sublocality_level_1' in componente['types']:
            bairro = componente['long_name']
        if 'administrative_area_level_2' in componente['types']:
            cidade = componente['long_name']
    return {
        "bairro": bairro, "cidade": cidade,
        "lat": dados['geometry']['location']['lat'],
        "lng": dados['geometry']['location']['lng']
    }

def avaliar_prioridade_geografica(lat, lng):
    """
    Seu Geofencing de 3 Níveis: Vermelho (Risco Alto), Amarelo (Médio), Azul (Normal).
    Calibrado para abranger a Liberdade e Bacias Anil/Bacanga.
    """
    
    # 1. ÁREAS DE RISCO CRÍTICO (Vermelho - Palafitas/Rio)
    # Expandimos a latitude do Anil para -2.540 para garantir que a Liberdade entre!
    rio_anil_critico = (-2.540 <= lat <= -2.520) and (-44.300 <= lng <= -44.270)
    
    # Zona Bacanga (Coroadinho e arredores)
    rio_bacanga_critico = (-2.580 <= lat <= -2.545) and (-44.320 <= lng <= -44.285)
    
    # Polo Industrial / Vila Maranhão
    vila_maranhao_critico = (-2.640 <= lat <= -2.580) and (-44.380 <= lng <= -44.310)

    # 2. ÁREAS DE ALERTA / BUFFER (Amarelo - Próximo ao risco)
    # Criamos uma borda de segurança um pouco maior que a crítica
    rio_anil_alerta = (-2.545 <= lat <= -2.515) and (-44.305 <= lng <= -44.265)
    rio_bacanga_alerta = (-2.585 <= lat <= -2.540) and (-44.325 <= lng <= -44.280)

    # 3. LÓGICA DE DECISÃO (O "Cérebro" do Geofencing)
    if rio_anil_critico or rio_bacanga_critico or vila_maranhao_critico:
        # Se cair aqui, o marcador no mapa será VERMELHO
        return "RISCO CRÍTICO (ALAGAMENTO/PALAFITA)", "ALTA" 
    
    elif rio_anil_alerta or rio_bacanga_alerta:
        # Se cair aqui, o marcador no mapa será AMARELO/LARANJA
        return "ÁREA DE ALERTA (PROXIMIDADE)", "MEDIA" 
    
    else:
        # Se não cair em nenhum dos retângulos, é AZUL
        return "ÁREA URBANA COMUM", "NORMAL" # Cor Azul

def gerar_url_mapa_estatico(lat, lng):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    config = f"center={lat},{lng}&zoom=16&size=600x300&maptype=roadmap"
    marcador = f"&markers=color:red%7Clabel:F%7C{lat},{lng}"
    return f"{base_url}{config}{marcador}&key={API_KEY}"