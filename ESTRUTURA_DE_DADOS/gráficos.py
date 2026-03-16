
import matplotlib.pyplot as plt

def grafico_comparativo_cidades(cadastro_geral):
    nomes_bairros = []
    contagem_familias = []

    # Percorre cada bairro e conta quantos NIS existem dentro dele
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
    # Lista de cores para as barras
    cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    # Criando as barras
    barras = plt.bar(nomes_bairros, contagem_familias, color=cores[:len(nomes_bairros)])
    
    # Adicionando os números exatos acima de cada barra
    for barra in barras:
        yval = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width()/2, 
            yval + 0.1, 
            f'{int(yval)}', 
            ha='center', 
            va='bottom', 
            fontweight='bold'
        )

    plt.title('Distribuição Real de Famílias por Bairro', fontsize=14)
    plt.ylabel('Quantidade de Famílias (Registros NIS)')
    plt.xlabel('Bairros Mapeados no Sistema')
    plt.xticks(rotation=45, ha='right')
    # Ajusta o limite do eixo Y para o número não cortar no topo
    plt.ylim(0, max(contagem_familias) + 2)
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