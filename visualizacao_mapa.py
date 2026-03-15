import folium

def gerar_mapa_interativo(cadastro_geral):
    # Coordenadas centrais de São Luís para iniciar o mapa
    # O zoom_start=12 é o ideal para apanhar toda a ilha
    mapa = folium.Map(location=[-2.5307, -44.3068], zoom_start=12)

    tem_dados = False

    # Varremos todas as cidades e famílias no nosso dicionário principal
    for cidade, cadastros_da_cidade in cadastro_geral.items():
        for id_f, info in cadastros_da_cidade.items():
            
            # Verificamos se a família tem coordenadas válidas (lat e lng) guardadas numa tupla ou lista
            if "coords" in info and len(info["coords"]) == 2:
                lat, lng = info["coords"]
                nome = info.get("nome", "Desconhecido")
                bairro = info.get("bairro", cidade)
                
                # Criamos o HTML simples do balão (popup) que vai aparecer ao clicar
                popup_texto = f"<b>Família:</b> {nome}<br><b>Bairro:</b> {bairro}<br><b>Zona:</b> {cidade}"
                
                # Definimos a cor do pino baseada numa lógica (ex: vermelho para destacar)
                cor_pino = "red"
                
                # Adicionamos o marcador ao mapa
                folium.Marker(
                    location=[lat, lng],
                    popup=folium.Popup(popup_texto, max_width=300),
                    icon=folium.Icon(color=cor_pino, icon="info-sign")
                ).add_to(mapa)
                
                tem_dados = True

    if tem_dados:
        # Geramos e guardamos o ficheiro HTML dinamicamente
        ficheiro_html = "mapa_seguranca_alimentar.html"
        mapa.save(ficheiro_html)
        print(f"\n🗺️ Mapa atualizado com sucesso! Abra o ficheiro '{ficheiro_html}' no seu navegador para ver as zonas de risco.")
    else:
        print("\n⚠️ Não existem coordenadas válidas no sistema para gerar o mapa.")
