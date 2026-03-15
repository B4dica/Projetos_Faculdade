import matplotlib.pyplot as plt

def grafico_comparativo_cidades(cadastro_geral):
    # Filtra apenas cidades que possuem alguém cadastrado para o gráfico não ficar vazio
    cidades = [c for c in cadastro_geral.keys() if len(cadastro_geral[c]) > 0]
    totais = [len(cadastro_geral[c]) for c in cidades]
    
    if not totais:
        print("⚠️ Sem dados para gerar o gráfico comparativo.")
        return

    plt.figure(figsize=(8, 5))
    cores = ['#1f77b4', '#ff7f0e', '#2ca02c'] # Cores distintas
    
    plt.bar(cidades, totais, color=cores[:len(cidades)])
    plt.title('Distribuição de Assistência na Região Metropolitana')
    plt.ylabel('Quantidade de Famílias')
    plt.xlabel('Municípios')
    
    # Ajusta para os nomes não sumirem
    plt.tight_layout()
    plt.show()

import folium


def gerar_mapa_interativo(cadastro_geral):
    mapa = folium.Map(location=[-2.5307, -44.3068], zoom_start=12)

    # --- DESENHANDO ZONAS DE RISCO ---
    # Rio Anil
    folium.Rectangle(
        bounds=[[-2.535, -44.290], [-2.520, -44.260]],
        color='red', fill=True, fill_opacity=0.2, popup='Risco: Rio Anil'
    ).add_to(mapa)

    # Rio Bacanga
    folium.Rectangle(
        bounds=[[-2.570, -44.310], [-2.545, -44.285]],
        color='red', fill=True, fill_opacity=0.2, popup='Risco: Rio Bacanga'
    ).add_to(mapa)

    for local, familias in cadastro_geral.items():
        if isinstance(familias, dict):
            for id_f, dados in familias.items():
                if "coords" in dados:
                    lat, lng = dados['coords']
                    cor = 'red' if dados.get('prioridade') == 'ALTA' else 'blue'
                    
                    folium.Marker(
                        [lat, lng],
                        popup=f"Família: {dados['nome']}<br>Bairro: {dados.get('bairro')}",
                        icon=folium.Icon(color=cor, icon='info-sign')
                    ).add_to(mapa)

    mapa.save("mapa_seguranca_alimentar.html")
    print("🌐 Mapa com Zonas de Risco gerado!")