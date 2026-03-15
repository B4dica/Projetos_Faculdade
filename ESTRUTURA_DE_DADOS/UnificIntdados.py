# 1. Importe todas as funções que você criou no arquivo Geo
from GeolocIntelij import (
    inicializar_gmaps, 
    buscar_endereco, 
    extrair_dados_limpos,
    buscar_endereco_regiao_metropolitana,
    extrair_cidade_e_bairro,
    avaliar_prioridade_geografica                
)
import os
import json # <--- Importante estar aqui
from dotenv import load_dotenv
from relatorios import exibir_ranking_bairros

# Importe a função do arquivo de gráficos
from gráficos import grafico_comparativo_cidades

load_dotenv()
gmaps_cliente = inicializar_gmaps()

# -------------------------------------------------------------
# LÓGICA DE CARREGAMENTO (A "Memória" do Sistema)
# -------------------------------------------------------------
# Tenta ler os dados salvos quando o programa inicia
try:
    with open("cadastro_familias.json", "r", encoding="utf-8") as arquivo:
        cadastro_geral = json.load(arquivo)
        print("📦 Memória restaurada: Dados do JSON carregados com sucesso!")
except FileNotFoundError:
    # Se for a primeira vez rodando e o arquivo não existir, usa dados de teste
    print("⚠️ Primeiro acesso: Iniciando banco com dados de teste.")
    cadastro_geral = {
        "Centro": {
            "NIS-001": {
                "nome": "Maria Silva",
                "cidade": "São Luís",
                "bairro": "Centro", # <--- Faltava isso aqui!
                "coords": [-2.5278493, -44.3033239]
            }
        },
        "Maiobão": {
            "NIS-002": {
                "nome": "José Ribamar",
                "cidade": "Paço do Lumiar",
                "bairro": "Maiobão", # <--- Faltava isso aqui!
                "coords": [-2.5392866, -44.1743995]
            }
        },
        "Não Identificado": {
            "NIS-003": {
                "nome": "Ana Clara",
                "cidade": "São José de Ribamar",
                "bairro": "Não Identificado", # <--- Faltava isso aqui!
                "coords": [-2.4894791, -44.0385431]
            }
        }
    }
# -------------------------------------------------------------

    # ... (o resto do seu código continua normal daqui para baixo) ...
def cadastrar_na_ilha(id_f, nome, endereco, cidade_alvo):
    res_bruto = buscar_endereco_regiao_metropolitana(gmaps_cliente, endereco, cidade_alvo)
    dados_geo = extrair_cidade_e_bairro(res_bruto)
    
    if dados_geo:
        bairro_real = dados_geo["bairro"]
        lat, lng = dados_geo["lat"], dados_geo["lng"]
        
        # --- NOVIDADE: MAPEAMENTO DE RISCO ---
        situacao_geo, nivel_prioridade = avaliar_prioridade_geografica(lat, lng)
        # -------------------------------------
        
        if bairro_real not in cadastro_geral:
            cadastro_geral[bairro_real] = {}
            
        cadastro_geral[bairro_real][id_f] = {
            "nome": nome,
            "cidade": dados_geo["cidade"],
            "coords": (lat, lng),
            "situacao": situacao_geo,      # Salva se é ribeirinha, palafita, etc.
            "prioridade": nivel_prioridade # Define se o atendimento deve ser urgente
        }
        print(f"✅ {nome} cadastrado!")
        print(f"📢 Alerta de Zona: {situacao_geo} | Prioridade: {nivel_prioridade}")
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
                print("📊 Gerando visualização de dados...")
                grafico_comparativo_cidades(cadastro_geral) # O gráfico que você já tem
                
                # CHAMADA NOVA PARA O FOLIUM:
                from gráficos import gerar_mapa_interativo
                gerar_mapa_interativo(cadastro_geral)
            else:
                print("⚠️ Sem dados para gerar mapas.")

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


# Tenta ler os dados salvos quando o programa inicia
try:
    with open("cadastro_familias.json", "r", encoding="utf-8") as arquivo:
        cadastro_geral = json.load(arquivo)
        print("📦 Memória restaurada: Dados do JSON carregados com sucesso!")
except FileNotFoundError:
    # Se for a primeira vez rodando e o arquivo não existir, usa dados de teste
    print("⚠️ Primeiro acesso: Iniciando banco com dados de teste.")

if __name__ == "__main__":
    # O sistema já carregou os dados lá em cima, então é só abrir o menu direto!
    menu_principal()
