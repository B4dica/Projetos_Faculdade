
import json
import random
from GeolocIntelij import avaliar_prioridade_geografica

def exibir_ranking_bairros(cadastro_geral):
    contagem_bairros = {}

    for local, familias in cadastro_geral.items():
        # Verifica se 'familias' é realmente um dicionário de cadastros
        if isinstance(familias, dict):
            for id_f, dados_familia in familias.items():
                # .get() evita o KeyError: se não achar "bairro", retorna "Não Informado"
                nome_do_bairro = dados_familia.get("bairro", "Não Informado")

                if nome_do_bairro not in contagem_bairros:
                    contagem_bairros[nome_do_bairro] = 0
                contagem_bairros[nome_do_bairro] += 1

    if not contagem_bairros:
        print("⚠️ Nenhum dado cadastrado para gerar o ranking.")
        return

    ranking_ordenado = sorted(contagem_bairros.items(), key=lambda item: item[1], reverse=True) #O(n log n)

    print("\n" + "="*45)
    print("🚨 RANKING DE NECESSIDADE POR BAIRRO 🚨")
    print("="* 45)

# enumerate(..., 1) nos ajuda a colocar a posição (1º, 2º, 3º...) automaticamente
    for posicao, (bairro, quantidade) in enumerate(ranking_ordenado, 1):
        print(f"{posicao}º Lugar | {bairro}: {quantidade} famílias mapeadas")
    print("="*45 + "\n")



def salvar_dados_json(cadastro_geral):
    try:
        with open("cadastro_familias.json", "w", encoding="utf-8") as arquivo:
            # indent=4 deixa o arquivo bonito para ler
            # ensure_ascii=False garante que acentos como 'ã' e 'í' funcionem
            json.dump(cadastro_geral, arquivo, indent=4, ensure_ascii=False)
        print("💾 Dados salvos com sucesso em 'cadastro_familias.json'!")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")

def simular_dados_transparencia(total_real=117700):
    """
    Simula a disparidade real de São Luís baseada no desafio UNDB 4.0.
    Ajustado para gerar quantidades DIFERENTES por bairro.
    """
    distribuicao = {
        "Cidade Olímpica": 0.35,  
        "Anjo da Guarda": 0.25,   
        "Coroadinho": 0.15,       
        "Vila Maranhão": 0.10,    
        "Alemanha": 0.08,         
        "Centro": 0.07            
    }

    dados_simulados = {}
    coords_base = {
        "Cidade Olímpica": [-2.578, -44.205],
        "Anjo da Guarda": [-2.558, -44.315],
        "Vila Maranhão": [-2.633, -44.322],
        "Coroadinho": [-2.551, -44.270],
        "Centro": [-2.527, -44.303],
        "Alemanha": [-2.535, -44.278]
    }

    # Fator de escala para não travar o PC, mas manter a proporção
    # Aqui vamos gerar cerca de 1177 registros no total (1% do real)
    escala = 0.01 

    for bairro, proporcao in distribuicao.items():
        dados_simulados[bairro] = {}
        
        # CÁLCULO DA QUANTIDADE POR BAIRRO (O segredo está aqui!)
        qtd_bairro = int(total_real * proporcao * escala)

        for i in range(qtd_bairro): 
            id_f = f"GOV-{random.randint(100000, 999999)}"
            
            lat = coords_base[bairro][0] + random.uniform(-0.012, 0.012)
            lng = coords_base[bairro][1] + random.uniform(-0.012, 0.012)

            situacao, prioridade_real = avaliar_prioridade_geografica(lat, lng)

            dados_simulados[bairro][id_f] = {
                "nome": f"Cadastro Base {i}",
                "bairro": bairro,
                "coords": [lat, lng],
                "prioridade": prioridade_real,
                "situacao": situacao,
                "data_cadastro": "01/2026" 
            }
            
    return dados_simulados

def identificar_lacunas_atendimento(cadastro_geral):
    """
    Usa a estrutura de dados SET (Conjuntos) para encontrar bairros sem assistência.
    Exigência do desafio UNDB 4.0.
    """
    todos_bairros_slz = {"Cidade Olímpica", "Anjo da Guarda", "Vila Maranhão", 
                         "Coroadinho", "Centro", "Alemanha", "Cohab", "Cohatrac", "Renascença"}
    
    # Pega apenas os bairros que já têm famílias cadastradas no sistema
    bairros_com_cadastro = set(cadastro_geral.keys())
    
    # Operação de DIFERENÇA entre conjuntos
    lacunas = todos_bairros_slz - bairros_com_cadastro
    
    print("\n" + "🔍 ANÁLISE DE LACUNAS (SET DIFFERENCE)")
    print(f"Bairros ainda não mapeados: {lacunas if lacunas else 'Todos atendidos!'}")