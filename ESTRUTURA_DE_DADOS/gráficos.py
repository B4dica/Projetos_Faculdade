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
    print("🌍 Gerando Mapa de Risco com Controle de Camadas...")
    
    mapa = folium.Map(location=[-2.5307, -44.3068], zoom_start=12)
    dados_calor = []

    # --- 1. GRUPOS DE CAMADAS (Para o Botão funcionar) ---
    camada_risco = folium.FeatureGroup(name="🚨 Zonas de Risco (Geofencing)")
    camada_indicadores = folium.FeatureGroup(name="📍 Indicadores de Famílias", show=True)
    
    # --- 2. ADICIONANDO AS ZONAS DE RISCO AO GRUPO ---
    folium.Rectangle(
        bounds=[[-2.5450, -44.2980], [-2.5200, -44.2700]], 
        color="red", fill=True, fill_opacity=0.2, popup="Rio Anil"
    ).add_to(camada_risco)

    folium.Rectangle(
        bounds=[[-2.5850, -44.3150], [-2.5500, -44.2900]], 
        color="red", fill=True, fill_opacity=0.2, popup="Rio Bacanga"
    ).add_to(camada_risco)

    # --- 3. PROCESSANDO FAMÍLIAS E ADICIONANDO AO GRUPO DE INDICADORES ---
    for bairro, familias in cadastro_geral.items():
        if not isinstance(familias, dict) or "ESTATISTICA" in bairro:
            continue
            
        for id_f, info in familias.items():
            if isinstance(info, dict) and "coords" in info:
                dados_calor.append(info["coords"])
                
                prioridade = info.get("prioridade", "NORMAL").upper()
                cor_ponto = "red" if prioridade in ["CRÍTICO", "ALTA"] else "orange" if prioridade in ["ALERTA", "MEDIA"] else "blue"
                
                folium.CircleMarker(
                    location=info["coords"],
                    radius=6, color=cor_ponto, fill=True, fill_opacity=0.8,
                    popup=f"<b>Família:</b> {info['nome']}<br><b>Prioridade:</b> {info['prioridade']}"
                ).add_to(camada_indicadores)

    # --- 4. CAMADA DE CALOR (HEATMAP) ---
    if dados_calor:
        # Criamos o HeatMap como uma camada separada
        camada_calor = HeatMap(dados_calor, name="🔥 Mapa de Calor (Densidade)", radius=20, blur=15, show=False)
        camada_calor.add_to(mapa)

    # --- 5. ADICIONANDO TUDO AO MAPA E O BOTÃO DE CONTROLE ---
    camada_risco.add_to(mapa)
    camada_indicadores.add_to(mapa)

    # O COMANDO MÁGICO: Adiciona o seletor no canto superior direito
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    mapa.save("mapa_seguranca_alimentar.html")
    print("✅ Mapa gerado! Agora você pode alternar as camadas no canto superior direito.")