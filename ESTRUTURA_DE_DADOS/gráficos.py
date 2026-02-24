import matplotlib.pyplot as plt

# 1. Dados já unificados (Simulando o processamento inteligente)
bairros = ["Cidade Olímpica", "Vila Maranhão", "Anjo da Guarda", "Coroadinho"]
niveis_inseguranca = [85, 92, 78, 95] # Porcentagem ou volume unificado

# 2. Criação do Gráfico de Barras (Pedido no desafio)
plt.figure(figsize=(10, 6))
plt.bar(bairros, niveis_inseguranca, color='teal')

# 3. Customização para a realidade de São Luís
plt.title('Nível de Insegurança Alimentar por Bairro - São Luís/MA')
plt.xlabel('Comunidades')
plt.ylabel('Índice de Vulnerabilidade (%)')

plt.show()