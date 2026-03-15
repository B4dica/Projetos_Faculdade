
def exibir_ranking_bairros(cadastro_geral):
    # Dicionário temporário para guardar a contagem. Ex: {"Centro": 5, "Maiobão": 12}
    contagem_bairros = {}

    # 1. Varremos todas as cidades e seus respectivos cadastros
    for cidade, cadastros_da_cidade in cadastro_geral.items():

# Varremos todos os IDs dentro daquela cidade
        for id_f, dados_familia in cadastros_da_cidade.items():

# Pegamos o nome do bairro dessa família específica
            nome_do_bairro = dados_familia["bairro"]

# Se o bairro ainda não está na nossa contagem, adicionamos com valor 0
            if nome_do_bairro not in contagem_bairros:
                contagem_bairros[nome_do_bairro] = 0

# Adicionamos +1 família para este bairro
            contagem_bairros[nome_do_bairro] += 1

    # Se não houver nenhum dado, encerra a função
    if not contagem_bairros:
        print("⚠️ Nenhum dado cadastrado para gerar o ranking.")
        return

    # 3. Ordenamos do maior número de cadastros (mais crítico) para o menor
    ranking_ordenado = sorted(contagem_bairros.items(), key=lambda item: item[1], reverse=True)

    # 4. Exibimos o resultado formatado
    print("\n" + "="*45)
    print("🚨 RANKING DE NECESSIDADE POR BAIRRO 🚨")
    print("="* 45)

# enumerate(..., 1) nos ajuda a colocar a posição (1º, 2º, 3º...) automaticamente
    for posicao, (bairro, quantidade) in enumerate(ranking_ordenado, 1):
        print(f"{posicao}º Lugar | {bairro}: {quantidade} famílias mapeadas")
    print("="*45 + "\n")

import json

def salvar_dados_json(cadastro_geral):
    try:
        with open("cadastro_familias.json", "w", encoding="utf-8") as arquivo:
            # indent=4 deixa o arquivo bonito para ler
            # ensure_ascii=False garante que acentos como 'ã' e 'í' funcionem
            json.dump(cadastro_geral, arquivo, indent=4, ensure_ascii=False)
        print("💾 Dados salvos com sucesso em 'cadastro_familias.json'!")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")