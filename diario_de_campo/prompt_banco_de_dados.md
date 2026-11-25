# Prompt — Etapa 3: Banco de dados

# Instrucao

Utilize o notebook `03_banco_de_dados.ipynb`, os dados da pasta `dados`, o diagrama ER da pasta `banco` e os conhecimentos de SQL e SQLite necessarios para concluir integralmente esta etapa.

## Objetivo

Analisar a normalizacao dos dados, criar um banco relacional em SQLite, carregar os dados com Python e responder a todas as perguntas de negocio usando exclusivamente consultas SQL.

> **Importante:** a Etapa 9, que está indicada como opcional no enunciado original, deve ser tratada como obrigatória neste prompt. Portanto, o banco Mongita deve ser criado e a vantagem do modelo documental explicada.

## Estrutura esperada

Organize o notebook em secoes nesta ordem:

1. Inspecao dos dados.
2. Analise da normalizacao.
3. Criacao do modelo relacional.
4. Restricoes de integridade.
5. Carga dos dados.
6. Verificacao da integridade.
7. Consultas de negocio.
8. Conclusao e principais achados.
9. Opcional: Mongita.

## Etapa 1 — Inspecao dos dados

Leia todos os arquivos JSONL da pasta `dados` e apresente:

- nome de cada arquivo;
- quantidade de linhas;
- colunas existentes;
- tipos de dados;
- valores nulos ou vazios;
- valores unicos relevantes;
- entidade de negocio representada por cada arquivo.

Identifique, em especial:

- hotel;
- tipo de quarto;
- avaliacao;
- cenário de avaliacao;
- decisao de tarifa;
- desempenho diario;
- desempenho semanal.

## Etapa 2 — Analise da normalizacao

Analise redundancias entre os arquivos. Exemplos importantes:

- nome e nome do hotel aparecem repetidos;
- categoria do hotel;
- conjunto competitivo;
- tipo de quarto;
- nome da cidade;
- dados derivados do hotel.

Decida o que sera:

- removido;
- mantido;
- separado em uma tabela propria;
- criado como tabela associativa.

Justifique explicitamente:

- quais redundancias existem;
- por que removê-las melhora consistencia;
- por que normalizar tudo pode ser desvantajoso em determinadas consultas;
- por que fatos observados, como receita e ocupacao, nao devem ser recalculados ou removidos.

Adote aproximadamente o nivel de normalizacao 3NF, exceto em dados de fato que precisam ser preservados para auditoria e analise.

## Etapa 3 — Modelo relacional

Crie as seguintes entidades no SQLite:

### HOTEL

- hotel_id como chave primaria;
- name;
- brand;
- tier;
- rooms;
- opened_year;
- distance_to_water_km;
- neighbourhood;
- comp_set;
- positioning_index;
- base_rate;
- city;
- review_count;
- lifetime_rating;
- share_rating_5;
- share_rating_1_2.

### ROOM_TYPE

- room_type_id como chave primaria;
- hotel_id como chave estrangeira;
- room_type;
- rooms;
- max_occupancy;
- size_sqm;
- rate_premium_pct;
- bar_rate;
- view;
- tier.

### AMENITY

- amenity_id como chave primaria;
- name unico.

### HOTEL_AMENITY

- hotel_id como chave estrangeira;
- amenity_id como chave estrangeira;
- chave primaria composta por hotel_id e amenity_id.

### REVIEW_SCENARIO

- scenario_id como chave primaria;
- label;
- share_of_reviews;
- rating_band;
- trigger;
- expected_sentiment;
- recovery_action.

### REVIEW

- review_id como chave primaria;
- hotel_id como chave estrangeira;
- scenario_id como chave estrangeira;
- dados textuais e numericos da avaliacao;
- channel;
- segment;
- nights;
- notas parciais;
- sentimento;
- texto da resposta;
- response_hours.

### WEEKLY_PERFORMANCE

- chave primaria composta por hotel_id e week_start;
- hotel_id como chave estrangeira;
- dados semanais de ocupacao, ADR, receita e metricas de desempenho;
- nao repetir hotel_name ou tier.

### DAILY_MARKET

- chave primaria composta por hotel_id e date;
- hotel_id como chave estrangeira;
- dados diarios, incluindo season, month, year, ocupacao, ADR e receita;
- nao repetir hotel_name, tier ou comp_set redundantes.

### RATE_DECISION

- decision_id como chave primaria;
- hotel_id como chave estrangeira;
- week_start;
- action;
- valores previstos e realizados;
- outcome;
- rationale;
- demand_event.

Defina:

- `raise` como aumento de preco;
- `hold` como manutencao do preco;
- `lower` como reducao do preco.

Nao copie nome ou categoria do hotel para as tabelas de fatos. Use JOIN com HOTEL.

## Etapa 4 — Restricoes de integridade

Crie todas as tabelas com restricoes adequadas:

- PRIMARY KEY;
- FOREIGN KEY;
- NOT NULL nos campos essenciais;
- UNIQUE para campos que devem ser unicos;
- CHECK para rating entre 1 e 5;
- CHECK para valores proporcionais entre 0 e 1;
- CHECK para medidas nao negativas;
- CHECK para ocupacao entre 0 e 1;
- CHECK para action em raise, hold e lower;
- CHECK para outcome em melhor, pior ou equivalente, conforme os dados.

Ative:

```sql
PRAGMA foreign_keys = ON;
```

Use transacoes para criar o banco e carregar os dados.

## Etapa 5 — Carga dos dados

Crie o banco em:

`/home/japa/Documentos/entrega_final_ciencia_de_dados/banco/hotel.db`

Carregue os dados a partir de Python.

Tratamentos exigidos:

