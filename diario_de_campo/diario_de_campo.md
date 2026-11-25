# Diário de Campo — Arthur Maciel de Oliveira

## 3 Melhores Prompts que Usei

### Prompt 1: Planejar uma análise estatística verificável

**Módulo:** Etapa 2 — Análise estatística

**Prompt enviado (trecho exato do arquivo `prompt_analise_estatistica.md`):**

> Utilize o notebook `02_estatistica.ipynb`, os dados disponíveis no projeto e os conhecimentos de estatística necessários para responder às questões propostas.

**Por que foi bom:**

O prompt completo organizou a análise em perguntas e pediu justificativas para agrupamentos, medidas e limitações. Isso ajudou a comparar primeiro os hotéis e depois os tiers, em vez de tratar cada registro diário como um hotel independente.

### Prompt 2: Estruturar e validar o banco relacional

**Módulo:** Etapa 3 — Banco de dados

**Prompt enviado (trecho exato do arquivo `prompt_banco_de_dados.md`):**

> Utilize o notebook `03_banco_de_dados.ipynb`, os dados da pasta `dados`, o diagrama ER da pasta `banco` e os conhecimentos de SQL e SQLite necessarios para concluir integralmente esta etapa.

**Por que foi bom:**

O prompt detalhou entidades, chaves, integridade e consultas de negócio, tornando a tarefa verificável. Também orientou a separar os dados relacionais do armazenamento documental complementar.

### Prompt 3: Criar visualizações reutilizáveis e responsáveis

**Módulo:** Etapa 4 — Visualização de dados

**Prompt enviado (trecho exato do arquivo `prompt_visualizacao.md`):**

> Utilize o notebook `notebooks/04_visualizacao.ipynb`, os dados disponíveis em `dados/`, os resultados e definições documentados nas etapas anteriores e os conhecimentos de visualização de dados necessários para concluir integralmente esta etapa.

**Por que foi bom:**

O prompt exigiu que cada gráfico declarasse fonte, unidade e agregação, além de separar medidas com escalas diferentes. Isso ajudou a produzir visualizações mais fáceis de interpretar e reaproveitar no painel.

## 1 Erro que a AI Cometeu e Como Corrigi

**Módulo:** Etapa 2 — Análise estatística

**O que pedi:**

> Compare a ocupação média dos hotéis por tier.

**O que a AI errou:**

Como a solicitação não especificava a granularidade, a resposta poderia calcular a média diretamente sobre os registros diários. Isso daria peso maior a hotéis com mais observações, em vez de comparar cada hotel de forma equilibrada.

**Como corrigi:**

Reformulei a estrutura do prompt para pedir que a ocupação fosse resumida por hotel antes da comparação entre tiers. Também explicitei unidades e a diferença entre ADR, RevPAR e TRevPAR. O detalhamento dos prompts finais ajudou a evitar que essa ambiguidade gerasse problemas nas análises seguintes.

## 1 Coisa que Aprendi Graças à Explicação da AI

**Módulo:** Etapa 4 — Visualização de dados

**O que perguntei (em essência):**

> Como escolho gráficos adequados para comparar ocupação, ADR e RevPAR?

**O que aprendi:**

Aprendi que a visualização precisa acompanhar a pergunta e respeitar o tipo e a escala de cada medida. Ocupação é uma proporção, enquanto ADR e RevPAR são valores monetários; colocá-los no mesmo eixo pode esconder diferenças e induzir a erro. Também entendi que correlações e padrões visuais ajudam a explorar os dados, mas não provam que uma variável causou outra.

**Como usei esse conhecimento depois:**

No painel, separei as métricas em visualizações próprias e usei a dispersão de ARI por MPI, com paridade em 100, para apoiar a comparação competitiva. Interpretei os gráficos como evidência descritiva: associações e coincidências observadas não demonstram causalidade.
