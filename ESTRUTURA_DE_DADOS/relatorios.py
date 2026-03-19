import json
import random
from GeolocIntelij import avaliar_prioridade_geografica

def exibir_ranking_bairros(cadastro_geral):
    # Ranking considerando o volume total de famílias
    contagem = {b: len(f) for b, f in cadastro_geral.items() if isinstance(f, dict)}
    if not contagem:
        print("⚠️ Nenhum dado para gerar o ranking.")
        return
    
    # Ordenação O(n log n)
    ranking = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    print("\n" + "="*45)
    print("🚨 RANKING DE PRIORIDADE POR VOLUME 🚨")
    print("="* 45)
    for pos, (bairro, quantidade) in enumerate(ranking, 1):
        print(f"{pos}º Lugar | {bairro}: {quantidade} famílias mapeadas")
    print("="*45 + "\n")

def salvar_dados_json(cadastro_geral):
    try:
        with open("cadastro_familias.json", "w", encoding="utf-8") as arquivo:
            json.dump(cadastro_geral, arquivo, indent=4, ensure_ascii=False)
        print("💾 Base de dados unificada salva com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")

def simular_dados_transparencia(total_real=117700):
    """
    Sua Simulação Proporcional: Gera disparidade real para gráficos e mapa.
    Agora inclui Renda Per Capita realista baseada na Transparência.
    """
    # Proporções de vulnerabilidade para os bairros de São Luís
    distribuicao = {
        "Cidade Olímpica": 0.35, "Anjo da Guarda": 0.25, 
        "Coroadinho": 0.15, "Vila Maranhão": 0.10, 
        "Alemanha": 0.08, "Centro": 0.07
    }
    coords_base = {
        "Cidade Olímpica": [-2.578, -44.205], "Anjo da Guarda": [-2.558, -44.315],
        "Vila Maranhão": [-2.633, -44.322], "Coroadinho": [-2.551, -44.270],
        "Centro": [-2.527, -44.303], "Alemanha": [-2.535, -44.278]
    }
    
    dados_simulados = {}
    
    # Fator de escala para não travar o PC (amostra de 1%)
    # Geramos cerca de 1177 registros no total
    escala = 0.05 
    
    for bairro, proporcao in distribuicao.items():
        dados_simulados[bairro] = {}
        
        # CÁLCULO DA QUANTIDADE POR BAIRRO (Ajustado para o gráfico)
        qtd_bairro = int(total_real * proporcao * escala)
        
        for i in range(qtd_bairro): 
            id_f = f"GOV-{random.randint(100000, 999999)}"
            lat = coords_base[bairro][0] + random.uniform(-0.012, 0.012)
            lng = coords_base[bairro][1] + random.uniform(-0.012, 0.012)
            sit, prio_geo = avaliar_prioridade_geografica(lat, lng)
            
            # Adicionando Renda Familiar Proporcional (Média de vulnerabilidade social)
            # Famílias da base Gov têm renda entre 150 e 650 por pessoa.
            renda_per_capita = random.uniform(150, 650)
            
            # Lógica de Aluguel (Simulando que 40% das famílias pagam aluguel)
            mora_aluguel = random.random() < 0.40
            
            dados_simulados[bairro][id_f] = {
                "nome": f"Base Gov {i}", "bairro": bairro,
                "coords": [lat, lng], "prioridade": prio_geo,
                "situacao": sit, "renda_capita": round(renda_per_capita, 2),
                "aluguel": mora_aluguel,
                "data_cadastro": "01/2026" 
            }
            
    return dados_simulados