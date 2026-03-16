import os
import json 
from dotenv import load_dotenv
from GeolocIntelij import (
    inicializar_gmaps, 
    buscar_endereco_regiao_metropolitana,
    extrair_cidade_e_bairro,
    avaliar_prioridade_geografica,                
)
from relatorios import exibir_ranking_bairros, salvar_dados_json
from gráficos import grafico_comparativo_cidades
from visualizacao_mapa import gerar_mapa_interativo

load_dotenv()
gmaps_cliente = inicializar_gmaps()

# --- CARREGAMENTO DE DADOS ---
try:
    with open("cadastro_familias.json", "r", encoding="utf-8") as arquivo:
        cadastro_geral = json.load(arquivo)
        print("📦 Memória restaurada: Dados do JSON carregados com sucesso!")
except (FileNotFoundError, json.JSONDecodeError):
    print("⚠️ Banco de dados não encontrado ou vazio. Iniciando novo cadastro.")
    cadastro_geral = {}

def cadastrar_na_ilha(id_f, nome, endereco, cidade_alvo):
    res_bruto = buscar_endereco_regiao_metropolitana(gmaps_cliente, endereco, cidade_alvo)
    dados_geo = extrair_cidade_e_bairro(res_bruto)
    
    if dados_geo:
        bairro_real = dados_geo["bairro"]
        lat, lng = dados_geo["lat"], dados_geo["lng"]
        situacao_geo, nivel_prioridade = avaliar_prioridade_geografica(lat, lng)
        
        if bairro_real not in cadastro_geral:
            cadastro_geral[bairro_real] = {}
            
        cadastro_geral[bairro_real][id_f] = {
            "nome": nome,
            "cidade": dados_geo["cidade"],
            "bairro": bairro_real,         
            "coords": [lat, lng],          
            "situacao": situacao_geo,
            "prioridade": nivel_prioridade
        }
        print(f"✅ {nome} cadastrado com sucesso!")

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("🍽️  SISTEMA DE SEGURANÇA ALIMENTAR - GRANDE ILHA")
        print("="*50)
        print("1. Cadastrar Nova Família")
        print("2. Gerar Gráfico de Assistência")
        print("3. Exibir Ranking de Bairros")
        print("4. Gerar Mapa Interativo (Zonas de Risco) 🗺️")
        print("5. Sair e Salvar 💾")
        print("="*50)
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            id_f = input("NIS/CPF da Família: ")
            nome = input("Nome do Responsável: ")
            endereco = input("Endereço: ")
            cidade_alvo = input("Cidade: ")
            cadastrar_na_ilha(id_f, nome, endereco, cidade_alvo)

        elif opcao == "2":
            grafico_comparativo_cidades(cadastro_geral)

        elif opcao == "3":
            exibir_ranking_bairros(cadastro_geral)

        elif opcao == "4":
            gerar_mapa_interativo(cadastro_geral) 

        elif opcao == "5":
            salvar_dados_json(cadastro_geral)
            print("💾 Dados salvos. Saindo...")
            break

if __name__ == "__main__":
    menu_principal()