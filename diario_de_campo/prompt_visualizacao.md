# Prompt — Etapa 4: Visualização de dados em Python

## Instrução

Utilize o notebook `notebooks/04_visualizacao.ipynb`, os dados disponíveis em `dados/`, os resultados e definições documentados nas etapas anteriores e os conhecimentos de visualização de dados necessários para concluir integralmente esta etapa.

O foco desta etapa são os gráficos e as conclusões que eles sustentam. Organize as figuras e o código de modo que seja simples reaproveitar os gráficos posteriormente no Streamlit, sem transformar o notebook em um dashboard ou duplicar a análise.

## Conhecimentos a mobilizar

Utilize os conhecimentos do Módulo 3 — Visualização:

- escolha do tipo de gráfico de acordo com a pergunta e os dados;
- gráficos de barras;
- gráficos de linhas e áreas;
- gráficos de dispersão e quadrantes;
- gráficos de pizza e suas limitações;
- limpeza visual, rótulos e paletas;
- diagramas de Sankey;
- nuvens de palavras;
- gráficos interativos;
- uso responsável de IA generativa na análise, quando aplicável.

## Organização do notebook

Estruture o notebook nesta ordem:

1. Objetivo, escopo e decisões de visualização.
2. Carregamento e preparação dos dados.
3. Configuração visual comum e funções reutilizáveis.
4. Visualizações e respostas às perguntas.
5. Síntese dos achados e limitações.
6. Referências às fontes e às definições utilizadas.

Use Python e Pandas para preparar os dados. Leia os arquivos JSONL necessários de `dados/`; não dependa de caminhos absolutos da máquina. Carregue apenas os campos necessários para cada visualização sempre que isso deixar o código mais claro.

Antes de construir os gráficos:

- confira as colunas, tipos, unidades, valores ausentes e granularidade dos arquivos relevantes;
- confirme as definições dos índices e das métricas no `README.md` e na documentação disponível no projeto;
- procure as definições em notebooks e prompts anteriores se o README não as trouxer;
- não invente definições nem trate variáveis com nomes parecidos como equivalentes;
- registre de forma breve a fonte, a unidade, a granularidade e as transformações usadas.

Se uma definição necessária não estiver documentada, explicite a limitação e justifique a interpretação adotada a partir dos dados e das etapas anteriores. Não afirme que o README define algo que ele não define.

## Requisitos para todas as visualizações

Produza **no mínimo oito visualizações**, cobrindo todas as perguntas desta etapa. Cada visualização deve ter, junto ao gráfico:

- uma justificativa curta para o tipo de gráfico escolhido;
- uma ou duas frases indicando o que o leitor deve concluir;
- a fonte dos dados, a unidade das medidas e o nível de agregação;
- o tratamento de valores ausentes ou filtros que alterem a leitura.

Aplique a todos os gráficos as práticas da Aula 10:

- títulos informativos que antecipem a conclusão ou a pergunta respondida;
- eixos com nomes e unidades explícitos;
- categorias e períodos em ordem lógica;
- paleta consistente em todo o notebook, com cores semanticamente estáveis;
- contraste e tamanhos legíveis;
- rótulos apenas quando ajudarem a leitura;
- escalas honestas, sem cortes que exagerem diferenças;
- ausência de efeitos 3D, decoração ou elementos que não contribuam para interpretar os dados.

Não use cor como único meio de distinguir séries. Inclua legenda quando necessária e evite rótulos sobrepostos. Para percentuais, indique claramente se os dados estão em proporção (`0–1`) ou porcentagem (`0–100%`); para valores monetários, mantenha a unidade monetária dos dados e não invente uma moeda.

## Reaproveitamento no Streamlit

Escreva o código dos gráficos para que possa ser reutilizado depois em um aplicativo Streamlit:

