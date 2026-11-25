# Guia completo do projeto de ciência de dados

Este guia explica o que existe no projeto, como os dados passam pelas quatro etapas, o que cada célula de código faz, por que os gráficos foram escolhidos, como o banco foi modelado e como o dashboard transforma os resultados em indicadores para gestão. Também registra limites e diferenças entre os materiais: compreender um trabalho inclui saber o que ele não demonstra e quais partes precisam ser interpretadas com cuidado.

## 1. Resumo em uma página

O projeto analisa o desempenho de 14 hotéis de Port Alder durante 2027 e 2028. Os arquivos de entrada são JSON Lines (JSONL): cada linha é um objeto JSON. Os dados incluem resultados diários e semanais, hotéis, tipos de quarto, avaliações, cenários de avaliação e decisões de preço.

O fluxo de trabalho é:

1. **Exploração:** conferir a forma, granularidade, tipos e ausências dos sete arquivos JSONL.
2. **Estatística:** comparar ocupação e ADR, descrever sazonalidade e eventos, calcular correlações e ilustrar uma extrapolação.
3. **Banco:** normalizar as entidades em SQLite, conferir chaves e executar consultas de negócio; manter uma cópia documental das avaliações em Mongita.
4. **Visualização:** criar gráficos estáticos e interativos para comparar tiers, acompanhar o tempo, posicionar hotéis frente aos concorrentes e resumir avaliações.
5. **Dashboard:** pré-agregar os dados semanais em CSV e mostrar indicadores filtráveis em Streamlit.
6. **Comunicação:** resumir os achados no relatório executivo, registrar reflexões no diário de campo e apoiar o trabalho com prompts de etapa.

Os dados são descritos no relatório e no dashboard como sintéticos. Portanto, os resultados servem para aprender e ilustrar decisões analíticas; não devem ser tratados como resultados de hotéis reais. A moeda dos valores monetários não está identificada no projeto. Os resultados também não provam causalidade: por exemplo, uma associação entre redução de tarifa e resultado “better” não demonstra que reduzir a tarifa causou o resultado.

## 2. Mapa dos materiais

- [`README.md`](README.md): inventário mínimo da estrutura; não contém glossário de métricas ou metodologia detalhada.
- [`dados/`](dados/): sete fontes JSONL.
- [`notebooks/01_exploracao.ipynb`](notebooks/01_exploracao.ipynb): auditoria inicial dos dados.
- [`notebooks/02_estatistica.ipynb`](notebooks/02_estatistica.ipynb): estatística descritiva, correlações e extrapolação.
- [`notebooks/03_banco_de_dados.ipynb`](notebooks/03_banco_de_dados.ipynb): esquema SQLite, carga, validações, consultas SQL e Mongita.
- [`notebooks/04_visualizacao.ipynb`](notebooks/04_visualizacao.ipynb): figuras reutilizáveis, interpretação e limitações.
- [`banco/Diagrama Entidade-Relacionamento.svg`](banco/Diagrama%20Entidade-Relacionamento.svg): desenho do modelo relacional.
- [`banco/hotel.db`](banco/hotel.db): banco SQLite persistido.
- [`banco/hotel_mongita.db/`](banco/hotel_mongita.db/): armazenamento Mongita de documentos de avaliação.
- [`dashboard/prepare_data.py`](dashboard/prepare_data.py): lê JSONL e gera os quatro CSVs de resumo.
- [`dashboard/app.py`](dashboard/app.py): aplicativo Streamlit que apresenta filtros, métricas, gráficos e tabela.
- [`dashboard/data/`](dashboard/data/): CSVs pré-computados consumidos pelo aplicativo.
- [`dashboard/requirements.txt`](dashboard/requirements.txt): dependências do aplicativo.
- [`relatorio_executivo/relatorio_executivo.md`](relatorio_executivo/relatorio_executivo.md) e [`relatorio_executivo/relatorio_executivo.pdf`](relatorio_executivo/relatorio_executivo.pdf): comunicação para público executivo.
- [`diario_de_campo/diario_de_campo.md`](diario_de_campo/diario_de_campo.md): reflexões sobre uso de IA e aprendizado.
- [`prompt_analise_estatistica.md`](prompt_analise_estatistica.md), [`prompt_banco_de_dados.md`](prompt_banco_de_dados.md) e [`prompt_visualizacao.md`](prompt_visualizacao.md): instruções que especificam as etapas; são briefings, não registros completos de execução.

## 3. O universo de dados

| Arquivo | Linhas | Unidade de observação | Uso principal |
|---|---:|---|---|
| `hotels.jsonl` | 14 | Um hotel | Dimensões e atributos estáveis do hotel; inclui uma lista de comodidades. |
| `room_types.jsonl` | 42 | Um tipo de quarto de um hotel | Capacidade, metragem, ocupação máxima, vista e preço-base. |
| `daily_market.jsonl` | 10.192 | Um hotel em um dia | Ocupação, ADR, receitas, comparação competitiva, eventos e métricas tarifárias. |
| `weekly_performance.jsonl` | 1.456 | Um hotel em uma semana | Desempenho semanal, receitas, índices competitivos e resumo de avaliações. |
| `reviews.jsonl` | 12.077 | Uma avaliação | Nota, texto, cenário, sentimento, atributos avaliados e resposta do hotel. |
| `review_scenarios.jsonl` | 11 | Um cenário do catálogo | Rótulo e descrição do cenário, faixa de notas esperada e ação de recuperação. |
| `rate_decisions.jsonl` | 1.442 | Uma decisão de tarifa de hotel/semana | Ação (`raise`, `hold`, `lower`), valores previstos/realizados e resultado categórico. |

O período dos dados diários vai de 4 de janeiro de 2027 a 31 de dezembro de 2028. As 10.192 linhas diárias equivalem a 14 hotéis observados ao longo de 728 dias. O conjunto semanal tem 104 semanas por hotel (1.456 linhas). Os primeiros três dias de 2027 não estão cobertos. Os dados semanais contêm alguns valores ausentes em `mean_rating`, razão pela qual a análise de nota semanal utiliza 1.429 semanas válidas.

