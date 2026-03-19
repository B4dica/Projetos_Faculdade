import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from transparência import buscar_beneficios_municipio

def grafico_comparativo_cidades(cadastro_geral):
    # --- ESTA FUNÇÃO GERA APENAS O GRÁFICO DE BARRAS NO TERMINAL ---
    nomes_bairros = []
    contagem_familias = []

    for chave, dados in cadastro_geral.items():
        if isinstance(dados, dict) and "ESTATISTICA" not in chave:
            nomes_bairros.append(chave)
            contagem_familias.append(len(dados))

    if not contagem_familias:
        print("⚠️ Sem dados de bairros para o gráfico. Sincronize (Opção 5) primeiro.")
        return

    print("🔄 Puxando dados oficiais de São Luís...")
    dados_api = buscar_beneficios_municipio("2111300", "202601")
    
    texto_api = "Dados Oficiais indisponíveis."
    if dados_api and len(dados_api) > 0:
        res = dados_api[0]
        qtd = res.get('quantidadeBeneficiarios') or res.get('quantidadeBeneficiados') or 0
        valor = res.get('valor', 0)
        texto_api = f"PORTAL DA TRANSPARÊNCIA (SLZ):\nFamílias: {qtd} | Investimento: R$ {valor:,.2f}"

    plt.figure(figsize=(12, 7))
    cores = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6']
    barras = plt.bar(nomes_bairros, contagem_familias, color=cores[:len(nomes_bairros)])
    
    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval + 1, f'{int(yval)}', ha='center', va='bottom')

    plt.title('Vigilant: Monitoramento de Clusters de Vulnerabilidade (N=1.200)', fontsize=14, fontweight='bold')
    plt.figtext(0.5, 0.01, texto_api, ha="center", bbox={"facecolor":"orange", "alpha":0.2, "pad":5})
    plt.tight_layout()
    plt.show()

def gerar_mapa_interativo(cadastro_geral):
    print("🌍 Gerando Mapa de Risco de São Luís (Versão Final Completa)...")
    
    # 1. CRIAÇÃO DO MAPA (Base)
    mapa = folium.Map(location=[-2.5307, -44.3068], zoom_start=12)
    dados_calor = []

    # --- CAMADA: GEOFENCING DE 3 NÍVEIS (Retângulos Fixos) ---
    # Coordenadas calibradas para Anil e Bacanga
    zona_critica = [[-2.5450, -44.2980], [-2.5200, -44.2700]] # Anil/Liberdade
    folium.Rectangle(
        bounds=zona_critica, color="red", weight=3, fill=True, fill_color="red", fill_opacity=0.2,
        popup="🚨 ZONA CRÍTICA"
    ).add_to(mapa)

    folium.Rectangle(
        bounds=[[-2.5850, -44.3150], [-2.5500, -44.2900]], # Bacanga
        color="red", weight=3, fill=True, fill_color="red", fill_opacity=0.2,
        popup="🚨 ZONA CRÍTICA"
    ).add_to(mapa)

    # Perímetro de Monitoramento (Buffer Tracejado Amarelo/Laranja)
    folium.Rectangle(
        bounds=[[-2.6000, -44.3300], [-2.5100, -44.2600]], color="orange", weight=1, fill=False,
        dash_array='10, 10', popup="⚠️ PERÍMETRO DE MONITORAMENTO"
    ).add_to(mapa)
    # ---------------------------------------------------------

    # 2. RENDERIZAÇÃO DOS DADOS (Onde estava o erro)
    for bairro, familias in cadastro_geral.items():
        if not isinstance(familias, dict) or "ESTATISTICA" in bairro:
            continue
            
        for id_f, info in familias.items():
            if isinstance(info, dict) and "coords" in info:
                dados_calor.append(info["coords"])
                
                # --- CORREÇÃO: LÓGICA DE CORES DOS ÍCONES ---
                # Pega a prioridade. Se não tiver, assume "NORMAL".
                prioridade = info.get("prioridade", "NORMAL").upper()
                
                if prioridade == "CRÍTICO" or prioridade == "ALTA":
                    cor_ponto = "red" # Vermelho para o Garcia e zonas críticas
                elif prioridade == "ALERTA" or prioridade == "MEDIA":
                    cor_ponto = "orange" # Amarelo/Laranja para Proximidade
                else:
                    cor_ponto = "blue" # Azul para Comum
                # ----------------------------------------------
                
                # Desenha o Marcador com a cor correta
                folium.CircleMarker(
                    location=info["coords"],
                    radius=6, color=cor_ponto, fill=True, fill_opacity=0.8,
                    popup=f"<b>Família:</b> {info['nome']}<br><b>Prioridade:</b> {info['prioridade']}"
                ).add_to(mapa)

    # 3. NOVIDADE: CAMADA DE CALOR (O "efeito visual" que sumiu)
    if dados_calor:
        print("🔥 Adicionando Mapa de Calor...")
        # radius=20 e blur=15 criam manchas visíveis no mapa
        HeatMap(dados_calor, radius=20, blur=15).add_to(mapa)
        
    mapa.save("mapa_seguranca_alimentar.html")
    print("✅ Mapa gerado com TODAS as camadas (Calor, Marcadores Coloridos e Geofencing)!")