- separe a preparação dos dados da construção das figuras;
- crie funções pequenas para construir gráficos, recebendo DataFrames e parâmetros necessários;
- faça cada função retornar a figura (por exemplo, um objeto Plotly ou Matplotlib), em vez de depender exclusivamente de efeitos colaterais;
- mantenha nomes de funções, colunas e parâmetros claros e consistentes;
- evite caminhos absolutos, estado global desnecessário, widgets dentro das funções de gráfico e código específico do notebook que impeça reutilização;
- mantenha os filtros da análise explícitos e fáceis de converter em controles do Streamlit;
- use Plotly para pelo menos um gráfico interativo e produza figuras que possam ser exibidas diretamente com `st.plotly_chart`;
- não é necessário criar o aplicativo Streamlit nesta etapa nem criar arquivos adicionais, a menos que sejam indispensáveis para a reutilização.

Não sacrifique a clareza ou a validade analítica apenas para tornar uma figura interativa.

## 1. Comparação dos tiers

Responda:

**Como os tiers se comparam em ocupação, diária e receita por quarto disponível?**

Compare os tiers disponíveis nos dados, incluindo luxury, upscale, boutique, midscale e economy quando houver observações.

Apresente uma visualização que permita comparar, para cada tier:

- ocupação;
- ADR (diária média);
- RevPAR (receita de quartos por quarto disponível).

Como as medidas têm unidades e escalas diferentes, não as coloque em um único eixo que torne alguma delas ilegível. Prefira painéis alinhados, pequenos múltiplos ou gráficos separados com a mesma ordenação de tiers. Informe que o RevPAR não é receita total, mas receita de quartos por quarto disponível.

Explique a granularidade e o método de agregação utilizados. Evite que hotéis com mais registros ou mais quartos recebam peso implícito sem que isso seja uma decisão consciente. Se usar médias simples por registro ou médias ponderadas, justifique e informe como os resultados devem ser interpretados.

## 2. Evolução temporal e eventos de demanda

Responda:

**Como a ocupação e a diária evoluem ao longo dos dois anos? Os eventos de demanda aparecem no gráfico?**

Construa uma visualização temporal com a evolução de ocupação e ADR ao longo dos dois anos disponíveis. Como as duas medidas têm unidades distintas, use painéis alinhados ou outra solução que não confunda suas escalas.

Inclua eventos de demanda de forma legível, utilizando os campos de evento existentes nos dados. Caso haja muitos eventos ou categorias, escolha uma codificação que não sobrecarregue o gráfico e explique como interpretá-la. Não marque datas ou eventos que não estejam nos dados.

Deixe claro:

- se os valores são diários, semanais ou agregados por período;
- como os valores de vários hotéis foram combinados;
- como períodos sem observações foram tratados;
- se a sazonalidade ou a agregação pode ocultar variações de hotéis individuais.

Não atribua causalidade aos eventos apenas porque coincidem com mudanças de ocupação ou ADR.

## 3. Mapa de posicionamento competitivo

Responda:

**Quais hotéis cobram caro e enchem? Quais cobram caro e ficam vazios?**

Crie um gráfico de dispersão com um ponto por hotel e quadrantes que compare:

- o índice de preço/posicionamento contra os concorrentes no eixo horizontal;
- o índice de ocupação contra os concorrentes no eixo vertical.

Antes de definir as linhas de referência:

- consulte o `README.md` e as fontes do projeto para verificar o significado, a escala e o sentido de cada índice;
- determine qual valor representa paridade com os concorrentes (por exemplo, `1` ou `100`, conforme a definição real);
- use esse valor como referência nos eixos e justifique por que ele separa os quadrantes;
- não confunda um índice de posicionamento cadastral com uma medida de preço realizado sem confirmar sua definição.

Escolha um período e uma forma de agregação coerentes para obter um ponto por hotel. Se os índices variarem dia a dia, explique como foram resumidos e por que essa sumarização representa o período. Não misture médias de índices e razões de valores sem justificar.