### Glossário das métricas usadas

- **Ocupação:** proporção de quartos ocupados ou vendidos sobre quartos disponíveis. Nos JSONL aparece em escala de 0 a 1; para apresentação, multiplica-se por 100 para obter porcentagem. Quando se calcula uma razão de quartos vendidos por quartos disponíveis, ela pode diferir ligeiramente da média simples das proporções já arredondadas nos registros.
- **ADR:** diária média (Average Daily Rate), preço médio dos quartos vendidos. O projeto não especifica a moeda.
- **RevPAR:** receita de quartos por quarto disponível. Não é receita total nem faturamento geral do hotel.
- **TRevPAR:** receita total por quarto disponível, incorporando outras receitas além de quartos conforme os dados.
- **ARI:** índice relativo de tarifa frente ao conjunto competitivo. Na visualização, os dados sustentam a leitura `ADR / comp_set_adr × 100`; 100 indica paridade.
- **MPI:** índice relativo de ocupação frente ao conjunto competitivo. Na visualização, os dados sustentam a leitura `ocupação / comp_set_occupancy × 100`; 100 indica paridade.
- **RGI:** índice relativo de receita de quartos frente ao conjunto competitivo. É relativo, não uma receita absoluta. O projeto não documenta sua fórmula formal além dos campos observados.
- **MARS:** taxa de referência usada como comparação de tarifa. No dado diário, `mars_basis` informa `comp_set_median_adr_x_positioning`. O notebook calcula o desvio relativo como `(ADR - mars_rate) / mars_rate × 100`; isso não demonstra se uma tarifa é adequada.
- **Pontos percentuais:** diferença entre duas proporções expressas em porcentagem. De 70% para 80% são +10 pontos percentuais, não +10% de variação relativa.
- **Outcome `better`:** rótulo observado em uma decisão semanal; não é uma estimativa de efeito causal.

## 4. Etapa 1 — Exploração: explicação das células

O notebook de exploração é principalmente uma auditoria e uma orientação para entender as fontes. A maioria das células não transforma dados: exibe amostras, dimensões, tipos ou contagens de valores ausentes.

### Células de código, uma a uma

| Célula | O que faz e por que existe |
|---:|---|
| 2 | Importa Pandas, biblioteca usada para representar e inspecionar os JSONL em tabelas. |
| 3 | Lê os sete arquivos JSONL em sete DataFrames. `lines=True` informa que cada linha do arquivo é um JSON independente. Os caminhos são relativos à pasta `notebooks/`. |
| 5 | Mostra as primeiras linhas de `daily_market`, para conferir visualmente nomes de campos e valores. Não resume nem altera os registros. |
| 6 | Retorna `(linhas, colunas)` de `daily_market`: 10.192 × 56. |
| 8 | Lista os tipos inferidos para cada uma das 56 colunas, útil para distinguir datas, textos, números e valores ausentes. |
| 9 | Conta nulos por coluna em `daily_market`. É uma auditoria de completude, não uma imputação. |
| 11 | Mostra uma amostra de `hotels`, incluindo atributos como `name`, `tier`, `rooms` e `amenities`. |
| 13 | Mede as dimensões da dimensão `hotels`: 14 registros e 17 campos. |
| 14 | Célula vazia, sem operação ou resultado; pode ser ignorada. |
| 17 | Verifica os tipos dos 17 campos de `hotels`; `amenities` é uma lista/objeto, não uma coluna numérica simples. |
| 19 | Conta nulos nos atributos de hotel. A saída registrada não mostra nulos. |
| 21 | Mostra uma amostra das decisões de tarifa, incluindo ação, hotel, semana e tarifas de referência. |
| 23 | Confirma 1.442 decisões e 24 campos. |
| 26 | Inspeciona tipos como datas em texto, campos numéricos e rótulos categóricos de ação e resultado. |
| 28 | Conta nulos em `rate_decisions`; a saída registrada não aponta nulos. |
| 30 | Mostra a amostra do catálogo `review_scenarios`, que dá nomes e descrições aos identificadores de cenário. |
| 32 | Confirma 11 cenários e 7 campos. |
| 35 | Verifica tipos do catálogo, incluindo proporção declarada e textos de trigger/ação. |
| 37 | Conta nulos nos campos do catálogo; a saída registrada não aponta nulos. |
| 39 | Mostra avaliações com identificador, hotel, datas, cenário, nota e trechos de texto. |
| 41 | Confirma 12.077 avaliações e 26 campos. |
| 44 | Verifica tipos, incluindo indicadores booleanos, notas parciais e `response_hours` numérico. |
| 46 | Conta ausências nas avaliações. A saída registrada encontra 3.769 valores nulos em `response_hours`; o texto explicativo informa que resposta/horas podem faltar quando o hotel não respondeu. |
| 49 | Mostra tipos de quartos e seus atributos; cada linha é um tipo de quarto, não uma reserva individual. |
| 51 | Confirma 42 linhas e 10 campos em `room_types`. |
| 54 | Inspeciona os tipos de quarto: capacidade, dimensões e prêmio de tarifa são números; vista, tier e tipo são categorias. |
| 56 | Conta nulos nos tipos de quarto; a saída registrada não aponta nulos. |
| 58 | Mostra uma amostra do desempenho semanal, incluindo ocupação, receita, ADR e índices. |
| 60 | Confirma 1.456 semanas de hotel e 41 campos. |
| 63 | Inspeciona tipos do desempenho semanal. `week_start` é texto ISO nos arquivos de origem; métricas e contagens são numéricas. |
| 65 | Conta nulos nas métricas semanais. |
| 68 | Seleciona identificador, nome e lista de comodidades; `explode` transforma cada item da lista em uma linha. Padroniza o texto em minúsculas e sem espaços externos, procura o texto `restaurant` e conta hotéis distintos correspondentes. Resultado registrado: cinco hotéis. |

### Células de texto e conclusão da exploração

