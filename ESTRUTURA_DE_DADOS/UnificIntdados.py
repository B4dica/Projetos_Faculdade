
import json 
from datetime import datetime
from dotenv import load_dotenv

# Importações corrigidas e unificadas
from GeolocIntelij import (
    inicializar_gmaps, 
    buscar_endereco_mestre,  # <--- Nome unificado aqui
    extrair_cidade_e_bairro,
    avaliar_prioridade_geografica,
                 
)
from relatorios import exibir_ranking_bairros, salvar_dados_json, simular_dados_transparencia
from gráficos import grafico_comparativo_cidades, gerar_mapa_interativo

load_dotenv()
gmaps_cliente = inicializar_gmaps()

# --- CARREGAMENTO DE DADOS ---
try:
    with open("cadastro_familias.json", "r", encoding="utf-8") as arquivo:
        cadastro_geral = json.load(arquivo)
        print("📦 Memória restaurada: Dados carregados com sucesso!")
except (FileNotFoundError, json.JSONDecodeError):
    print("⚠️ Banco de dados novo iniciado.")
    cadastro_geral = {}

def cadastrar_na_ilha():
    print("\n" + "-"*30)
    print("📝 NOVO CADASTRO DE FAMÍLIA")
    print("-"*30)
    id_f = input("NIS/CPF da Família: ")
    nome = input("Nome do Responsável: ")
    
    # Otimização: Assume São Luís, diminuindo o esforço do usuário
    endereco_parcial = input("Endereço (Rua, Nº, Bairro ou Ref): ")
    cidade_alvo = "São Luís" 
    
    print(f"🔍 Consultando base do Google Maps...")
    # Chamada corrigida para a função mestre
    res_bruto = buscar_endereco_mestre(gmaps_cliente, endereco_parcial, cidade_alvo)
    
    if not res_bruto:
        print("❌ Localização não encontrada. Tente ser mais específico.")
        return

    # Extração e Confirmação (UX de Segurança)
    dados_geo = extrair_cidade_e_bairro(res_bruto)
    endereco_completo = res_bruto[0].get('formatted_address', 'Endereço não formatado')
    
    print(f"\n📍 O Google encontrou: {endereco_completo}")
    confirmar = input("Confirmar este local para o cadastro? (S/N): ").upper()
    
    if confirmar == 'S' and dados_geo:
        bairro_real = dados_geo["bairro"]
        lat, lng = dados_geo["lat"], dados_geo["lng"]
        
        # Define prioridade baseada nas Zonas de Risco (Geofencing)
        situacao_geo, nivel_prioridade = avaliar_prioridade_geografica(lat, lng)
        data_atual = datetime.now().strftime("%m/%Y") 
        
        if bairro_real not in cadastro_geral:
            cadastro_geral[bairro_real] = {}
            
        cadastro_geral[bairro_real][id_f] = {
            "nome": nome,
            "cidade": dados_geo["cidade"],
            "bairro": bairro_real,         
            "coords": [lat, lng],          
            "situacao": situacao_geo,
            "prioridade": nivel_prioridade,
            "data_cadastro": data_atual
        }
        print(f"✅ Sucesso! {nome} alocado em {bairro_real} (Prioridade: {nivel_prioridade}).")
    else:
        print("🚫 Operação cancelada pelo usuário.")

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("🍽️  SISTEMA DE SEGURANÇA ALIMENTAR - SÃO LUÍS")
        print("="*50)
        print("1. Cadastrar Família (Entrada Manual)")
        print("2. Ver Gráfico de Distribuição por Bairro")
        print("3. Exibir Ranking de Necessidade (Priorização)")
        print("4. Mapa de Calor Geral (Tempo Real)")
        print("5. Histórico: Filtrar Mapa por Período (Mês/Ano) 📅")
        print("6. Sincronizar Portal da Transparência (117.700 registros)")
        print("7. Sair e Salvar Dados 💾")
        print("="*50)
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_na_ilha()
        elif opcao == "2":
            grafico_comparativo_cidades(cadastro_geral)
        elif opcao == "3":
            exibir_ranking_bairros(cadastro_geral)
        elif opcao == "4":
            gerar_mapa_interativo(cadastro_geral) 
        elif opcao == "5":
            periodo = input("Digite o período desejado (Ex: 01/2026): ")
            dados_mes = {}
            for b, fams in cadastro_geral.items():
                filtro = {k: v for k, v in fams.items() if v.get('data_cadastro') == periodo}
                if filtro: dados_mes[b] = filtro
            
            if dados_mes:
                gerar_mapa_interativo(dados_mes)
            else:
                print(f"⚠️ Sem registros para o período {periodo}.")
        elif opcao == "6":
            print("⚙️ Sincronizando com base de dados do Governo Federal...")
            novos_dados = simular_dados_transparencia(117700)
            cadastro_geral.update(novos_dados) # Isso mescla os dados novos com os manuais
            print("✅ Dados sincronizados! Não esqueça de Salvar (Opção 7) para tornar permanente.")
        elif opcao == "7":
            salvar_dados_json(cadastro_geral)
            print("💾 Base de dados atualizada. Até logo!")
            break

if __name__ == "__main__":
    menu_principal()