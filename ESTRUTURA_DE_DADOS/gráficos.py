import matplotlib.pyplot as plt
import folium
from folium import plugins # <--- Essencial para o HeatMap e MiniMap

def grafico_comparativo_cidades(cadastro_geral):
    # Lógica de contagem que já corrigimos para mostrar os valores reais (8, 6, 4...)
    nomes_bairros = []
    contagem_familias = []

    for bairro, familias in cadastro_geral.items():
        if isinstance(familias, dict):
            quantidade = len(familias)
            if quantidade > 0:
                nomes_bairros.append(bairro)
                contagem_familias.append(quantidade)

    if not contagem_familias:
        print("⚠️ Sem dados válidos para gerar o gráfico.")
        return

    plt.figure(figsize=(10, 6))
    cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    barras = plt.bar(nomes_bairros, contagem_familias, color=cores[:len(nomes_bairros)])
    
    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval + 0.1, f'{int(yval)}', ha='center', va='bottom', fontweight='bold')

    plt.title('Distribuição Real de Famílias por Bairro', fontsize=14)
    plt.ylabel('Quantidade de Famílias (Registros NIS)')
    plt.xlabel('Bairros Mapeados no Sistema')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(contagem_familias) + 2)
    plt.tight_layout()
    plt.show()

def gerar_mapa_interativo(cadastro_geral):
    """Gera o mapa avançado com HeatMap, Marcadores e Zonas de Risco."""
    # Centralizado em São Luís
    mapa = folium.Map(location=[-2.5307, -44.3068], zoom_start=12)
    
    # Criamos os Grupos de Camadas (Para o menu lateral)
    camada_risco = folium.FeatureGroup(name='Zonas de Risco (Rios)')
    camada_familias = folium.FeatureGroup(name='Marcadores Individuais')
    camada_calor = folium.FeatureGroup(name='Mapa de Calor (Densidade)', show=True)

    dados_calor = []

    # --- PROCESSAMENTO DOS DADOS ---
    for bairro, familias in cadastro_geral.items():
        if isinstance(familias, dict):
            for id_f, dados in familias.items():
                if "coords" in dados:
                    lat, lng = dados['coords']
                    dados_calor.append([lat, lng]) # Adiciona à lista de calor
                    
                    # Marcadores Individuais (Vermelho para ALTA prioridade)
                    cor_pino = 'red' if dados.get('prioridade') == 'ALTA' else 'blue'
                    folium.Marker(
                        location=[lat, lng],
                        popup=folium.Popup(f"<b>Família:</b> {dados['nome']}<br><b>Bairro:</b> {bairro}", max_width=300),
                        icon=folium.Icon(color=cor_pino, icon='home')
                    ).add_to(camada_familias)

    # --- ADICIONANDO O CALOR ---
    if dados_calor:
        plugins.HeatMap(dados_calor, radius=15, blur=10, min_opacity=0.5).add_to(camada_calor)

    # --- ZONAS DE RISCO (Retângulos) ---
    # Rio Anil
    folium.Rectangle(
        bounds=[[-2.535, -44.290], [-2.520, -44.260]],
        color='red', fill=True, fill_opacity=0.2,
        popup='ZONA DE RISCO: Bacia do Rio Anil'
    ).add_to(camada_risco)

    # Rio Bacanga
    folium.Rectangle(
        bounds=[[-2.570, -44.310], [-2.545, -44.285]],
        color='red', fill=True, fill_opacity=0.2,
        popup='ZONA DE RISCO: Bacia do Rio Bacanga'
    ).add_to(camada_risco)

    # Adiciona tudo ao mapa
    camada_calor.add_to(mapa)
    camada_risco.add_to(mapa)
    camada_familias.add_to(mapa)

    # Controle de Camadas e MiniMapa
    folium.LayerControl().add_to(mapa)
    plugins.MiniMap().add_to(mapa)

    mapa.save("mapa_seguranca_alimentar.html")
    print("\n🔥 Mapa de Calor e Zonas de Risco gerados com sucesso!")