- Células 1, 4, 10, 20, 29, 38, 48 e 57 abrem a etapa ou uma subseção para cada conjunto de dados.
- Células 7, 15, 24, 33, 42, 52 e 61 explicam a granularidade: diário por hotel/dia, uma linha por hotel, decisão semanal, cenário, avaliação, tipo de quarto e desempenho semanal.
- As células 12, 16, 18, 22, 25, 27, 31, 34, 36, 40, 43, 45, 50, 53, 55, 59, 62 e 64 organizam a leitura por dimensões, tipos e valores ausentes.
- A célula 47 esclarece que `response_text` e `response_hours` ausentes significam ausência de resposta registrada, e não necessariamente dado perdido ao acaso.
- A célula 66 registra ausências em `mean_rating` no desempenho semanal e texto de resposta ausente quando não há avaliação naquela semana.
- A célula 67 apresenta a pergunta de gestão que motivou a contagem de hotéis com restaurante.
- A célula 69 identifica `hotel_id` como ligação geral e `scenario_id` como ligação entre avaliação e catálogo de cenário. O texto contém grafias simplificadas/typos (`hotle_id`, `reviews_scenarios`) que não alteram a intenção.
- A célula 70 observa que não foi criada função auxiliar: cada operação era curta e local, então abstraí-la não traria benefício claro.

## 5. Etapa 2 — Estatística: cálculo, escolha e interpretação

O notebook declara como população observada os registros disponíveis dos 14 hotéis, e não uma amostra aleatória de um mercado maior. Isso restringe a generalização. As células de texto introduzem cada pergunta, explicam a escolha estatística e registram resultados e limitações.

### Células de código, uma a uma

| Célula | O que faz e como interpretar |
|---:|---|
| 2 | Importa Pandas, lê dados diários, semanais e avaliações, converte datas para `datetime` e imprime contagens, número de hotéis e período. Confirma que as análises seguintes partem dos dados presentes. |
| 4 | Calcula primeiro a ocupação média de cada hotel e depois resume essas médias por tier com média, mediana, mínimo, máximo e quantidade de hotéis. Multiplica proporções por 100 para apresentar porcentagens. Essa ordem evita que hotéis com mais linhas tenham peso adicional na comparação do tier. |
| 6 | Agrupa ADR diário por hotel e tier; calcula ADR médio, desvio padrão populacional (`ddof=0`) e variância populacional. Calcula também coeficiente de variação (desvio padrão / média × 100), depois tira a média das estatísticas por hotel dentro de cada tier. Separa variação absoluta de variação proporcional. |
| 8 | Conta notas 1–5, reintroduz notas sem observação com zero, calcula frequência relativa e frequências absoluta e relativa acumuladas. `rating <= 3` fornece diretamente a proporção de avaliações até três estrelas. Resultado: 55,8%. |
| 10 | Agrupa observações diárias por mês e por dia da semana, calcula médias de ocupação e ADR, converte ocupação para porcentagem e ordena para localizar os períodos de maior média. Traduz os nomes dos dias/meses para facilitar leitura. Agosto lidera mensalmente; sábado lidera por dia da semana. |
| 12 | Cria `tem_evento` verificando se `demand_event` não está vazio. A função `diferenca_evento` calcula médias com e sem evento, e diferenças para ocupação e ADR; a ocupação é reportada em pontos percentuais. Aplica a função ao mercado e a cada tier. É comparação descritiva, sem controle de outros fatores. |
| 14 | Calcula correlação de Pearson entre ocupação diária e ADR, primeiro no conjunto inteiro e depois dentro de cada tier. A correlação mede associação linear, não causalidade. |
| 16 | Descarta semanas sem `mean_rating` ou `trevpar`, calcula correlação de Pearson entre as duas variáveis e repete por tier. São 1.429 semanas válidas; o coeficiente geral é 0,229, mas os valores dentro dos tiers estão próximos de zero. |
| 18 | Seleciona nota geral e seis notas parciais, calcula a matriz de correlações, retém a correlação de cada atributo com `rating` e ordena da mais forte para a mais fraca. Limpeza é a associação mais alta (0,901); localização, a menor (0,166). |
| 20 | Seleciona o hotel H01, verifica se há datas ausentes, calcula ocupação média em cada ano e exige exatamente dois anos consecutivos. Projeta 2029 por extrapolação linear: valor do segundo ano mais a diferença entre os dois anos. Resultado: 73,63% em 2027, 73,89% em 2028 e 74,14% projetado. Se o valor sair de 0–100%, apenas alerta; a extrapolação permanece um exemplo frágil. |

### Por que essas medidas e gráficos não são intercambiáveis

- **Média e mediana:** ambas descrevem centro; a média usa todos os valores e é sensível a extremos; a mediana é mais resistente. As médias e medianas de ocupação por tier são próximas, mas há apenas dois hotéis em economy e luxury, então não há base forte para avaliar extremos nesses grupos.
- **Desvio padrão, variância e CV:** o desvio padrão é expresso na mesma unidade do ADR; a variância está na unidade ao quadrado; o coeficiente de variação é relativo ao ADR médio. Luxury tem o maior desvio padrão médio (65,74), enquanto upscale tem o CV médio ligeiramente maior (18,01%, contra 17,90% em luxury).
- **Correlação:** Pearson resume relação linear entre duas medidas. Uma relação agrupada pode mudar ao segmentar por tier; temporada, evento e características de hotel podem influenciar simultaneamente as variáveis.
- **Pontos percentuais:** a diferença entre ocupação com e sem eventos é expressa em pontos percentuais, não como crescimento relativo.
- **Extrapolação:** projeta além dos anos observados; interpolação estimaria entre observações. Com somente dois pontos anuais, a projeção de 2029 supõe que a mudança observada continuará igual, hipótese não validada.

## 6. Etapa 3 — Modelo relacional, restrições e consultas SQL

### 6.1 O esquema efetivamente persistido

O banco SQLite contém nove tabelas, com 14 hotéis, 42 tipos de quarto, 33 amenidades, 57 associações hotel-amenidade, 11 cenários, 12.077 avaliações, 1.456 fatos semanais, 10.192 fatos diários e 1.442 decisões.

