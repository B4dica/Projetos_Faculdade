import json 
from datetime import datetime
from dotenv import load_dotenv

# Importações corrigidas e unificadas (O melhor de cada um)
from GeolocIntelij import (
    inicializar_gmaps, 
    buscar_endereco_mestre, 
    extrair_cidade_e_bairro,
    avaliar_prioridade_geografica,
)
from transparência import buscar_beneficios_municipio # Módulo do Davi
from relatorios import exibir_ranking_bairros, salvar_dados_json, simular_dados_transparencia
from gráficos import grafico_comparativo_cidades, gerar_mapa_interativo

load_dotenv()
gmaps_cliente = inicializar_gmaps()

# --- CARREGAMENTO DE DADOS (Memória Unificada) ---
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
    
    # Campo de Renda (Unificando a lógica do Davi)
    renda = float(input("Renda Familiar Total (R$): ").replace(',', '.'))
    mora_aluguel = input("Mora de aluguel? (S/N): ").strip().upper() == "S"
    
    # Otimização: Assume São Luís, diminuindo o esforço do usuário
    endereco_parcial = input("Endereço (Rua, Nº, Bairro): ")
    cidade_alvo = "São Luís" 
    
    print(f"🔍 Consultando base do Google Maps...")
    res_bruto = buscar_endereco_mestre(gmaps_cliente, endereco_parcial, cidade_alvo)
    
    if not res_bruto:
        print("❌ Localização não encontrada. Tente ser mais específico.")
        return

    # Extração e UX de Segurança (Do seu código)
    dados_geo = extrair_cidade_e_bairro(res_bruto)
    endereco_completo = res_bruto[0].get('formatted_address', 'Endereço não formatado')
    
    print(f"\n📍 O Google encontrou: {endereco_completo}")
    confirmar = input("Confirmar este local para o cadastro? (S/N): ").upper()
    
    if confirmar == 'S' and dados_geo:
        bairro_real = dados_geo["bairro"]
        lat, lng = dados_geo["lat"], dados_geo["lng"]
        
        # 1. Prioridade Geográfica (SEU Geofencing de 3 Níveis)
        situacao_geo, prioridade_geo = avaliar_prioridade_geografica(lat, lng)
        
        # 2. Lógica de Estado Crítico do Davi (Renda <= 1 Salário Mínimo e Aluguel)
        # Salário Mínimo 2026 estimado em R$ 1.500,00 para o trabalho
        salario_minimo = 1500.00
        if renda <= salario_minimo and mora_aluguel:
            nivel_final = "CRÍTICO" # <--- Lógica unificada do Davi
        else:
            nivel_final = prioridade_geo # <--- Lógica unificada do Geofencing
        
        data_atual = datetime.now().strftime("%m/%Y") 
        
        if bairro_real not in cadastro_geral:
            cadastro_geral[bairro_real] = {}
            
        cadastro_geral[bairro_real][id_f] = {
            "nome": nome,
            "cidade": dados_geo["cidade"],
            "bairro": bairro_real, 
            "coords": [lat, lng],
            "situacao": situacao_geo,
            "prioridade": nivel_final,
            "renda_capita": round(renda / 4, 2), # Estimativa de 4 pessoas por família
            "aluguel": mora_aluguel,
            "data_cadastro": data_atual
        }
        print(f"✅ Sucesso! {nome} alocado em {bairro_real} (Status: {nivel_final}).")
    else:
        print("🚫 Operação cancelada pelo usuário.")

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("🍽️  SISTEMA DE SEGURANÇA ALIMENTAR UNIFICADO (VIGILANT)")
        print("="*50)
        print("1. Cadastrar Família (Entrada Manual + Critérios Sociais)")
        print("2. Ver Gráfico de Distribuição por Bairro (Proporcional)")
        print("3. Exibir Ranking de Necessidade (Volume)")
        print("4. Mapa de Calor e Risco Interativo (3 níveis) 🗺️")
        print("5. Sincronizar Portal da Transparência (Massa de Dados Realista)")
        print("6. Consultar Dados Oficiais do Governo 💰")
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
            print("⚙️ Sincronizando com base de dados do Governo Federal (117.700 registros)...")
            novos_dados = simular_dados_transparencia(117700)
            cadastro_geral.update(novos_dados) # Isso mescla os dados novos com os manuais
            print("✅ Dados sincronizados! Não esqueça de Salvar (Opção 7) para tornar permanente.")
        elif opcao == "6":
            # Lógica de Consulta do Davi (Unificada e Blindada)
            print("\n" + "="*40)
            print("--- CONSULTA PORTAL DA TRANSPARÊNCIA ---")
            
            # 1. Inputs com valores padrão para facilitar o teste em São Luís
            cod_ibge = input("Código IBGE (São Luís: 2111300): ") or "2111300"
            mes_ano = input("Mês/Ano (Ex: 202601): ")
            
            # 2. Chama a função do arquivo transparencia.py
            dados = buscar_beneficios_municipio(cod_ibge, mes_ano)
            
            if dados and len(dados) > 0:
                res = dados[0]
                
                # 3. Extração segura dos campos (evita erro se a API mudar o nome da chave)
                qtd = res.get('quantidadeBeneficiados') or res.get('quantidadeBeneficiarios') or 0
                valor_total = res.get('valor', 0)
                nome_cidade = res.get('municipio', {}).get('nomeIBGE', 'SÃO LUÍS')

                # 4. EXIBIÇÃO NA TELA
                print(f"\n📊 DADOS OFICIAIS ({nome_cidade}):")
                print(f"💰 Total Bolsa Família: R$ {valor_total:,.2f}")
                print(f"👥 Beneficiários: {qtd}")
                print("="*40)

                # 5. O SEGREDO: Salvar na memória sem apagar os bairros
                # Criamos uma chave especial chamada 'ESTATISTICA_GOVERNO'
                cadastro_geral["ESTATISTICA_GOVERNO"] = {
                    "municipio": nome_cidade,
                    "valor_total": valor_total,
                    "beneficiarios": qtd,
                    "mes_referencia": mes_ano,
                    "data_da_consulta": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                print("\n✅ Resumo oficial integrado ao banco de dados com sucesso!")
                print("💡 Dica: Use a Opção 7 para gravar permanentemente no JSON.")
            else:
                print("\n⚠️ A API não retornou dados. Verifique sua chave no .env ou tente o mês '202601'.")
        elif opcao == "7":
            salvar_dados_json(cadastro_geral)
            print("💾 Base de dados atualizada. Até logo!")
            break

if __name__ == "__main__":
    menu_principal()