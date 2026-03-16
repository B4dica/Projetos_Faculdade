import matplotlib.pyplot as plt

def grafico_comparativo_cidades(cadastro_geral):
    nomes_bairros = []
    contagem_familias = []

    # 1. Coleta os dados garantindo que estamos contando os NIS
    for bairro, familias in cadastro_geral.items():
        if isinstance(familias, dict):
            quantidade = len(familias)
            if quantidade > 0: # Só adiciona ao gráfico se tiver gente
                nomes_bairros.append(bairro)
                contagem_familias.append(quantidade)

    if not contagem_familias:
        print("⚠️ Sem dados válidos para gerar o gráfico.")
        return

    # 2. Gera o gráfico
    plt.figure(figsize=(10, 6))
    # Cores repetidas caso tenha muitos bairros
    cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'] * 2
    
    barras = plt.bar(nomes_bairros, contagem_familias, color=cores[:len(nomes_bairros)])
    
    # 3. Adiciona os números em cima das barras (com trava de segurança para o erro)
    for barra in barras:
        yval = barra.get_height()
        if yval > 0:
            plt.text(
                barra.get_x() + barra.get_width()/2, 
                yval + 0.05, 
                f'{int(yval)}', # Formata como string diretamente
                ha='center', 
                va='bottom', 
                fontweight='bold',
                fontsize=11
            )

    plt.title('Distribuição de Famílias por Bairro', fontsize=14)
    plt.ylabel('Quantidade de Famílias', fontsize=12)
    plt.ylim(0, max(contagem_familias) + 1) # Dá um espaço no topo para o número não sumir
    plt.xticks(rotation=45, ha='right')
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