| Tabela | Chave e responsabilidade |
|---|---|
| `HOTEL` | `hotel_id` primária; dimensões descritivas do hotel, incluindo tier, capacidade, localização, base de tarifa e dados agregados de avaliação fornecidos na fonte. |
| `ROOM_TYPE` | `room_type_id` primária e `hotel_id` estrangeira; quartos e características do tipo de acomodação. |
| `AMENITY` | `amenity_id` primária; nome de comodidade único. |
| `HOTEL_AMENITY` | Chave composta `(hotel_id, amenity_id)`; tabela associativa que resolve muitos-para-muitos entre hotel e comodidade. |
| `REVIEW_SCENARIO` | `scenario_id` primária; catálogo de rótulos, faixa, proporção declarada e ação recomendada. |
| `REVIEW` | `review_id` primária; conteúdo e notas da avaliação, ligado a hotel e cenário. Booleanos são inteiros 0/1 no SQLite. |
| `WEEKLY_PERFORMANCE` | Chave composta `(hotel_id, week_start)`; fatos semanais. Não repete nome, tier ou comp_set do hotel. |
| `DAILY_MARKET` | Chave composta `(hotel_id, date)`; fatos diários. Não repete nome, tier ou comp_set do hotel. |
| `RATE_DECISION` | `decision_id` primária; decisão com hotel e semana. Tem chave estrangeira composta `(hotel_id, week_start)` para uma semana válida em `WEEKLY_PERFORMANCE`. |

As tabelas de fatos preservam valores observados, incluindo métricas derivadas presentes na fonte; não recalculam nem removem fatos que podem ser úteis para auditoria. Dados descritivos de hotel ficam em `HOTEL` e são recuperados com `JOIN`. A lista de amenities é decomposta em uma tabela de nomes e uma associativa. O desenho aproxima-se de 3FN para atributos descritivos; não significa que toda redundância possível tenha sido convertida em dimensões.

### 6.2 Integridade e tipos

O SQL cria o esquema dentro de `BEGIN; ... COMMIT` e inclui:

- **PRIMARY KEY** para identificadores e chaves de grão composto.
- **FOREIGN KEY** para relações hotel, cenário, amenidade e hotel-semana.
- **NOT NULL** nos identificadores e atributos essenciais.
- **UNIQUE** para o nome da amenidade.
- **CHECK** para notas em 1–5, proporções/ocupação em 0–1, contagens e tarifas não negativas, booleanos em 0/1, ação em `raise`/`hold`/`lower` e outcome em `better`/`worse`/`in line`.
- Datas e semanas guardadas como texto ISO, por exemplo `2027-01-04`, para ordenação e interoperabilidade simples.
- Índices em colunas usadas com frequência em filtros e junções: semana, data, estação, hotel, cenário, rating e ação.

Uma nuance importante: em SQLite, `PRAGMA foreign_keys=ON` precisa ser habilitado em cada conexão que deve impor as chaves estrangeiras. O notebook ativa isso na carga e na conexão de validação. Os `CHECK`s de proporção são específicos de cada campo; índices como ARI, MPI e RGI podem ser maiores que 1/100 e não são limitados a 0–1.

### 6.3 Células de código do notebook do banco

| Célula | O que faz |
|---:|---|
| 3 | Importa utilitários, tenta localizar a raiz subindo diretórios até achar `dados/`, define caminhos e catálogo de arquivos, lê cada JSONL com a biblioteca `json`, cria tabelas de perfil com linhas/colunas/tipos/nulos e calcula valores únicos de campos categóricos. Também importa Mongita, necessário na etapa documental. |
| 6 | Define o SQL completo de nove tabelas, chaves primárias/estrangeiras, restrições `CHECK` e índices. A tabela semanal é criada antes de `RATE_DECISION` para que a chave estrangeira composta possa referenciá-la. |
| 8 | Define `value` para converter booleano em inteiro e string vazia em `NULL`; define auxiliares de inserção com parâmetros e descoberta de colunas. Remove o banco anterior para reconstruí-lo, abre SQLite e habilita chaves estrangeiras. Insere hotéis, amenidades distintas e ligações, depois as demais tabelas; exclui nome/tier/comp_set redundantes dos fatos. Em seguida recria Mongita e insere avaliações como documentos, usando `review_id` também como `_id`. Fecha a conexão SQLite em `finally`. |
| 10 | Reabre o SQLite, ativa chaves estrangeiras, executa consultas de órfãos com `LEFT JOIN ... IS NULL`, executa `PRAGMA foreign_key_check` e usa `assert` para falhar se alguma relação estiver inconsistente. A saída registrada é zero órfãos e lista vazia no pragma. |
| 12 | Abre conexão e executa sete perguntas de negócio usando exclusivamente SQL. Pandas apenas exibe os resultados. As consultas são detalhadas na próxima seção. |
| 15 | Conta registros nas nove tabelas, confirma que todas as 12.077 avaliações estão tanto no SQLite quanto no Mongita e apresenta novamente o top 5 anual. A consulta é uma verificação/resumo de persistência. |
| 17 | Lê documentos Mongita, verifica unicidade de `review_id`, compara contagens com SQLite e confirma novamente `foreign_key_check`. Usa `assert` para tornar divergências erros explícitos. |
| 18 | Célula vazia, sem operação. |

As células de Markdown 4, 5, 7, 9, 11, 13, 14 e 16 contextualizam normalização, restrições, carga, validação, perguntas de negócio, interpretação e Mongita. A célula 4 explica uma correção importante: uma versão anterior do texto descrevia avaliações somente em Mongita/SQLite em memória; a versão atual persistida inclui `REVIEW` no `hotel.db`.

### 6.4 O propósito de cada consulta

