# 1. Importe todas as funções que você criou no arquivo Geo
from GeolocIntelij import (
    inicializar_gmaps, 
    buscar_endereco, 
    extrair_dados_limpos,
    buscar_endereco_regiao_metropolitana, # Nova
    extrair_cidade_e_bairro                # Nova
)
import os
from dotenv import load_dotenv
from relatorios import exibir_ranking_bairros

# 2. Importe a função do arquivo de gráficos
from gráficos import grafico_comparativo_cidades

load_dotenv()
gmaps_cliente = inicializar_gmaps() # Use o nome gmaps_cliente para ser consistente

# Estrutura de dados para as 3 cidades
cadastro_geral = {
    "Cidade Olímpica": {},
    "Vila Maranhão": {},
    "Anjo da Guarda": {} 
}

def cadastrar_na_ilha(id_f, nome, endereco, cidade_alvo):
    res_bruto = buscar_endereco_regiao_metropolitana(gmaps_cliente, endereco, cidade_alvo)
    dados_geo = extrair_cidade_e_bairro(res_bruto)
    
    if dados_geo:
        # MUDANÇA AQUI: Usamos o bairro oficial retornado pelo Google
        bairro_real = dados_geo["bairro"]
        
        # Se o bairro não estiver no nosso dicionário inicial, nós o adicionamos
        if bairro_real not in cadastro_geral:
            cadastro_geral[bairro_real] = {} # cadastro_geral = {bairro_real = {}}
            
        cadastro_geral[bairro_real][id_f] = { #cadastro_geral = {bairro_real = {id_f = {}}}
            "nome": nome,
            "cidade": dados_geo["cidade"], # Guardamos a cidade dentro, mas a chave é o bairro
            "coords": (dados_geo["lat"], dados_geo["lng"]), #cadastro_geral = {bairro_real = {id_f = {"nome":nome, "cidade": cidade}}}
            "bairro":  bairro_real
        }
        print(f"✅ {nome} cadastrado com sucesso no bairro: {bairro_real}")
    else:
        print(f"❌ Erro ao localizar: {endereco}")
# ... (seus imports continuam iguais aqui) ...


# ... (seus imports continuam iguais)

def menu_principal():
    while True:
        print("\n--- SISTEMA DE SEGURANÇA ALIMENTAR - GRANDE ILHA ---")
        print("1. Cadastrar Nova Família")
        print("2. Gerar Gráfico de Assistência")
        print("3. Exibir Ranking de Bairros (NOVO)") # Adicione esta linha
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            id_f = input("NIS/CPF da Família: ")
            nome = input("Nome do Responsável: ")
            endereco = input("Endereço (Rua, nº, Ref): ")
            cidade_alvo = input("Cidade de Referência: ")
            cadastrar_na_ilha(id_f, nome, endereco, cidade_alvo)

        elif opcao == "2":
            if any(cadastro_geral.values()):
                grafico_comparativo_cidades(cadastro_geral)
            else:
                print("⚠️ Sem dados para gráficos.")

        elif opcao == "3": # Nova opção para chamar seu relatório
            exibir_ranking_bairros(cadastro_geral)

        elif opcao == "4": # Supondo que 4 seja o Sair
            print("Encerrando sistema...")
            # Chamada para salvar o JSON antes de fechar tudo
            from relatorios import salvar_dados_json # Se você colocou a função lá
            salvar_dados_json(cadastro_geral)
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    # COLOQUE OS TESTES AQUI DENTRO! 
    # Assim eles rodam assim que você der o play, mas não quebram o código.
    print("--- INICIALIZANDO TESTES AUTOMÁTICOS ---")
    cadastrar_na_ilha("NIS-001", "Maria Silva", "Rua do Egito, Centro", "São Luís")
    cadastrar_na_ilha("NIS-002", "José Ribamar", "Maiobão", "Paço do Lumiar")
    cadastrar_na_ilha("NIS-003", "Ana Clara", "Praia de Panaquatira", "São José de Ribamar")
    
    # Depois dos testes, ele abre o menu para você usar
    menu_principal()