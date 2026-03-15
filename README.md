# 🗺️ Sistema de Unificação Geográfica (UNDB 4.0)
**Sistema de Segurança Alimentar - Grande Ilha (São Luís)**

> **Status do Projeto:** Em desenvolvimento (Sprint 1) 🚧  
> **Última Atualização:** 15 de Março de 2026

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Google Maps API](https://img.shields.io/badge/Google%20Maps-API-success)
![Status](https://img.shields.io/badge/status-Sprint%201-orange)

## 📖 1. Visão Geral do Projeto
Este sistema é uma solução de **Inteligência Geográfica** desenvolvida para mapear e mitigar a insegurança alimentar na Região Metropolitana de São Luís (São Luís, Paço do Lumiar, São José de Ribamar e Raposa). 

O software utiliza a **API do Google Maps** para normalizar endereços informais e convertê-los em dados estruturados, permitindo a priorização algorítmica de famílias em zonas de alta vulnerabilidade (ex: comunidades ribeirinhas e palafitárias do Eixo Itaqui-Bacanga).

### 🎯 Principais Desafios Resolvidos:
- **Duplicidade de Dados:** Mitiga lacunas no atendimento da assistência social municipal.
- **Inconsistência Geográfica:** Transforma inputs informais (ex: "Rua do Peixe, Anjo da Guarda") em endereços oficiais validados em tempo real.
- **Volume de Cadastros:** Utiliza estruturas com complexidade $O(1)$ para processamento rápido e eficiente.

---

## 🏗️ 2. Arquitetura do Sistema (Modularização)
O sistema adota uma arquitetura modular, dividindo claramente as responsabilidades:

| Módulo | Papel | Descrição das Responsabilidades |
| :--- | :--- | :--- |
| `UnificIntdados.py` | **O Maestro** (Cérebro) | Gerencia o fluxo principal, interface interativa (CLI) e orquestração. |
| `GeolocIntelij.py` | **O Especialista** (API) | Executa geocoding, extração de coordenadas e monitoramento de cotas da Google Maps API. |
| `relatorios.py` | **O Analista** (Dados) | Processa rankings de prioridade e gerencia a persistência no `cadastro_familias.json`. |
| `gráficos.py` | **O Visualizador** (UI) | Utiliza `matplotlib` para gerar indicadores visuais da distribuição por município. |

---

## ⚙️ 3. Lógica e Estruturas de Dados
Para garantir a melhor complexidade computacional, o sistema utiliza:

- **Dicionários Aninhados:** Estrutura matriz `{ Cidade: { NIS: { Dados } } }` garantindo acesso de complexidade temporal $O(1)$.
- **Tuplas:** Coordenadas (lat, lng) são salvas em tuplas garantindo imutabilidade e economia de memória.
- **Sets (Conjuntos):** Operações matemáticas de Diferença de Conjuntos para comparar "Bairros Alvo" vs "Bairros Atendidos".
- **Listas de Listas:** Matrizes (`distribuicao_cestas`) para prever a sazonalidade e logística no período de chuvas.

---

## 🚀 4. Funcionalidades de Destaque
- **Gavetas Dinâmicas:** Alocação de bairros sob demanda (`if bairro_real not in cadastro_geral:`), evitando travamentos por Erro de Chave.
- **Priorização Automática:** Algoritmo que eleva a prioridade de famílias com renda *per capita* < R$ 200,00 e chefia feminina.
- **Dashboard de Cotas:** Contador preventivo de requisições `.geocode()` no terminal para evitar cobranças indevidas na Google Cloud.

---

## 📊 5. Referencial Teórico (Validação de Dados)
A base de dados de testes foi calibrada com as pesquisas oficias mais recentes do Brasil e do Maranhão:

1. **IBGE (PNAD Contínua):** Priorização de lares chefiados por mulheres (59,9% dos casos graves) e baixa escolaridade.
2. **Rede PENSSAN (VIGISAN):** Linha de corte focada em renda *per capita* $\le$ meio salário mínimo e trabalho informal.
3. **IMESC / Sedes:** Validação geográfica focada no Eixo Itaqui-Bacanga, Coroadinho e Zona Rural.

---