1. **Receita por hotel/ano:** soma `total_revenue` semanal, junta `HOTEL`, agrupa por hotel e ano extraído de `week_start`, usa `ROW_NUMBER()` particionado por ano e mostra top 5. Marisol Bay Resort lidera os dois anos. Receita total favorece hotéis maiores; não equivale a rentabilidade por quarto.
2. **Ocupação e ADR por tier/estação:** junta fatos diários com hotel para obter tier, calcula `AVG(occupancy)` e `AVG(adr)` por grupo. É média por linha diária, não ponderada pelo número de quartos.
3. **Hotéis com mais de 30% de notas 1–2:** agrupa avaliações por hotel, conta avaliações totais e baixas, calcula proporção e filtra com `HAVING`. Northgate Inn tem a maior proporção, 39,14%.
4. **Cenários:** junta `REVIEW` ao catálogo `REVIEW_SCENARIO`, conta avaliações e calcula média de nota por cenário. `recovery_action` vem da dimensão do cenário, não de uma ação realizada em cada avaliação.
5. **Outcome por ação:** conta decisões e avaliações `better` por ação, calcula proporção e percentual. Reduções aparecem com 42,86% `better`, mas têm apenas 189 casos, comparados com 634 aumentos e 619 manutenções; a diferença não estabelece efeito causal.
6. **Respostas por nota:** considera respondida uma linha com `response_text` não vazia; calcula cobertura e média de horas apenas para as respondidas. Nos dados, 100% das notas 1–3 foram respondidas contra cerca de 29% das notas 4–5.
7. **Pergunta original em hotéis luxury:** junta avaliação, hotel e cenário; filtra tier luxury em `WHERE`; agrupa por cenário; mantém grupos com pelo menos 50 avaliações em `HAVING`; calcula nota, tempo de resposta e cobertura. Demonstra consulta com três tabelas e filtro de grupos.

### 6.5 Por que Mongita também está presente

O SQLite é o sistema relacional principal: relações explícitas, integridade referencial, valores validados e consultas com joins e agrupamentos. Mongita mantém uma cópia completa dos documentos de avaliações para demonstrar consultas centradas em documentos, textos longos, campos opcionais ou formatos mais flexíveis. O projeto não usa Mongita como substituto do SQLite: ambos contêm os 12.077 registros, e o notebook verifica essa igualdade.

**Ressalva documental:** o texto da célula 13 ainda contém uma explicação antiga dizendo que avaliações foram lidas de Mongita e analisadas em SQLite `:memory:`. Isso contradiz as células de código e os textos corrigidos das células 4 e 11: o código atual consulta `REVIEW` no banco SQLite persistente. Para entender a execução atual, confie no código e na validação persistida, e considere a frase da célula 13 desatualizada.

## 7. Etapa 4 — Visualizações: por que cada gráfico existe

O notebook separa preparação e construção de figuras. Usa Matplotlib/Seaborn para figuras estáticas e Plotly para as interativas. As funções recebem DataFrames/parâmetros e retornam figuras, o que permite reutilização no Streamlit. Os gráficos respondem a perguntas distintas; cor, tamanho ou eixo adicional não substituem unidade, agregação e fonte.

### Células de código, uma a uma

| Célula | O que faz |
|---:|---|
| 3 | Importa caminhos, expressões regulares, Pandas, NumPy, Matplotlib, Seaborn, Plotly e WordCloud. Define ordem e paletas estáveis por tier/sentimento e um tema visual comum. |
| 4 | Lê cinco JSONL usados nos gráficos, converte datas para tipo temporal e informa período, hotéis, avaliações, cenários e tiers disponíveis. |
| 6 | Define `data_profile`, que lista para campos selecionados o arquivo, tipo e número de nulos. Junta esses perfis para conferir as colunas relevantes antes de desenhar. |
| 8 | Define as funções de preparação e gráfico: resumo por tier, pequenos múltiplos, série temporal, mapa competitivo, boxplot MARS, barras de cenário, Sankey, limpeza de texto e nuvem de palavras. Detalhes abaixo. |
| 10 | Calcula resumo por tier, cria e mostra os três painéis de barras e imprime a tabela numérica que alimenta o gráfico. |
| 13 | Chama a função temporal e exibe a figura Plotly interativa. |
| 16 | Cria o mapa, exibe a figura, mostra os valores agregados por hotel e imprime nomes separados por quadrante. |
| 19 | Cria o boxplot de MARS, calcula por tier quantidade, mediana, média, desvio, mínimo e máximo do desvio percentual. Também registra aviso de depreciação futuro do parâmetro `palette` usado no Seaborn; não impediu a execução registrada. |
| 22 | Constrói e exibe barras horizontais de cenários e tabela de contagens/participação observada, preservando a participação declarada no catálogo para comparação conceitual. |
| 25 | Constrói e exibe o Sankey, compara o total de fluxos ao total de avaliações e imprime os dez maiores pares cenário/faixa. Os dados registrados não têm avaliações excluídas. |
| 28 | Junta e limpa textos por sentimento, conta avaliações positivas/negativas e cria duas nuvens com as mesmas configurações. |

### Funções da célula 8 — lógica interna

