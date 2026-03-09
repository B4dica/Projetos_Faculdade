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

# 2. Importe a função do arquivo de gráficos
from gráficos import grafico_comparativo_cidades

load_dotenv()
gmaps_cliente = inicializar_gmaps() # Use o nome gmaps_cliente para ser consistente

# Estrutura de dados para as 3 cidades
cadastro_geral = {
    "Cidade Olímpica": {},
    "Vila Maranhão": {},
    "Anjo da Guarda": {} # ("joao",19,'São luis',9291): 15231637
}

def cadastrar_na_ilha(id_f, nome, endereco, cidade_alvo):
    res_bruto = buscar_endereco_regiao_metropolitana(gmaps_cliente, endereco, cidade_alvo)
    dados_geo = extrair_cidade_e_bairro(res_bruto)
    
    if dados_geo:
        # MUDANÇA AQUI: Usamos o bairro oficial retornado pelo Google
        bairro_real = dados_geo["bairro"]
        
        # Se o bairro não estiver no nosso dicionário inicial, nós o adicionamos
        if bairro_real not in cadastro_geral:
            cadastro_geral[bairro_real] = {}
            
        cadastro_geral[bairro_real][id_f] = {
            "nome": nome,
            "cidade": dados_geo["cidade"], # Guardamos a cidade dentro, mas a chave é o bairro
            "coords": (dados_geo["lat"], dados_geo["lng"])
        }
        print(f"✅ {nome} cadastrado com sucesso no bairro: {bairro_real}")
    else:
        print(f"❌ Erro ao localizar: {endereco}")
# ... (seus imports continuam iguais aqui) ...

def menu_principal():
    while True:
        print("\n--- SISTEMA DE SEGURANÇA ALIMENTAR - GRANDE ILHA ---")
        print("1. Cadastrar Nova Família")
        print("2. Gerar Gráfico de Assistência")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            # Coleta os dados via teclado
            id_f = input("NIS/CPF da Família: ")
            nome = input("Nome do Responsável: ")
            endereco = input("Endereço (Rua, nº, Ref): ")
            
            print("\nCidades Alvo: Cidade Olímpica, Vila Maranhão, Anjo da Guarda")
            cidade_alvo = input("Cidade de Referência: ")
            
            # Chama sua função que já usa o Google Maps
            cadastrar_na_ilha(id_f, nome, endereco, cidade_alvo)

        elif opcao == "2":
            if any(cadastro_geral.values()): # Verifica se há alguém cadastrado
                print("📊 Gerando visualização de dados...")
                grafico_comparativo_cidades(cadastro_geral)
            else:
                print("⚠️ Nenhum dado cadastrado para gerar gráficos.")

        elif opcao == "3":
            print("Encerrando sistema... Dados salvos na memória.")
            break
        else:
            print("❌ Opção inválida!")

# Substitua seus testes manuais por:
if __name__ == "__main__":
    menu_principal()