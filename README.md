# 🗺️ Sistema de Unificação Geográfica (UNDB 4.0)

**Foco:** Segurança Alimentar na Região Metropolitana de São Luís

**Status:** Sprint 1 Finalizada ✅ | **Data:** 15 de Março de 2026

## 📖 1. Visão Geral e Contexto

O sistema foi desenvolvido para mapear e mitigar a insegurança alimentar na Grande Ilha. Ele soluciona o problema de endereços informais e duplicidade de dados, utilizando geolocalização precisa para priorizar famílias em áreas de extrema vulnerabilidade.

Bairros como **Cidade Olímpica, Vila Maranhão e Anjo da Guarda** concentram famílias com renda inferior a meio salário mínimo. O software identifica automaticamente se essas famílias estão em comunidades ribeirinhas ou palafitárias (como nas margens dos **rios Anil e Bacanga**), que sofrem com enchentes sazonais.

## 🏗️ 2. Arquitetura Modular (Clean Code)

O projeto foi estruturado seguindo o princípio da responsabilidade única, facilitando a manutenção e escala:

| Arquivo | Função |
| --- | --- |
| **`UnificIntdados.py`** | **O Maestro:** Gerencia o menu, o fluxo de cadastro e o carregamento inicial da memória. |
| **`GeolocIntelij.py`** | **O Especialista:** Integração com Google Maps API e lógica de classificação automática de prioridade geográfica. |
| **`relatorios.py`** | **O Analista:** Gera rankings de necessidade e gerencia a persistência (leitura/escrita) no banco JSON. |
| **`visualizacao_mapa.py`** | **O Cartógrafo:** Gera o mapa interativo (`Folium`) com retângulos de risco e marcadores dinâmicos. |
| **`gráficos.py`** | **O Visualizador:** Gera indicadores estatísticos em barras usando `Matplotlib`. |

## ⚙️ 3. Decisões Técnicas e Estrutura de Dados

* **Persistência de Dados:** Uso de arquivos **JSON** com tratamento de exceção (`try/except`). Isso garante que os dados não sejam perdidos ao fechar o programa.
* **Dicionários Aninhados:** A estrutura `{Bairro: {NIS: Dados}}` garante busca e inserção rápidas ($O(1)$), fundamental para o crescimento do banco de dados.
* **Geoprocessamento:** O sistema utiliza cálculos de limites (latitude/longitude) para detectar se um endereço validado pelo Google entra em uma zona de monitoramento crítico.

## 🚀 4. Funcionalidades Implementadas

1. **Cadastro com Validação Real:** Consulta à API do Google Cloud para converter endereços em coordenadas.
2. **Ranking de Necessidade:** Ordenação automática dos bairros com maior volume de famílias em risco.
3. **Mapa de Risco Interativo:** Geração de arquivo HTML com:
* **Pins Coloridos:** Vermelho para prioridade alta e Azul para normal.
* **Zonas de Risco:** Retângulos vermelhos delimitando as bacias hidrográficas dos rios Anil e Bacanga.
* **Controle de Camadas:** Seletor para ligar/desligar visualizações.



## 💻 5. Como Executar

1. Instale as dependências: `pip install googlemaps python-dotenv matplotlib folium`
2. Configure sua chave no arquivo `.env`: `GEOCODEAPI_KEY=sua_chave_aqui`
3. Execute o arquivo principal: `python UnificIntdados.py`

---

### 🎓 Nota para a Apresentação

Este projeto demonstra a aplicação prática de Engenharia de Software ao unir estruturas de dados eficientes, integração de APIs de terceiros e visualização estratégica de informações para a resolução de problemas sociais reais.