- `summarize_tiers_equal_hotels`: mantém hotel, tier, ocupação, ADR e RevPAR; exclui linhas incompletas para as métricas; tira primeiro a média de cada hotel ao longo do período e depois a média entre hotéis no tier. Assim cada hotel tem o mesmo peso, ainda que os hotéis tenham tamanhos diferentes.
- `make_tier_small_multiples`: cria três painéis de barras lado a lado, um para ocupação, um ADR e um RevPAR. A ocupação é multiplicada por 100; ADR e RevPAR ficam na unidade monetária original. Separar eixos evita comparar diretamente unidades incomensuráveis.
- `make_temporal_figure`: agrupa desempenho semanal por data, calcula médias simples entre hotéis e desenha linhas para ocupação e ADR em eixos y distintos. Eventos não vazios aparecem como marcadores por categoria. Esse gráfico mantém interação e hover, mas o eixo duplo pode levar o leitor a comparar visualmente inclinações de medidas com escalas diferentes; leia cada série no eixo próprio.
- `make_competitive_map`: calcula uma média de ARI e MPI por hotel para todo o período, anexa o nome, classifica quatro quadrantes em torno de 100 e cria dispersão Plotly com tier, símbolo, tooltip e linhas de paridade. Acrescenta rótulos por quadrante e IDs dos hotéis. O campo cadastral `positioning_index` não é usado como preço realizado.
- `make_mars_boxplot`: conserva observações com ADR e MARS válida (>0), calcula `(ADR - mars_rate) / mars_rate × 100` e mostra caixa por tier com pontos diários transparentes. O zero indica paridade; sinal positivo/negativo mostra acima/abaixo da referência. Pontos extremos não são removidos sem evidência de erro.
- `make_scenario_bar`: conta identificadores distintos de avaliação por `scenario_id`, junta ao catálogo para obter rótulos, calcula participação observada sobre o total e ordena barras horizontais. As barras são mais comparáveis do que pizza com onze categorias.
- `make_sankey`: junta avaliação ao rótulo do cenário, converte notas em bandas 1–2, 3 e 4–5, conta `review_id` distinto por cenário e banda e cria links ponderados pelas contagens. É um cruzamento categórico, não uma linha temporal nem uma relação causal.
- `clean_review_text`: converte texto a minúsculas, substitui pontuação por espaços, separa tokens e exclui stopwords comuns em português e inglês, vocabulário de domínio pouco informativo e tokens com menos de três caracteres. As avaliações estão em inglês; manter stopwords em ambos idiomas torna a limpeza ampla, mas não equivale a uma análise linguística completa.
- `make_wordcloud`: cria nuvem com largura 900, altura 500, máximo de 30 palavras, escala relativa 0,5, sem combinações automáticas e cores verdes/vermelhas por grupo. Retorna figura Matplotlib.

### As figuras e a interpretação pretendida

1. **Pequenos múltiplos por tier:** três gráficos de barras (ocupação, ADR, RevPAR), mesmo ordenamento, eixos próprios. Boutique tem maior ocupação média entre hotéis (75,8%); luxury tem maiores ADR e RevPAR. São médias entre hotéis, não ranking de cada hotel.
2. **Série temporal semanal:** linhas para ocupação e ADR, painel com eixo duplo e marcadores de evento. A média entre hotéis dá cada registro semanal o mesmo peso; há 104 semanas por hotel. Coincidência entre evento e variação não prova efeito do evento.
3. **Dispersão ARI × MPI:** ponto por hotel, linhas em 100 e quadrantes de preço/ocupação relativos acima/abaixo do conjunto competitivo. Permite distinguir, por exemplo, preço acima com ocupação abaixo, sem presumir que tarifa alta é boa ou ruim. O mapa agrega médias diárias simples e pode ocultar variação temporal.
4. **Boxplot do desvio ADR–MARS:** mediana, quartis, dispersão e pontos diários mostram a distribuição por tier. Há 10.192 observações válidas; o valor positivo é acima da MARS, negativo abaixo. A mediana do boutique é -3,13%, mas sua dispersão é maior do que em outros tiers.
5. **Barras de cenários:** frequência observada por cenário, rótulo e participação calculada. `share_of_reviews` do catálogo é participação declarada/planejada e não deve ser confundida com a frequência observada.
6. **Sankey cenário → faixa de nota:** liga 11 cenários a três bandas (1–2, 3, 4–5) por contagem distinta. As 12.077 avaliações foram incluídas; fluxo mais largo significa maior volume, não progressão causal.
7. **Nuvem positiva e nuvem negativa:** dois gráficos separados e com a mesma configuração, grupos definidos pelo campo existente `sentiment`. Há 4.415 positivas e 5.379 negativas; sentimento neutro é excluído. Tamanho de palavra significa frequência no corpus processado, não importância do tema nem prevalência em todos os hóspedes.

Os três painéis de tier contam como três visualizações separadas, além de sete figuras (temporal, mapa, MARS, cenários, Sankey e duas nuvens): o notebook contém dez representações gráficas distintas. O mapa e a série temporal são interativos em Plotly; outros gráficos usam Matplotlib/Seaborn.

### Limites que afetam a leitura dos gráficos

- O agregado por tier dá peso igual a cada hotel, não a cada quarto vendido; isso responde “como é o hotel médio do tier”, não “qual é o desempenho médio por quarto”.
- No mapa, o notebook calcula médias diárias simples de índices e adota 100 como paridade a partir das relações entre índices e valores competitivos presentes nos dados. O `README.md` não define esses índices.
- No Sankey, agrupamento de notas é uma decisão analítica: 1–2, 3, 4–5; é útil para leitura, mas descarta a distinção entre as notas individuais.
- Nuvem de palavras é uma ferramenta exploratória de frequência. Não estima importância, causalidade nem proporção de hóspedes que mencionam cada tema.
- Os gráficos descrevem 14 hotéis de um mercado sintético e dois anos; não são amostra probabilística de outros hotéis/mercados.

## 8. Dashboard Streamlit — fluxo e desenho da experiência

O dashboard não consulta SQLite durante a execução. Seu fluxo é uma camada de preparação offline e uma camada de apresentação:

1. `prepare_data.py` procura a raiz do projeto a partir do próprio caminho do arquivo.
2. Lê `weekly_performance.jsonl`, `hotels.jsonl`, `rate_decisions.jsonl`, `reviews.jsonl` e `review_scenarios.jsonl`.
3. Deriva mês e ano de `week_start` e agrega fatos semanais em CSVs.
4. O `app.py` lê esses CSVs uma vez por cache de dados do Streamlit e aplica filtros em memória.
5. As métricas e gráficos são atualizados com o subconjunto filtrado; a tabela do hotel é alimentada por um resumo geral.

### O que `prepare_data.py` calcula

