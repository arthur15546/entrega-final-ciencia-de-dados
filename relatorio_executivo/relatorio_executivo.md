# Relatório Executivo — Desempenho dos hotéis de Port Alder

**Público:** diretoria da associação de hoteleiros  
**Base analisada:** 14 hotéis, 2027–2028; 12.077 avaliações e 1.442 decisões semanais de preço. Os valores monetários mantêm a unidade fornecida nos dados, cuja moeda não está identificada.

## Síntese para decisão

O mercado apresenta diferenças importantes entre hotéis do mesmo tier. Os índices competitivos permitem identificar quem está acima ou abaixo da paridade de tarifa e ocupação; não são, por si sós, prova de melhor rentabilidade. As reduções de preço tiveram a maior proporção observada de resultados classificados como “better”, mas a diferença para as outras ações é modesta e não demonstra causalidade. Nas avaliações, há sinais claros de experiências muito positivas e problemas operacionais recorrentes; a relação entre nota semanal e desempenho financeiro é fraca quando observada dentro dos tiers.

## 1. Como cada hotel se compara com concorrentes diretos?

O painel compara cada estabelecimento por tier e mostra ARI (posição relativa de tarifa) e MPI (posição relativa de ocupação), com paridade em 100. O RGI resume a posição de receita de quartos em relação ao conjunto competitivo. Esses índices são mais adequados à comparação entre concorrentes do que a receita total isolada, mas a documentação dos dados não detalha suas fórmulas; devem ser lidos como indicadores relativos, não como métricas financeiras absolutas.

**Gráfico 1 — Mapa de posicionamento competitivo (ARI × MPI), no painel:** a linha em 100 separa os quadrantes acima/abaixo da paridade. Os índices anuais mostram diferenças dentro do mesmo tier:

| Hotel (tier) | ARI 2027 | MPI 2027 | RGI 2027 |
|---|---:|---:|---:|
| Harborlight Suites (upscale) | 112,9 | 102,9 | 116,1 |
| Alder & Quay Hotel (upscale) | 102,5 | 100,8 | 103,4 |
| Seabright Grand (upscale) | 94,1 | 99,5 | 93,6 |
| Willowmere Lodge (upscale) | 90,9 | 96,1 | 87,3 |
| The Lantern House (boutique) | 138,4 | 99,9 | 138,3 |
| The Wren Rooms (boutique) | 87,4 | 102,2 | 89,3 |

Harborlight lidera entre os upscale em RGI; Alder & Quay está pouco acima da paridade, enquanto Seabright e Willowmere ficam abaixo. Entre os boutique, Lantern combina tarifa muito acima da paridade com ocupação próxima dela; Wren tem ocupação acima, mas tarifa e RGI abaixo.

O retrato de 2028 é semelhante: Harborlight segue com RGI de 116,6 e Willowmere com 87,0; não se observa uma mudança suficiente para afirmar que a posição competitiva tenha sido revertida. Para a diretoria, a prioridade é investigar práticas comerciais e operacionais dos hotéis abaixo de 100 no RGI e entender a disposição a pagar no Lantern House, sem concluir que apenas reduzir ou elevar tarifas resolverá os resultados.

## 2. As decisões semanais de preço estão funcionando?

**Gráfico 2 — Proporção de decisões com resultado “better”, por ação (consulta SQL do banco):**

| Ação | Decisões | “Better” | Proporção |
|---|---:|---:|---:|
| Reduzir (`lower`) | 189 | 81 | 42,86% |
| Aumentar (`raise`) | 634 | 243 | 38,33% |
| Manter (`hold`) | 619 | 233 | 37,64% |

Reduções apresentam a maior proporção observada de resultados “better”, cerca de 4,5 pontos percentuais acima de aumentos e 5,2 pontos acima de manutenções. Isso é um sinal para investigar em quais condições as reduções funcionam, não uma recomendação geral para baixar preços: houve apenas 189 reduções, as ações podem ter sido escolhidas em situações diferentes, e o resultado observado não isola outros fatores. A amostra de decisões também é desigual entre ações. O painel ajuda a acompanhar ocupação e desempenho mensal, mas a comparação causal exigiria um desenho analítico que controlasse contexto, demanda, concorrência e sazonalidade.

## 3. O que os hóspedes dizem e isso se relaciona ao resultado financeiro?

**Gráfico 3 — Frequência acumulada das avaliações (notebook estatístico) e volume por cenário (painel):** em 12.077 avaliações, **55,8% têm nota igual ou inferior a 3**. Há experiências muito positivas: “Stay exceeded expectations” é o cenário mais frequente na consulta do banco, com 1.840 avaliações e nota média 4,84. Também aparecem problemas concretos: billing tem média 1,63 e cleanliness 1,69. No recorte por hotel, Northgate Inn tem 39,14% de avaliações com 1 ou 2 estrelas, a maior proporção entre os hotéis consultados. Esses achados sugerem priorizar a investigação de cobrança e limpeza e acompanhar a resposta dos hotéis, sem assumir que um cenário isolado representa toda a experiência.

Na análise semanal, a correlação de Pearson entre nota média e TRevPAR foi **0,229** em 1.429 semanas válidas — associação positiva fraca no conjunto. Dentro dos tiers, as correlações ficaram próximas de zero (entre −0,060 e 0,040). Portanto, não há evidência de uma relação consistente entre nota e desempenho financeiro dentro de cada categoria, muito menos de que uma mudança de nota cause um aumento de receita. Diferenças estruturais entre tiers, eventos, sazonalidade, volume de avaliações por semana e outros fatores podem influenciar simultaneamente as medidas.

## Limitações e próximos passos

Os dados cobrem um mercado fictício e 14 hotéis em dois anos; resultados não devem ser generalizados automaticamente para outros mercados ou períodos. Alguns tiers têm apenas dois hotéis, e avaliações semanais podem representar volumes diferentes de hóspedes. Índices competitivos são relativos e suas fórmulas detalhadas não estão documentadas no projeto. As relações entre variáveis e resultados das decisões são observacionais, não experimentais; não demonstram causalidade. A moeda dos valores monetários também não foi informada.

Recomenda-se usar o painel para localizar diferenças e acompanhar métricas, investigar individualmente os hotéis abaixo da paridade de RGI, revisar os cenários de cobrança e limpeza e avaliar decisões de preço segmentando por demanda, hotel e período. Qualquer mudança de política deve ser acompanhada por métricas e comparação apropriada, em vez de ser atribuída diretamente a uma única variável.

### Referências visuais do projeto

- **Gráfico 1:** “Posicionamento competitivo dos hotéis” — mapa ARI × MPI com linha de paridade em 100 no painel Streamlit.
- **Gráfico 2:** consulta 7.5, “Decisões por ação e outcome better”, no notebook da Etapa 3.
- **Gráfico 3:** “Cenários das avaliações” no painel; frequência acumulada das notas e análise de TRevPAR no notebook da Etapa 2.
