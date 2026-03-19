# 🗺️ Sistema de Unificação Geográfica (UNDB 4.0)

**Foco:** Segurança Alimentar e Inteligência de Dados na Região Metropolitana de São Luís  
**Status:** Sprint Final Finalizada ✅ | **Data:** 19 de Março de 2026  

---

## 📖 1. Visão Geral e Contexto
O sistema funciona como uma plataforma de **Inteligência Geossocial**. Além de validar endereços informais via geolocalização, o software cruza dados geográficos de risco (áreas de alagamento) com indicadores socioeconômicos (Renda e Aluguel) para identificar famílias em **Estado Crítico**.

O diferencial desta versão é a integração com o **Portal da Transparência**, permitindo comparar os cadastros locais com o investimento federal (Bolsa Família) na região.

---

## 🏗️ 2. Arquitetura Modular
O projeto segue o princípio da **Responsabilidade Única (SRP)**:

| Arquivo | Função |
| :--- | :--- |
| **UnificIntdados.py** | Maestro: Gerencia o menu e a lógica de decisão social. |
| **GeolocIntelij.py** | Especialista: Interface com Google Maps API e polígonos de risco. |
| **transparencia.py** | Integrador: Consome a API REST do Governo Federal. |
| **visualizacao_mapa.py** | Dashboard: Gera o mapa interativo, Calor e Painel HTML. |
| **gráficos.py** | Visualizador: Gera barras estatísticas com dados da API. |
| **relatorios.py** | Persistente: Gerencia o ranking e o banco de dados JSON. |



---

## ⚙️ 3. Decisões Técnicas e Lógica
* **Lógica de Priorização:** Triagem automática usando a regra:  
  `SE (Renda <= 1412.00 E Aluguel == True) -> STATUS: CRÍTICO (Vinho)`.
* **Resiliência (Failover):** Implementação de **Mock de Dados**. Caso a API do Governo falhe ou o token expire, o sistema ativa dados históricos para não interromper a visualização.
* **Eficiência:** Uso de **Dicionários Aninhados**, garantindo busca e inserção em tempo constante **O(1)**.

---

## 🚀 4. Funcionalidades Principais
1. **Geocodificação:** Converte endereços em coordenadas precisas via Google Cloud.
2. **Análise Geoespacial:** Identifica residências em zonas de risco (rios Anil/Bacanga).
3. **Pins Dinâmicos:** Cores diferenciadas (Vinho, Vermelho, Azul) por urgência.
4. **Mapa de Calor:** Identifica manchas de densidade de vulnerabilidade.
5. **Dashboard Integrado:** O mapa HTML exibe um painel com dados reais de investimento federal.

---

## 💻 5. Como Executar
1. Instale as dependências:  
   `pip install googlemaps python-dotenv matplotlib folium requests`
2. Configure o arquivo `.env`:
   ```env
   GEOCODEAPI_KEY=sua_chave_google
   CHAVE_TRANSPARENCIA=seu_token_governo
