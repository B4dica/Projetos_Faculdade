
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
