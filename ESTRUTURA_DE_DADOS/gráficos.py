import matplotlib.pyplot as plt

def grafico_comparativo_cidades(cadastro_geral):
    # Filtra apenas cidades que possuem alguém cadastrado para o gráfico não ficar vazio
    cidades = [c for c in cadastro_geral.keys() if len(cadastro_geral[c]) > 0]
    totais = [len(cadastro_geral[c]) for c in cidades]
    
    if not totais:
        print("⚠️ Sem dados para gerar o gráfico comparativo.")
        return

    plt.figure(figsize=(8, 5))
    cores = ['#1f77b4', '#ff7f0e', '#2ca02c'] # Cores distintas
    
    plt.bar(cidades, totais, color=cores[:len(cidades)])
    plt.title('Distribuição de Assistência na Região Metropolitana')
    plt.ylabel('Quantidade de Famílias')
    plt.xlabel('Municípios')
    
    # Ajusta para os nomes não sumirem
    plt.tight_layout()
    plt.show()