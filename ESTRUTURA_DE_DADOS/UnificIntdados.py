
# def sistema(): 
#     familia = {Nome:f'{nome}',Bairro:f'{bairro}',Membros:f'{membros}',Renda:f'{renda}',Tipo_de_moradia:f'{tipo}',Nivel:f'{nivel}'}

#     bairros = set(f'{bairro}')
    
# def dados():

#Gemini
# 1. Dicionário de Famílias (Cadastro)
# Chave: CPF ou ID único | Valor: Atributos da família
familias = {
    "123.456.789-00": {
        "responsavel": "Maria Silva",
        "bairro": "Anjo da Guarda",
        "membros": 4,
        "renda_pc": 250.00,
        "inseguranca": "Alta"
    },
    "987.654.321-11": {
        "responsavel": "João Souza",
        "bairro": "Cidade Operária",
        "membros": 3,
        "renda_pc": 150.00,
        "inseguranca": "Crítica"
    }
}

# 2. Conjuntos (Sets) para Gestão de Bairros
todos_bairros_alvo = {"Anjo da Guarda", "Cidade Operária", "Coroadinho", "Vila Luizão"}
bairros_atendidos = {"Anjo da Guarda", "Vila Luizão"}

# Operação de Diferença: Quais faltam atender?
bairros_pendentes = todos_bairros_alvo - bairros_atendidos

# 3. Lista de Listas (Matriz) - Distribuição Mensal (Jan a Jun)
# Cada linha é um bairro, cada coluna é um mês (quantidade de cestas)
# Exemplo: [Jan, Fev, Mar, Abr, Mai, Jun]
distribuicao_cestas = [
    [100, 120, 150, 200, 180, 130], # Bairro A
    [80, 90, 110, 160, 140, 100]    # Bairro B
]

# 4. Tuplas para Histórico Imutável (Data, Bairro, Quantidade)
historico_entregas = (
    ("2024-01-15", "Anjo da Guarda", 50),
    ("2024-02-10", "Vila Luizão", 30)
)

# --- Demonstração de Saída ---
print(f"Bairros que ainda precisam de assistência: {bairros_pendentes}")
print(f"Cestas entregues no Coroadinho em Março (Simulação): {distribuicao_cestas[0][2]}")