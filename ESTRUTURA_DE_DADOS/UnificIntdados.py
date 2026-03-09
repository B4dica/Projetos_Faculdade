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
    # Chamando a função correta do GeolocIntelij
    res_bruto = buscar_endereco_regiao_metropolitana(gmaps_cliente, endereco, cidade_alvo)
    dados_geo = extrair_cidade_e_bairro(res_bruto)
    
    if dados_geo:
        cidade_real = dados_geo["cidade"]
        
        # Se o Google retornar uma cidade que não previmos (ex: Raposa), criamos a chave
        if cidade_real not in cadastro_geral:
            cadastro_geral[cidade_real] = {}
            
        cadastro_geral[cidade_real][id_f] = {
            "nome": nome,
            "bairro": dados_geo["bairro"],
            "coords": (dados_geo["lat"], dados_geo["lng"])
        }
        print(f"✅ {nome} cadastrado em {cidade_real} ({dados_geo['bairro']})")
    else:
        print(f"❌ Erro ao localizar: {endereco}")

# --- TESTE PRÁTICO COM AS 3 CIDADES ---
cadastrar_na_ilha("NIS-001", "Maria Silva", "Rua do Egito, Centro", "Cidade Olímpica")
cadastrar_na_ilha("NIS-002", "José Ribamar", "Maiobão", "Vila Maranhão")
cadastrar_na_ilha("NIS-003", "Ana Clara", "Praia de Panaquatira", "Anjo da Guarda")

# --- GERAR O GRÁFICO FINAL ---
grafico_comparativo_cidades(cadastro_geral)