- **Mês e ano:** `week_start` é convertido em data; mês vira período `YYYY-MM`, ano é inteiro. Uma semana inteira é atribuída ao mês em que começa.
- **`monthly_summary.csv`:** para cada hotel/mês soma quartos disponíveis, vendidos, receita de quartos, receita total, avaliações e noites de evento. Ocupação é quartos vendidos / disponíveis; ADR é receita de quartos / quartos vendidos; RevPAR e TRevPAR são receita / quartos disponíveis. Nota média é ponderada por quantidade de avaliações.
- **`hotel_summary.csv`:** repete a agregação para o período completo por hotel. Os índices competitivos são calculados como média ponderada por quartos disponíveis. A nota também é ponderada por contagem de avaliações.
- **`competitive_year_summary.csv`:** calcula ARI, MPI e RGI ponderados por quartos disponíveis em cada ano/hotel e RevPAR como receita de quartos / quartos disponíveis.
- **`scenario_summary.csv`:** conta avaliações por ano, hotel, tier e cenário; junta atributos do catálogo e calcula `observed_share` usando a soma do resultado agrupado. O aplicativo exibe contagens, não usa esse campo `observed_share`.

Os quatro CSVs persistidos são artefatos intermediários: se as fontes JSONL mudarem, é necessário executar `prepare_data.py` novamente para atualizar os CSVs. O aplicativo não faz atualização automática dos resumos.

### Como a interface foi pensada

- **Público declarado:** gerente geral de hotel.
- **Decisões apoiadas:** ajustar preço/ocupação, priorizar melhorias operacionais e comparar posição competitiva.
- **Filtros laterais:** tier, ano e hotel. “Todos” preserva uma visão ampla; seleção de hotel lista hotéis compatíveis com o tier selecionado.
- **Indicadores principais:** ocupação, ADR, RevPAR e nota média.
- **Tendência mensal:** linha de ocupação e ADR com eixos separados, hover unificado e cores estáveis. A linha permite acompanhar direção temporal; eixos diferentes devem ser lidos separadamente.
- **Ocupação por tier:** barras para comparar categorias no recorte atual.
- **Mapa competitivo:** ARI no eixo horizontal e MPI no vertical; linhas de referência 100; tamanho do ponto usa RevPAR; cor indica tier; hover mostra hotel, tier e índices.
- **Cenários:** barras horizontais de contagem, coloridas pelo sentimento esperado do catálogo. O comprimento facilita ordenar os cenários e o título diferencia volume observado de expectativa.
- **Tabela por hotel:** ocupação, ADR, RevPAR, TRevPAR, nota e volume de avaliações para leitura tabular/comparação.
- **Estilo:** layout largo, cartões para métricas, paleta azul/laranja para séries, cores estáveis por sentimento e CSS leve para espaçamento e destaque.
- **Dependências declaradas:** Streamlit, Plotly e Pandas; WordCloud/Matplotlib/Seaborn pertencem ao notebook, não à lista do aplicativo.

### Cálculos dos cartões

- **Ocupação:** `soma(rooms_sold) / soma(available_rooms)`, ponderada pela quantidade de quartos disponíveis.
- **ADR:** `soma(adr × rooms_sold) / soma(rooms_sold)`, ponderada pelos quartos vendidos.
- **RevPAR:** receita de quartos estimada como `soma(adr × rooms_sold)` dividida por quartos disponíveis. O CSV mensal não carrega `room_revenue`, então o app reconstrói essa receita a partir de ADR e quartos vendidos.
- **TRevPAR:** receita total reconstruída de `trevpar × available_rooms`, dividida pelo total de quartos disponíveis. Como o denominador e o peso são os mesmos, o cartão mostra média ponderada pelo volume de quartos disponíveis.
- **Nota média:** soma de `mean_rating × review_count` dividida pelo total de avaliações. O peso permite que uma média apoiada em mais avaliações influencie mais o total.

### Observações técnicas importantes do dashboard atual

Estas observações descrevem o código encontrado; não são alterações aplicadas:

1. **Filtro de ano e tabela:** os KPIs e a série mensal usam `monthly` filtrado por ano, mas `hotel_summary` é um resumo de todo o período e não recebe filtro de ano. Assim, ao selecionar 2027 ou 2028, a tabela por hotel continua sendo o resumo dos dois anos. A leitura correta é verificar o título/recorte antes de comparar tabela e cartões.
2. **Mapa com “Todos” os anos:** `competitive_year_summary.csv` tem um ponto por hotel por ano. Sem selecionar ano, o gráfico mostra duas observações por hotel; o ano não está nos campos destacados no tooltip. Com um ano selecionado, passa a haver um ponto por hotel. A versão “Todos” pode parecer mais pontos/hotéis do que há de fato.
3. **Média dos cenários:** os dados são pré-agregados por ano/hotel/cenário e a interface soma `review_count` por cenário sob os filtros. `expected_sentiment` representa expectativa do catálogo, não análise independente de sentimento realizada no dashboard.
4. **Granularidade mensal:** a atribuição pelo mês de início da semana pode colocar dias de uma semana que cruza o limite de mês no mês anterior/seguinte ao de alguns dias. É uma agregação de semanas, não uma soma exata por noites de calendário.
5. **Eixo temporal duplo:** ocupação e ADR aparecem na mesma área visual com eixos y separados. Isso economiza espaço, porém comparar inclinações entre séries pode induzir uma impressão incorreta; leia valores pelos eixos próprios.
6. **Código sem efeito visual:** `line_data` é calculado na seção mensal e não é utilizado para desenhar o gráfico. A série exibida é `monthly_detail`; `line_data` não muda o resultado e é trabalho redundante.
7. **Preparação de resultados por cenário:** a junção à direita preserva cenários do catálogo mesmo quando não há observação em algum agrupamento; valores de contagem vazios são convertidos em zero. Com filtros por hotel/tier, cenários sem linha correspondente podem não aparecer, pois não há categoria de hotel/tier para atender ao filtro.
8. **Falha de dados filtrados:** se o filtro não tiver registros mensais, o app emite um aviso e não tenta calcular os KPIs. As demais áreas, quando sem dados, mostram mensagens específicas.

## 9. Relatório e diário de campo

