# Prompt inicial — Etapa 2: Análise estatística

```markdown
# Instrução

Utilize o notebook `02_estatistica.ipynb`, os dados disponíveis no projeto e os conhecimentos de estatística necessários para responder às questões propostas.

## Conhecimentos a mobilizar

Utilize conceitos de:

- população e amostra;
- organização e agrupamento de dados;
- medidas de tendência central;
- frequência absoluta, relativa e acumulada;
- média e mediana;
- efeito de valores extremos;
- dispersão;
- desvio padrão;
- variância;
- correlação;
- correlação espúria;
- interpolação;
- extrapolação.

## 1. Retrato do mercado

### Ocupação típica por tier

Responda:

**Qual é a ocupação típica de cada tier: luxury, upscale, boutique, midscale e economy?**

Para cada tier:

- decida se a média ou a mediana descreve melhor o valor típico;
- justifique a medida escolhida;
- considere o efeito de valores extremos;
- considere a quantidade de hotéis disponíveis em cada tier;
- apresente os resultados em uma tabela.

Não utilize diretamente apenas os registros diários sem explicar o nível de agrupamento adotado.

Justifique por que a ocupação média ou mediana representa melhor o típico em cada situação.

### Variabilidade da diária

Responda:

**Qual tier possui a diária, ADR, mais variável ao longo do ano?**

Indique:

- a medida utilizada;
- o cálculo realizado;
- por que essa medida é adequada;
- se a variabilidade é absoluta ou proporcional;
- o resultado por tier.

Diferencie desvio padrão, variância e coeficiente de variação quando for necessário para fundamentar a resposta.

Justifique a medida escolhida.

### Distribuição das notas das avaliações

Construa a distribuição das notas de 1 a 5 estrelas contendo:

- frequência absoluta;
- frequência relativa;
- frequência acumulada;

Apresente também o cálculo da frequência acumulada relativa.

Responda:

**Que porcentagem das avaliações possui 3 estrelas ou menos?**

Apresente a tabela completa.

Justifique como a frequência acumulada permite obter a resposta.

## 2. Sazonalidade e eventos

### Meses e dias da semana

Responda:

- Em quais meses a ocupação é mais alta?
- Em quais meses a diária é mais alta?
- Em quais dias da semana a ocupação é mais alta?
- Em quais dias da semana a diária é mais alta?

Apresente:

- os resultados calculados;
- o método de agrupamento;
- os valores médios utilizados;
- as conclusões em texto.

### Noites com evento e noites comuns

Compare as noites com evento de demanda com as noites sem evento.

Determine:

- a ocupação média das noites com evento;
- a ocupação média das noites comuns;
- a mudança média da ocupação;
- a ADR média das noites com evento;
- a ADR média das noites comuns;
- a mudança média da ADR;
- se a diferença é semelhante em todos os tiers;
- se existe diferença entre tiers.

Apresente os resultados para o mercado inteiro e por tier.

Apresente diferenças de ocupação em pontos percentuais.

Apresente diferenças de ADR na unidade utilizada pelos dados.

Não apresente associação observada como causalidade.

## 3. Relações entre variáveis

### Ocupação e ADR

Responda:

**Existe correlação entre ocupação e diária?**

Determine:

- se a correlação é positiva ou negativa;
- a intensidade da relação;
- o resultado para o mercado inteiro;
- o resultado dentro de cada tier;
- se o resultado muda ao segmentar os dados;
- o que essa diferença revela.

Explique o conceito de correlação utilizado.

Não interprete correlação como prova de causalidade.

### Nota média semanal e desempenho financeiro

Analise a relação entre:

- nota média semanal do hotel;
- desempenho financeiro na mesma semana.

Utilize TRevPAR como medida de desempenho financeiro.

Responda:

- Existe correlação entre essas variáveis?
- A relação pode ser causal?
- A relação pode ser espúria?
- Que fatores externos podem afetar simultaneamente as duas variáveis?

Diferencie claramente associação, causalidade e correlação espúria.

Apresente o resultado geral e o resultado por tier.

### Notas parciais e nota geral

Analise a relação entre a nota geral e as notas parciais de:

- limpeza;
- conforto;
- serviço;
- localização;
- custo-benefício;
- sono.

Responda:

**Quais notas parciais acompanham mais a nota geral?**

Apresente uma tabela ou outra representação comparável ordenada pela intensidade da relação.

Explique que associação não prova que melhorar uma nota parcial isoladamente produzirá um determinado aumento na nota geral.

## 4. Projeção

Escolha um hotel.

Com base nos dados dos dois anos disponíveis:

- calcule a medida anual escolhida;
- utilize o hotel selecionado;
- faça uma extrapolação simples para 2029;
- explique o método utilizado;
- diferencie interpolação e extrapolação;
- apresente os valores observados e o resultado projetado;
- liste as limitações da projeção.

Pode-se utilizar ocupação ou receita.

Justifique a escolha da medida e do hotel.

Indique por que a projeção é frágil.

Considere limitações como:

- poucos pontos temporais;
- tendência não constante;
- sazonalidade;
- eventos;
- mudanças de preço;
- mudanças de capacidade;
- alterações no mercado;
- dados futuros desconhecidos;
- ausência de um modelo mais complexo;
- possíveis valores fora de limites reais.

Não apresente a projeção como previsão garantida.

## Requisitos de apresentação

O notebook deve:

- executar sem erros;
- utilizar Python e Pandas, se Python for escolhido;
- conter cálculos verificáveis;
- apresentar tabelas de resultados;
- conter células Markdown explicativas;
- justificar as medidas escolhidas;
- diferenciar média e mediana;
- diferenciar desvio padrão e variância;
- diferenciar pontos percentuais e variação relativa;
- diferenciar correlação e causalidade;
- diferenciar interpolação e extrapolação;
- apresentar resultados em unidades compreensíveis;
- conter uma conclusão em texto de no máximo uma página;
- manter a conclusão baseada nos dados apresentados.

Se uma planilha tiver sido escolhida, deve ser entregue em conjunto com a documentação das transformações realizadas nos dados.

## Limitações obrigatórias

Inclua uma seção que explicite:

- os limites da análise descritiva;
- os limites da correlação;
- os limites da comparação entre grupos;
- os limites da análise de poucos hotéis ou poucas observações;
- os limites da extrapolação;
- fatores externos não controlados;
- possíveis interpretações espúrias;
- ausência de evidência causal quando não houver análise adequada.

## Conclusão

Finalize o notebook com uma síntese que responda às quatro partes da Etapa 2:

1. retrato do mercado;
2. sazonalidade e eventos;
3. relações entre variáveis;
4. projeção.

A conclusão deve indicar os principais achados e suas limitações.

Não ultrapasse uma página de texto na conclusão.
```
