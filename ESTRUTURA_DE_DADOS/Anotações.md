Bairros como Cidade Olímpica, Vila Maranhão e Anjo da Guarda concentram famílias com renda per capitai nferior a meio salário mínimo, muitas delas dependentes exclusivamente de programas de transferência de rendae doações para se alimentar. 

Comunidades ribeirinhas e palafitárias, como as do Rio Anil e Bacanga, sofrem com enchentes sazonais que agravam a escassez de alimentos e dificultam o acesso a pontos de distribuição. 

Duplicidade e lacunas no atendimento: enquanto algumas famílias são cadastradas em múltiplos programas assistenciais, outras em situação igualmente crítica sequer constam nos registros da assistência social municipal.

No entanto, mesmo com essas ferramentas, surgem desafios como:UNDB 4.0 

Volume de dados crescente, que impacta diretamente o desempenho dos algoritmos à medida que o número de famílias cadastradas em São Luís aumenta. -> [Possível resoução: Um sistema que limpe dados que não são mais necessários ou trasnsição desses dados par outro setor(Ex: Restrição por renda, )]

Critérios múltiplos de priorização, exigindo ordenação por diferentes atributos (renda, número de dependentes,tempo sem atendimento, localização em área de risco) e a escolha do algoritmo mais eficiente para cada cenário. --> [Muito provavelmente "Algorítmo mais eficiente = melhor complexidade]

Dados incompletos ou inconsistentes entre os diferentes órgãos da prefeitura, que demandam tratamento evalidação antes da análise. 

Necessidade de cruzar informações de diferentes secretarias para evitar duplicidade de atendimento e garantir cobertura nos bairros mais vulneráveis da capital

📑 Documentação do Projeto: Sistema de Unificação Geográfica (UNDB 4.0) mudanças do dia 06/03/2026

1. O Problema Inicial e ResoluçãoO projeto começou com um erro de sintaxe no terminal (no such option: -d), causado por uma tentativa incorreta de instalação de bibliotecas.Correção: Instalamos o python-dotenv (para segurança de chaves) e o googlemaps (para inteligência geográfica).Ambiente: Configuramos o VS Code para reconhecer as bibliotecas dentro do ambiente Python 3.13.


2. Arquitetura de Software (Modularização)Para atender aos critérios de organização e escalabilidade, dividimos o sistema em três pilares:GeolocIntelij.py (Módulo de Serviço): Responsável exclusivo pela comunicação com a API do Google Cloud.UnificIntdados.py (Cérebro/Lógica): Onde os dados são processados, unificados e armazenados em estruturas de dados complexas.gráficos.py (Visualização): Transforma os dicionários de dados em informação visual para tomada de decisão. [A geolocalização ainda não define "Zonas de risco" até agora ela só define os dados de localização das famílias inscritas]



3. Lógica de Estrutura de Dados (Conforme o Desafio)Implementamos as estruturas exigidas no enunciado para garantir eficiência:Dicionários Aninhados: Utilizamos uma estrutura { Cidade: { NIS: { Dados } } }. Isso permite acesso rápido ($O(1)$) e organiza as famílias por município.Tuplas: As coordenadas geográficas (lat, lng) são armazenadas em tuplas, garantindo que a localização, uma vez validada, seja imutável e segura.Sets (Conjuntos): Usamos a Diferença de Conjuntos para comparar "Bairros Alvo" vs "Bairros Atendidos", identificando lacunas de assistência. [A geo funciona da seguinte forma: cada cidade será uma chave e o seu valor será a família, logo ao registrar uma família para Sâo Luís, ele irá para ("São Luis":{}) e o google API vai identificar o "Sâo Luís" e vai identifciar que essa cidade é real e as coordenadas seriam ex: -2,5231823. É bom colocar em coordenadas pois números poupam menos memória RAM do que Strings como "Sâo Luis" então o computador apenas coloca as coordenadas no dados]



4. Integração com a API Google MapsA lógica de Unificação Inteligente resolve o problema de dados inconsistentes:Geocoding: O sistema converte endereços informais (ex: "Maiobão") em endereços oficiais.Entitização: O Google Maps atua como o validador que confirma se um bairro pertence a São Luís, Paço do Lumiar ou São José de Ribamar, evitando erros de jurisdição.



5. Impacto no Texto do DesafioA implementação afeta e resolve os seguintes pontos do texto base:Unificação de Dados: Resolve a dispersão de informações entre as três prefeituras. Agora, um único banco de dados entende a Ilha como uma unidade.Matriz de Sazonalidade: Através do distribuicao_cestas (Lista de Listas), o sistema pode prever quais meses exigem mais logística devido às chuvas no Maranhão.Priorização: Criamos um filtro automático onde famílias com renda per capita inferior a R$ 200 são marcadas com "Prioridade Alta".