O relatório executivo converte análises em três perguntas de gestão: comparação competitiva, desempenho associado às decisões de tarifa e sinais das avaliações. Ele apresenta amostras de ARI/MPI/RGI por hotel, os resultados da consulta de outcomes e a distribuição de notas/cenários. Traz limitações explícitas sobre tamanho de amostra, tiers pequenos, moeda não informada, observação sem experimento e causalidade.

O relatório recomenda investigar os hotéis abaixo da paridade competitiva e os cenários de cobrança/limpeza, sem transformar esses sinais em ordem automática de reduzir/preço ou em promessa de melhoria. A recomendação é usar o dashboard para monitorar e formular hipóteses.

O diário explica como prompts estruturados ajudaram a explicitar granularidade e limitações. Há uma ressalva de proveniência importante: o próprio diário declara que o “erro cometido pela IA” foi um exemplo plausível reconstruído, não um incidente verificável. Portanto, não deve ser apresentado como registro factual do processo.

Os três arquivos `prompt_*.md` definem tarefas, critérios e cautelas, inclusive exigências como execução, integridade, número mínimo de visualizações e limitações. Não provam, por si sós, que cada critério foi verificado no ambiente final; os notebooks e artefatos efetivos são a evidência do que foi implementado.

## 10. Achados registrados — com a interpretação correta

- **Ocupação por tier:** boutique tem a maior média/mediana entre hotéis (aprox. 75,8%); economy, a menor (aprox. 61,9%). Não generalizar para outros hotéis ou mercados.
- **Variação da diária:** luxury tem maior desvio padrão absoluto médio do ADR; upscale tem CV ligeiramente maior. “Mais variável” depende de se medir unidades monetárias absolutas ou variação relativa.
- **Sazonalidade:** agosto é o mês de maior ocupação e ADR médio; sábado lidera entre os dias da semana. É uma descrição dos dados observados.
- **Eventos:** noites com evento coincidem com ocupação e ADR maiores, mas o desenho não controla sazonalidade, tipo de evento, demanda ou decisão de tarifa. Não se pode atribuir a diferença ao evento isoladamente.
- **Correlação de ocupação e ADR:** positiva no mercado e positiva em cada tier; ainda assim, correlação não informa mecanismo causal.
- **Nota e receita:** correlação geral fraca entre nota e TRevPAR; dentro dos tiers, correlações próximas de zero. O número de avaliações por semana e diferenças estruturais podem afetar a leitura.
- **Avaliações:** 55,8% têm nota até 3; cenários como cobrança e limpeza apresentam notas médias baixas nos resultados SQL. São pistas operacionais para investigação, não prova de causa única.
- **Decisões de tarifa:** `lower` tem maior proporção observada de `better`, mas n menor e contextos possivelmente distintos. A comparação não demonstra que reduções causam melhor desempenho.
- **Competitividade:** ARI/MPI/RGI com base 100 ajudam a comparar com concorrentes; um valor relativo acima de 100 não é uma medida absoluta de lucro ou qualidade.
- **Projeção:** 74,14% de ocupação H01 em 2029 é resultado de uma extrapolação aritmética de dois pontos anuais, não uma previsão confiável.

## 11. Limitações e pontos para conferir ao apresentar

1. **Dados sintéticos:** não representam evidência empírica sobre hotéis reais.
2. **Cobertura:** 14 hotéis, dois anos e tiers com apenas dois a quatro hotéis. Os primeiros três dias de 2027 não estão no diário.
3. **Moeda:** não identificada; não atribua USD, EUR ou outra moeda aos valores.
4. **Métricas competitivas:** paridade 100 é coerente com a razão de tarifas/ocupações observadas; a documentação principal do README não fornece um glossário formal para todos os índices.
5. **Média por linha versus média ponderada:** notebook de estatística e SQL usam muitas vezes médias simples de registros; o dashboard pondera algumas métricas por volume. São estimandos diferentes, não necessariamente erros, mas não devem ser comparados como se tivessem a mesma regra.
6. **Mensalização:** a partir de fatos semanais, cada semana é agrupada pelo mês em que começa.
7. **Causalidade:** avaliações, eventos, tarifas e receita são observacionais; não há desenho experimental ou identificação causal.
8. **Colunas ausentes versus não aplicáveis:** resposta ausente pode significar que não houve resposta; nota semanal ausente pode indicar ausência de avaliações. Não imputar sem uma decisão explícita.
9. **Estado dos resultados:** os notebooks têm saídas gravadas, mas isso não garante que uma execução futura no mesmo ambiente e com as mesmas dependências será idêntica. O notebook 4 registra um aviso de depreciação futura do Seaborn.
10. **Materiais desatualizados:** a frase da célula 13 do notebook de banco sobre Mongita/SQLite em memória contradiz o código persistente atual. O dashboard também tem as ressalvas de filtro e duplicidade temporal descritas acima.

## 12. Roteiro para dominar e apresentar o trabalho

1. Comece pela unidade de observação de cada JSONL; antes de qualquer fórmula, pergunte “o que representa uma linha?”.
2. Explique por que um hotel-dia, um hotel-semana e uma avaliação não são linhas intercambiáveis.
3. Mostre como `hotel_id` e `scenario_id` conectam as fontes; depois mostre a normalização e as chaves no SQLite.
4. Ao apresentar cada resultado, diga primeiro fonte, filtro, granularidade e regra de agregação; só depois diga o número.
5. Separe números absolutos (receita total) de taxas/índices relativos (ocupação, ARI/MPI/RGI) e normalizados por capacidade (RevPAR/TRevPAR).
6. Para cada gráfico, formule a pergunta que ele responde; explique os eixos, a agregação e a razão da forma visual escolhida.
7. Explique que o dashboard é uma interface para recortes e monitoramento, alimentada por CSVs preparados fora do app; não é o banco de dados nem um modelo causal.
8. Termine com limitações e recomendações como hipóteses a validar, nunca como garantias.

Uma explicação tecnicamente sólida do projeto não é apenas repetir o resultado: é conseguir reproduzir a cadeia **fonte → transformação → agregação → visualização/consulta → interpretação → limite** para cada conclusão.