Identifique os quadrantes em linguagem de negócio, como preço acima/abaixo da paridade e ocupação acima/abaixo da paridade. Destaque hotéis com nomes legíveis. Use Plotly neste gráfico ou em outra visualização para fornecer tooltips úteis, por exemplo nome do hotel, tier, índices e período. Inclua contexto suficiente para interpretar pontos próximos às linhas de referência.

Se a definição ou o valor de paridade não puder ser verificado nos materiais do projeto, não invente uma linha: documente a lacuna e apresente a escolha adotada como hipótese.

## 4. Desvio entre preço praticado e diária MARS

Responda:

**Quanto o preço praticado se afasta da diária MARS?**

Mostre a distribuição desse desvio por hotel ou por tier. Prefira uma representação que revele a dispersão e os valores extremos, como boxplot, pontos com distribuição ou pequenos múltiplos; não use somente médias se isso esconder a variação.

Use a definição de MARS documentada nos dados. Se calcular o desvio, apresente a fórmula e use uma forma percentual comparável, como:

`(ADR - mars_rate) / mars_rate * 100`

Confirme que `mars_rate` é positiva e que ADR e MARS estão na mesma unidade antes de calcular. Se houver uma variável de desvio já calculada, verifique sua definição, unidade e sinal antes de reutilizá-la.

Explique o significado do sinal:

- valores positivos: preço praticado acima da MARS;
- valores negativos: preço praticado abaixo da MARS;
- zero: paridade.

Informe a unidade do eixo, o período, a quantidade de observações e como valores nulos ou denominadores inválidos foram tratados. Não interprete o desvio como prova de que a tarifa é adequada ou inadequada.

## 5. Distribuição dos cenários das avaliações

Responda:

**Como se distribuem os cenários das avaliações?**

Apresente a quantidade e, quando útil, a participação percentual das avaliações por cenário. Use os registros de avaliações e os rótulos/descrições do arquivo de cenários, relacionando-os por identificador.

Antes de escolher pizza:

- verifique se as categorias são mutuamente exclusivas e se representam partes do mesmo total;
- confira se o número de categorias e as diferenças entre as fatias permitem uma comparação legível;
- não use pizza para comparar várias dimensões ou valores que não compõem um total;
- se a pizza não for adequada, use barras ordenadas (ou outra alternativa comparável) e explique brevemente por que ela é mais clara.

Ordene as categorias de forma que facilite a leitura e não omita cenários sem explicar o motivo. Diferencie contagem observada de `share_of_reviews` planejado ou declarado no arquivo de cenários; não trate uma proporção esperada como se fosse uma frequência calculada das avaliações.

## 6. Fluxo das avaliações — Sankey

Construa um diagrama de Sankey que mostre o fluxo de um conjunto de categorias até outro. Escolha dimensões presentes nos dados, por exemplo:

- cenário → faixa de nota;
- segmento do hóspede → canal da avaliação;
- sentimento → faixa de nota.

Escolha uma combinação com significado para a análise e volume suficiente para leitura. O diagrama deve:

- usar contagens observadas como pesos dos fluxos;
- apresentar nomes claros para nós e categorias;
- evitar misturar registros com granularidades diferentes;
- tratar valores ausentes como categoria explícita ou excluí-los com justificativa;
- evitar fluxos duplicados causados por joins ou expansão de registros;
- usar uma paleta coerente, com cores que ajudem a acompanhar as categorias sem sugerir causalidade.

Explique em uma ou duas frases o que os fluxos mais relevantes mostram e quais categorias concentram maior volume. Não descreva o Sankey como uma sequência temporal ou causal se os dados não estabelecerem essa relação.

## 7. Nuvens de palavras — avaliações positivas e negativas

Construa nuvens de palavras comparáveis usando o texto das avaliações positivas e negativas.

Defina explicitamente como positivo e negativo serão identificados, usando uma coluna de sentimento existente ou uma regra previamente documentada. Não classifique o texto por uma regra improvisada sem validá-la.

Para o pré-processamento:

