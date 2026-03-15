import folium

def gerar_mapa_interativo(cadastro_geral):
    # Centralizado em São Luís
    mapa = folium.Map(location=[-2.5307, -44.3068], zoom_start=12)

    # --- DESENHANDO AS ZONAS DE RISCO (RETÂNGULOS) ---
    
    # Área 1: Proximidades do Rio Anil
    folium.Rectangle(
        bounds=[[-2.535, -44.290], [-2.520, -44.260]],
        color='red',
        fill=True,
        fill_opacity=0.3,
        popup='ZONA DE RISCO: Bacia do Rio Anil'
    ).add_to(mapa)

    # Área 2: Proximidades do Rio Bacanga
    folium.Rectangle(
        bounds=[[-2.570, -44.310], [-2.545, -44.285]],
        color='red',
        fill=True,
        fill_opacity=0.3,
        popup='ZONA DE RISCO: Bacia do Rio Bacanga'
    ).add_to(mapa)

    # --- ADICIONANDO OS MARCADORES DAS FAMÍLIAS ---
    for bairro, familias in cadastro_geral.items():
        # Verifica se 'familias' é um dicionário (estrutura NIS: dados)
        if isinstance(familias, dict):
            for id_f, dados in familias.items():
                if "coords" in dados:
                    lat, lng = dados['coords']
                    
                    # Define a cor do pino: vermelho se estiver em risco, azul se não
                    cor_pino = 'red' if dados.get('prioridade') == 'ALTA' else 'blue'
                    
                    folium.Marker(
                        location=[lat, lng],
                        popup=f"<b>Família:</b> {dados['nome']}<br><b>Prioridade:</b> {dados.get('prioridade')}",
                        icon=folium.Icon(color=cor_pino, icon='home')
                    ).add_to(mapa)

    # Salva o arquivo final
    mapa.save("mapa_seguranca_alimentar.html")
    print("\n🌐 Mapa atualizado com Zonas de Risco! Abra o arquivo HTML para conferir.")