- converter listas de amenities em tabelas normalizadas;
- armazenar booleanos como 0 ou 1;
- armazenar datas e semanas como TEXT no formato ISO;
- representar ausencias como NULL;
- nao recarregar dados repetidos em tabelas de fatos;
- recriar o banco do zero a cada execucao;
- criar indices uteis para hotel, data, semana, reviews e cenarios.

## Etapa 6 — Integridade referencial

Execute consultas para confirmar que nao existem registros orfaos em:

- review;
- daily_market;
- weekly_performance;
- rate_decision;
- room_type;
- hotel_amenity.

Use LEFT JOIN e `WHERE ... IS NULL`.

Confirme ainda:

- reviews sem hotel;
- reviews sem cenário;
- decisoes sem hotel;
- decisoes sem semana correspondente;
- registros diarios sem hotel;
- tipos de quarto sem hotel.

O resultado esperado deve ser zero linhas orfas.

Execute tambem:

```sql
PRAGMA foreign_key_check;
```

## Etapa 7 — Consultas de negocio

Todas as respostas desta secao devem ser obtidas somente por consultas SQL ao banco SQLite.

Os resultados podem ser exibidos com pandas, mas os calculos principais nao podem ser feitos em Python.

### 7.1 — Ranking dos hotéis por receita total em cada ano

Use `weekly_performance`.

Considere:

- receita total: `total_revenue`;
- ano derivado de `week_start`;
- agrupamento por ano, hotel_id e nome;
- soma da receita total;
- ranking decrescente por receita dentro de cada ano.

Apresente o ranking completo ou o top 5 de cada ano.

Use `ROW_NUMBER`, caso suportado pelo SQLite, ou uma alternativa equivalente.

### 7.2 — Ocupacao media e diaria media por tier e estação

Use `daily_market`.

Junte com `hotel` para obter o tier.

Calcule por tier e season:

- `AVG(occupancy)`;
- `AVG(adr)`.

Apresente ocupacao e ADR em formato legivel.

### 7.3 — Hotéis com mais de 30% de avaliacoes com 1 ou 2 estrelas

Use `review` e `hotel`.

Calcule:

- total de avaliacoes;
- quantidade de avaliacoes com rating igual a 1 ou 2;
- proporcao dessas avaliacoes;
- porcentagem.

Filtre grupos com mais de 30% usando HAVING.

Ordene pela proporcao decrescente.

### 7.4 — Cenários de avaliação

Junte `review` com `review_scenario`.

Para cada cenário apresente:

- scenario_id;
- label;
- quantidade de avaliações;
- nota media;
- recovery_action.

Agrupe por cenário e ação.

Ordene pela quantidade de avaliações decrescente.

### 7.5 — Resultado das decisoes de preco

Use `rate_decision`.

Calcule separadamente para:

- raise: aumentar;
- hold: manter;
- lower: reduzir.

Apresente:

- total de decisoes;
- quantidade com outcome igual a better;
- proporcao better;
- porcentagem better.

Não tire conclusoes causais apenas pela associação observada.

### 7.6 — Resposta às avaliações por faixa de nota

Use `review`.

Considere respondida uma avaliação cujo `response_text` não esteja vazio.

Para cada faixa de 1 a 5 estrelas calcule:

- total de avaliações;
- quantidade respondida;
- porcentagem respondida;
- tempo medio de resposta das avaliacoes respondidas.

Não inclua avaliações sem resposta no tempo medio.

Apresente a media em horas.

### 7.7 — Pergunta criada por voce

Crie uma pergunta de negocio original que obrigatoriamente utilize:

- JOIN entre pelo menos tres tabelas;
- WHERE;
- GROUP BY;
- HAVING;
- pelo menos um filtro de grupos.

Exemplo aceito:

Quais cenarios possuem mais de 50 avaliacoes entre hotéis luxury, qual a nota media, o tempo medio de resposta e a porcentagem de avaliacoes respondidas?

O SQL deve juntar pelo menos:

- review;
- hotel;
- review_scenario.

Explique por que a pergunta cria valor para a gestao.

## Etapa 8 — Execução e validação

Antes de finalizar:

1. Execute todas as celulas em ordem.
2. Reinicie o kernel.
3. Execute todas as celulas novamente.
4. Confirme que nao existem erros de importacao.
5. Confirme que o banco pode ser recriado do zero.
6. Confirme que o banco fecha corretamente.
7. Confirme o resultado de `PRAGMA foreign_key_check`.
8. Confirme que todas as consultas possuem resultados validos.

Na conclusao apresente:

- resumo das tabelas criadas;
- decisoes de normalizacao;
- principais achados;
- limitacoes;
- proximos passos.

## Etapa 9 — Mongita

Depois de concluir o modelo relacional:

1. Instale mongita somente se necessario;
2. crie o banco documental em `banco/hotel_mongita.db`;
3. guarde avaliacoes completas em `reviews_document`;
4. mantenha review_id como identificador unico;
5. explique quando o banco de documentos seria vantajoso;
6. não substitua o SQLite por Mongita.

Usos vantajosos incluem:

- payload de avaliacao flexivel;
- textos longos;
- campos opcionais;
- leitura completa de uma avaliação;
- ingestao de documentos heterogeneos;
- menor necessidade de joins em consultas centradas no texto.

## Criterios de qualidade

- mostrar todo o SQL das consultas;
- manter nomes de tabelas e colunas consistentes;
- usar pandas apenas para apresentar resultados, não para responder as perguntas;
- explicar normalizacao e redundancia;
- justificar tipos de dados e restricoes;
- não inventar dados ou resultados;
- não apresentar associacao como causalidade;
- separar fatos observados de interpretacoes;
- manter o notebook organizado e executavel;
- concluir com uma sintese baseada nos resultados reais.