- converta o texto de forma consistente;
- remova pontuação e elementos sem significado analítico;
- remova stopwords em português e, se os textos estiverem em outro idioma, stopwords adequadas ao idioma;
- acrescente stopwords específicas do domínio somente quando forem comuns e pouco informativas;
- preserve palavras relevantes para a experiência do hóspede;
- registre os critérios de limpeza;
- evite remover palavras manualmente só para produzir uma nuvem visualmente conveniente.

Use o mesmo conjunto de configurações e escalas para as nuvens positiva e negativa, para facilitar a comparação. Informe a quantidade de avaliações incluídas em cada grupo e a configuração principal utilizada, como número máximo de palavras.

Explique que o tamanho das palavras representa frequência (ou a métrica escolhida), não importância, causalidade ou representatividade de todos os hóspedes. Se uma dependência necessária para gerar nuvens não estiver disponível, identifique claramente a dependência; não apresente uma alternativa como se fosse uma nuvem de palavras.

## 8. Gráfico interativo em Plotly

Inclua pelo menos um gráfico interativo em Plotly. O mapa de posicionamento pode cumprir esse requisito; caso não tenha tooltips suficientes, adicione ou adapte uma figura interativa.

O gráfico deve:

- ter rótulos claros, eixos com unidades e título informativo;
- exibir tooltips úteis, com campos interpretáveis para quem analisa os hotéis;
- manter escalas e categorias coerentes com a versão estática, quando houver;
- permitir explorar pontos ou séries sem esconder a informação essencial;
- retornar um objeto de figura que possa ser exibido no Streamlit.

Explique qual interação é útil para a análise. Não conte uma versão duplicada da mesma figura como uma visualização adicional para atingir o mínimo de oito.

## Validação e execução

Antes de concluir:

1. Execute todas as células em ordem, com um kernel reiniciado.
2. Confirme que o notebook executa sem erros e pode ser executado novamente sem depender do estado anterior.
3. Confirme que cada pergunta tem ao menos uma visualização correspondente.
4. Confirme que há pelo menos oito visualizações distintas no total.
5. Confirme que o gráfico interativo funciona e que seus tooltips contêm os campos prometidos.
6. Confirme que a comparação entre tiers não mistura unidades em um eixo inadequado.
7. Confirme que as linhas do mapa competitivo correspondem à paridade definida nas fontes.
8. Confirme que o cálculo de desvio da MARS usa unidades compatíveis e denominador válido.
9. Confirme que o Sankey usa contagens sem duplicações acidentais.
10. Confirme que as nuvens de palavras usam grupos definidos e pré-processamento documentado.
11. Revise títulos, eixos, legendas, paleta, escalas e legibilidade em todas as figuras.

## Conclusão e limitações

Finalize com uma síntese curta baseada nas figuras e nos cálculos reais, incluindo:

- as diferenças mais relevantes entre tiers;
- os padrões temporais observados e a relação visual com os eventos;
- o posicionamento competitivo que merece atenção;
- a distribuição do desvio em relação à MARS;
- os padrões mais claros nas avaliações e nos fluxos;
- as palavras que mais diferenciam os textos positivos e negativos;
- as limitações da agregação, cobertura dos dados, índices e visualizações.

Separe observações de interpretações. Não apresente correlação visual, coincidência temporal ou frequência de palavras como evidência de causalidade.

## Critérios de qualidade

- responder a todas as perguntas sem inventar resultados;
- usar pelo menos oito visualizações distintas;
- justificar a escolha do tipo de gráfico e registrar a conclusão de cada figura;
- manter definições, unidades e granularidades explícitas;
- seguir as práticas de limpeza visual da Aula 10;
- escolher pizza somente se os dados e a legibilidade justificarem;
- incluir um Sankey e nuvens de palavras positivas e negativas;
- incluir pelo menos um gráfico interativo Plotly com tooltips úteis;
- manter as figuras e funções fáceis de reaproveitar no Streamlit;
- evitar conclusões causais que os dados não sustentam;
- manter o notebook organizado, reexecutável e baseado nos arquivos do projeto.
