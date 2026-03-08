# Documentação do Projeto: Sistema de Unificação Geográfica (UNDB 4.0)

**Data de atualização:** 06 de março de 2026  
**Status:** Em desenvolvimento (Sprint 1)

---

## 1. Contexto e Problemática
Bairros como Cidade Olímpica, Vila Maranhão e Anjo da Guarda concentram famílias com renda *per capita* inferior a meio salário mínimo. Muitas delas dependem exclusivamente de programas de transferência de renda e doações para subsistência. 

Além disso, comunidades ribeirinhas e palafitárias, como as localizadas às margens dos rios Anil e Bacanga, sofrem com enchentes sazonais que agravam a escassez de alimentos e dificultam o acesso aos pontos de distribuição.

### Desafios Identificados:
* **Duplicidade e lacunas no atendimento:** Enquanto algumas famílias estão cadastradas em múltiplos programas, outras em situação crítica sequer constam nos registros da assistência social municipal.
* **Volume de dados crescente:** O aumento no número de famílias cadastradas em São Luís impacta diretamente o desempenho dos algoritmos.
    * *Solução:* Implementação de rotinas para limpeza de dados obsoletos e transição de registros (ex: restrição por faixa de renda).
* **Critérios múltiplos de priorização:** Necessidade de ordenação por atributos (renda, dependentes, tempo de espera e localização em área de risco). O foco é a escolha do algoritmo com a melhor complexidade computacional para cada cenário.
* **Inconsistência de dados:** Informações incompletas entre diferentes órgãos demandam tratamento e validação prévia.

---

## 2. Diário de Bordo: Erros e Resoluções
O projeto iniciou com um erro de sintaxe no terminal (`no such option: -d`), causado por uma tentativa incorreta de instalação de bibliotecas.

**Correções efetuadas:**
1.  **Instalação de Dependências:** Instalamos a `python-dotenv` (para chaves de API) e a `googlemaps` (inteligência geográfica).
2.  **Configuração de Ambiente:** Ajuste no VS Code para reconhecimento das bibliotecas no ambiente Python 3.13.

---

## 3. Arquitetura de Software (Modularização)
O sistema foi dividido em três pilares para garantir organização e escalabilidade:

* **`GeolocIntelij.py` (Módulo de Serviço):** Comunicação exclusiva com a API do Google Cloud. *Obs: Atualmente identifica localização, mas a definição automática de "Zonas de Risco" ainda está em implementação.*
* **`UnificIntdados.py` (Cérebro/Lógica):** Onde os dados são processados, unificados e organizados.
* **`gráficos.py` (Visualização):** Transforma os dicionários de dados em informação visual para suporte à tomada de decisão.

---

## 4. Lógica e Estrutura de Dados
Para garantir a eficiência exigida pelo desafio, utilizamos:

* **Dicionários Aninhados:** Estrutura `{ Cidade: { NIS: { Dados } } }`, permitindo acesso rápido com complexidade $O(1)$.
* **Tuplas:** As coordenadas geográficas (lat, lng) são armazenadas em tuplas. Por serem imutáveis, garantem a segurança da localização validada. Além disso, o armazenamento numérico economiza memória RAM em comparação ao uso de strings.
* **Sets (Conjuntos):** Uso de **Diferença de Conjuntos** para comparar "Bairros Alvo" vs. "Bairros Atendidos", identificando lacunas de assistência.

> **Funcionamento da Geo:** Cada cidade é uma chave. Ao registrar uma família em São Luís, a API identifica as coordenadas reais (ex: -2.5231823), priorizando números para otimização de memória.

---

## 5. Integração com API Google Maps
A lógica de Unificação Inteligente resolve a inconsistência de dados através de:
1.  **Geocoding:** Converte endereços informais (ex: "Maiobão") em endereços oficiais.
2.  **Entitização:** O Google Maps atua como validador para confirmar a jurisdição correta do bairro (São Luís, Paço do Lumiar ou São José de Ribamar).

---

## 6. Impacto da Implementação
* **Unificação de Dados:** Resolve a dispersão de informações, tratando a Ilha de São Luís como uma unidade integrada.
* **Matriz de Sazonalidade:** Através da estrutura `distribuicao_cestas` (Lista de Listas), o sistema prevê meses de maior exigência logística devido ao período de chuvas.
* **Priorização Automática:** Filtro automático onde famílias com renda *per capita* inferior a R$ 200,00 são marcadas como "Prioridade Alta".
