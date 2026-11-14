# Histórico de Interação com IA

---

## Informações gerais

| Campo | Valor |
| --- | --- |
| **Grupo** | Grupo 14 — SN-2026-GRUPO-14-NASA |
| **Integrantes** | Vitor, Lorenzo e Cauan |
| **Projeto** | CoronaFlux |
| **API NASA escolhida** | DONKI/IPS |
| **Fontes complementares discutidas e escolhidas no histórico** | DONKI/CME, DONKI/GST e JPL Horizons |
| **IA utilizada** | Claude — Anthropic |
| **Data de início** | 12/11/2026 |
| **Data de conclusão** | 12/11/2026 |
| **Repositório** | https://github.com/SN-2026-GRUPO-14-NASA/DONKI-IPS |
| **Painel** | https://sn-2026-grupo-14-nasa.github.io/DONKI-IPS/ |

---

## Interação 1 — Avaliação inicial da DONKI/MPC

**Data:** 12/11/2026

**Objetivo:** Avaliar se a DONKI/MPC atendia à proposta de coleta e visualização de eventos do clima espacial.

**Prompt enviado à IA:**

````text
oi, lê os documentos da atividade e o modelo do ai-interaction.md. A gente já tem a estrutura e um rascunho do trabalho, mas quer conferir a parte técnica. Pensamos em usar a DONKI/MPC, mesmo não estando na lista. Ela serve pra essa ideia de coletar eventos do clima espacial e mostrar num painel?
````

**Resumo da resposta:**

A IA explicou o que a MPC registra, apresentou o endpoint e sugeriu nomenclaturas, chave natural e campos. Alertou para a raridade dos eventos e para a necessidade de uma consulta histórica ampla.

**O que funcionou:**

A resposta ajudou a comparar as fontes e destacou que uma lista vazia pode ser um resultado válido.

**O que precisou ajuste:**

O grupo decidiu usar a IPS na interação seguinte. As sugestões de nomes e de chave natural da MPC não correspondem à escolha final.

<details>
<summary>Resposta da IA</summary>

A DONKI/MPC trata de eventos de cruzamento da magnetopausa, relacionados à compressão dessa região para dentro da órbita geoestacionária, geralmente após uma CME ou um vento solar intenso.

O endpoint é:

`https://api.nasa.gov/DONKI/MPC?startDate=AAAA-MM-DD&endDate=AAAA-MM-DD&api_key=SUA_CHAVE`

Se ficarem com ela, usem um repositório DONKI-MPC, um projeto DONKI-MPC-DB no Supabase e uma chave natural baseada em `mpcID`. Os campos principais são o identificador, o horário do evento, instrumentos, eventos associados e o link para o registro.

Só prestem atenção na quantidade de eventos: os eventos MPC são relativamente raros. Um período curto pode não retornar registros. Se escolherem essa API, façam uma carga histórica ampla e tratem uma resposta vazia como execução concluída com zero registros, não como erro.

Antes de fechar o banco, confiram os campos no JSON da API e a reserva do tema com o professor.

</details>

---

## Interação 2 — Escolha da DONKI/IPS e levantamento dos campos

**Data:** 12/11/2026

**Objetivo:** Identificar os campos e a chave natural da IPS antes de finalizar o banco.

**Prompt enviado à IA:**

````text
ok, vamos usar a IPS. Pelo que vimos ela tem mais eventos e dá pra filtrar pelo local de detecção. Quais campos precisamos conferir antes de fechar o banco?
````

**Resumo da resposta:**

A IA descreveu a IPS, indicou activityID como chave natural e listou campos, locais de detecção e catálogos. Sugeriu DONKI-IPS para o repositório e DONKI-IPS-DB para o projeto.

**O que funcionou:**

A definição da IPS e de seus campos orientou a organização do banco e dos filtros discutidos nas interações seguintes.

**O que precisou ajuste:**

A indicação de SWRC_CATALOG foi revista na interação 13, em que a IA informou ter encontrado M2M_CATALOG na resposta consultada.

<details>
<summary>Resposta da IA</summary>

A DONKI/IPS registra choques interplanetários: frentes de choque no vento solar, frequentemente associadas a ejeções de massa coronal, detectadas por sondas e satélites.

O endpoint é:

`https://api.nasa.gov/DONKI/IPS?startDate=AAAA-MM-DD&endDate=AAAA-MM-DD&api_key=SUA_CHAVE`

Pra organizar:

| Elemento | Definição |
| --- | --- |
| Repositório | DONKI-IPS |
| Projeto no Supabase | DONKI-IPS-DB |
| Chave natural | `activityID` |
| Exemplo de identificador | `2024-05-10T16:36:00-IPS-001` |
| Campos principais | `activityID`, `catalog`, `location`, `eventTime`, `instruments`, `linkedEvents` e `link` |
| Filtro de local | Earth, STEREO A, STEREO B, MESSENGER ou ALL |
| Catálogo, a conferir na resposta | ALL, SWRC_CATALOG ou WINSLOW_MESSENGER_ICME_CATALOG |

A IPS combina com a ideia de vocês: tem mais eventos e permite filtrar por local. Os `linkedEvents` também permitem explorar relações com outros fenômenos do clima espacial. Mantenham a carga histórica e o tratamento de períodos sem registros.

</details>

---

## Interação 3 — Revisão da ordem de trabalho e das entregas

**Data:** 12/11/2026

**Objetivo:** Conferir a sequência de banco, coleta, painel e documentação e identificar pendências.

**Prompt enviado à IA:**

````text
nosso plano é terminar banco e coleta primeiro, depois o painel e fechar a documentação. Já temos essas partes separadas no rascunho. Dá uma olhada nessa ordem e vê se estamos esquecendo alguma coisa da entrega.
````

**Resumo da resposta:**

A IA revisou infraestrutura, banco, pipeline, automação, painel e documentos. Citou os acessos do professor, os Secrets, os controles do workflow, as evidências e a atualização da planilha.

**O que funcionou:**

A resposta reuniu as tarefas e explicou a dependência entre banco, coleta e validação do painel.

**O que precisou ajuste:**

A lista serviu como orientação. Nesta interação não há confirmação de que os acessos, os documentos e as demais tarefas já estivessem concluídos.

<details>
<summary>Resposta da IA</summary>

Essa ordem faz sentido. Banco e coleta precisam funcionar antes da validação completa do painel. Enquanto a coleta não estiver pronta, dá pra adiantar a interface com dados de exemplo e ir preenchendo a documentação.

Para a infraestrutura, confiram a organização do GitHub, o repositório público, o GitHub Pages na branch `main`, o projeto do Supabase na região São Paulo e os acessos do professor previstos no enunciado: GilFerques no GitHub e o endereço institucional indicado para o Supabase.

O que precisa ficar pronto:

| Frente | Arquivos e verificações |
| --- | --- |
| Banco | `sql/setup.sql`, tabelas, chave única, RLS e permissões |
| Coleta | `scripts/fetch_nasa.py`, normalização, deduplicação, upsert e logs |
| Automação e painel | `.github/workflows/update-data.yml`, Secrets, `index.html` e Pages |
| Documentação | README, tutorial, registro de interação, reflexão, slides e evidências |

No banco, mantenham `ips_eventos` e `execucoes`. No pipeline, prevejam busca por janelas, lotes de envio, deduplicação por identificador e saída com erro quando houver falha.

No workflow, confiram `cron`, `workflow_dispatch`, `permissions: contents: read`, `concurrency` e `timeout-minutes`. No painel, incluam filtros, gráfico, tabela e a última atualização lida de `execucoes`.

Os Secrets previstos são `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` e `NASA_API_KEY`. A chave secreta do Supabase não deve aparecer no front-end, em commits ou nos prints.

Para a entrega de 13/11, às 23h59, reservem tempo para o tutorial de 5 a 15 páginas, a reflexão, a apresentação, os prints do Actions, do Table Editor e do JSON da API REST, além dos links e da atualização das colunas G e H da planilha. Um vídeo curto do funcionamento pode servir como apoio à demonstração.

</details>

---

## Interação 4 — Geração e configuração da chave NASA

**Data:** 12/11/2026

**Objetivo:** Detalhar a geração da chave NASA e seu cadastro no GitHub.

**Prompt enviado à IA:**

````text
a parte de gerar a chave da NASA ficou meio vaga no nosso tutorial. Pode explicar esse passo e onde colocar a chave no GitHub?
````

**Resumo da resposta:**

A IA explicou o cadastro no portal, o recebimento da chave, uma consulta de teste e a criação do Secret NASA_API_KEY. Recomendou manter a chave pessoal fora do código e das capturas.

**O que funcionou:**

O passo a passo explicou onde obter a chave e onde configurá-la para o pipeline.

**O que precisou ajuste:**

A URL de exemplo cobria um ano inteiro. Esse intervalo não respeita o limite de 60 dias reconhecido posteriormente no histórico e precisa ser reduzido.

<details>
<summary>Resposta da IA</summary>

Entrem em https://api.nasa.gov, procurem “Generate API Key” e preencham nome, sobrenome e e-mail. A URL da aplicação é opcional. Depois do cadastro, a chave aparece na tela e também é enviada por e-mail.

Para testar, substituam apenas `SUA_CHAVE`:

`https://api.nasa.gov/DONKI/IPS?startDate=2024-01-01&endDate=2024-12-31&api_key=SUA_CHAVE`

Uma resposta em JSON com campos como `activityID`, `location` e `eventTime` indica que a consulta foi aceita.

No GitHub, abram Settings → Secrets and variables → Actions → New repository secret e usem o nome `NASA_API_KEY`.

A chave pessoal tem limite de até 1.000 requisições por hora para a chave pessoal. Usem a DEMO_KEY apenas em verificações pontuais. Não incluam a chave pessoal no tutorial, no código ou nos prints.

</details>

---

## Interação 5 — Diagnóstico de API_KEY_INVALID

**Data:** 12/11/2026

**Objetivo:** Investigar a recusa da chave antes de modificar o script.

**Prompt enviado à IA:**

````text
testamos a consulta e apareceu isso:

`API_KEY_INVALID`  
`An invalid api_key was supplied. Get one at https://api.nasa.gov:443`

acho que copiamos a chave errada. O que vale conferir antes de mexer no script?
````

**Resumo da resposta:**

A IA orientou conferir a chave completa, espaços, quebras de linha, o marcador SUA_CHAVE, o parâmetro api_key e a mensagem recebida por e-mail. Sugeriu um teste com DEMO_KEY.

**O que funcionou:**

O diagnóstico apontou a configuração da credencial, e o grupo confirmou na interação seguinte que utilizava a chave errada.

**O que precisou ajuste:**

Foi necessário substituir a chave incorreta. A autenticação correta, isoladamente, não confirma o funcionamento de todos os parâmetros da consulta.

<details>
<summary>Resposta da IA</summary>

Testem o mesmo endereço com a DEMO_KEY. Se funcionar, confiram a chave pessoal.

Confiram se a chave foi copiada inteira, sem espaços, quebras de linha ou pontuação. Verifiquem também se o texto `SUA_CHAVE` foi substituído por completo e se o parâmetro continua escrito exatamente como `api_key=`.

Comparem com a chave recebida por e-mail. Caso o problema persista, vocês podem gerar outra chave. Não é necessário compartilhar o valor aqui para fazer essa conferência.

</details>

---

## Interação 6 — Confirmação da correção da chave

**Data:** 12/11/2026

**Objetivo:** Registrar a solução do erro de autenticação e incluí-la no tutorial.

**Prompt enviado à IA:**

````text
foi, estávamos colocando a chave errada. Agora retornou os eventos. Vamos anotar isso no tutorial também.
````

**Resumo da resposta:**

O grupo informou que corrigiu a chave e recebeu eventos. A IA recomendou guardar a chave válida em NASA_API_KEY e registrar o diagnóstico no tutorial e na reflexão.

**O que funcionou:**

O retorno dos eventos foi confirmado pelo grupo após a correção da chave.

**O que precisou ajuste:**

A correção relatada foi na chave, sem necessidade de trocar o endpoint. A orientação anterior de consultar um ano inteiro permanece como um erro distinto a revisar.

<details>
<summary>Resposta da IA</summary>

Então era a chave mesmo. Anotem isso: a URL estava certa e não foi preciso mudar o endpoint.

Guardem a chave válida no Secret `NASA_API_KEY`. Isso pode entrar na reflexão: vocês testaram a consulta e conferiram a chave antes de sair alterando o código.

Agora podem seguir pro banco e pra integração.

</details>

---

## Interação 7 — Estrutura do repositório e publicação com Git

**Data:** 12/11/2026

**Objetivo:** Revisar as pastas, os arquivos e os comandos de publicação do projeto.

**Prompt enviado à IA:**

````text
somos o grupo 14, o repositório é esse:

https://github.com/SN-2026-GRUPO-14-NASA/DONKI-IPS

já organizamos README, reflexão, painel e as pastas scripts, sql e docs. Confere se falta alguma pasta e se os comandos pra conectar no Git estão certos.
````

**Resumo da resposta:**

A IA listou a estrutura esperada, explicou pastas vazias e .github/workflows e apresentou comandos de inicialização, commit e push. Também comentou permissões, autenticação e ativação do Pages.

**O que funcionou:**

A resposta esclareceu o caminho do workflow e a diferença entre os arquivos da raiz e os documentos em docs.

**O que precisou ajuste:**

Os comandos foram apresentados para uma primeira publicação e dependem da situação do repositório local. O histórico não confirma nesta interação que todos tenham sido executados.

<details>
<summary>Resposta da IA</summary>

Confiram se ficou assim:

| Caminho | Finalidade |
| --- | --- |
| `README.md` | API, arquitetura, configuração, links e divisão de responsabilidades |
| `.gitignore` | Exclusão de `.env` e outros arquivos locais com credenciais |
| `index.html` | Painel publicado no GitHub Pages |
| `scripts/fetch_nasa.py` | Coleta e tratamento dos dados |
| `sql/setup.sql` | Estrutura do banco e permissões |
| `.github/workflows/update-data.yml` | Automação da coleta |
| `docs/ai-interaction.md` | Registro das interações |
| `docs/reflexao.md` | Reflexão do grupo |
| `docs/tutorial.pdf` | Tutorial de reprodução |
| `docs/apresentacao.pdf` | Apresentação |

O Git não versiona pastas vazias; um `.gitkeep` pode ser usado enquanto não houver arquivos nelas. Confiram principalmente a pasta `.github/workflows`, porque o workflow precisa estar nesse caminho para ser reconhecido.

Para a primeira publicação, caso o diretório ainda não seja um repositório:

```bash
cd ~/DONKI-IPS
git init -b main
git remote add origin https://github.com/SN-2026-GRUPO-14-NASA/DONKI-IPS.git
git add .
git commit -m "Estrutura inicial do repositório"
git push -u origin main
```

Pra fazer o push, a conta autenticada precisa ter permissão de escrita. Se houver recusa, confiram o acesso à organização. Na autenticação por HTTPS, a senha comum da conta não substitui um token. A integração do Claude com GitHub é uma possibilidade, mas não é necessária para vocês publicarem pelo terminal.

Depois, ativem Pages em Settings → Pages → branch `main`, pasta raiz.

</details>

---

## Interação 8 — Revisão do modelo SQL e das permissões

**Data:** 12/11/2026

**Objetivo:** Revisar ips_eventos, execucoes, chave única e regras de acesso.

**Prompt enviado à IA:**

````text
no SQL colocamos ips_eventos e execucoes. O activity_id vai ser UNIQUE, e instruments e linked_events ficam como listas de texto. Em execucoes vamos guardar status, registros, lotes e erros. Dá uma olhada se isso faz sentido e o que precisamos ajustar nas permissões.
````

**Resumo da resposta:**

A IA revisou activity_id com UNIQUE, listas text[], campos de revisão e status de execução. Orientou RLS nas duas tabelas, políticas de leitura e GRANTs para os papéis previstos.

**O que funcionou:**

A análise relacionou a chave natural ao upsert e separou a leitura pública das permissões necessárias à carga.

**O que precisou ajuste:**

A execução do SQL e a conferência do RLS no Supabase ainda eram passos a realizar. A revisão da resposta não foi apresentada como prova de execução no banco.

<details>
<summary>Resposta da IA</summary>

O modelo faz sentido. Na resposta da IPS, além dos campos iniciais, aparecem `submissionTime`, `versionId` e `sentNotifications`. Só deixem claro quais campos vêm da API e quais vocês vão guardar no banco.

Na `ips_eventos`, mantenham:

- `activity_id` com restrição UNIQUE;
- catálogo, local, horário e link;
- `instruments` e `linked_events` como `text[]`;
- `submission_time` e `version_id`;
- datas de coleta e atualização.

Na `execucoes`, o CHECK de status pode limitar os valores a `concluido`, `erro_parcial`, `erro_critico` e `em_andamento`.

Ativem RLS nas duas tabelas. As políticas públicas devem liberar somente leitura. Os GRANTs previstos são SELECT para `anon` e `authenticated` e as permissões necessárias para `service_role` executar a carga.

Deixem o script preparado pra rodar mais de uma vez, assim dá pra ajustar depois sem recriar o banco. Depois rodem no SQL Editor do Supabase. Conferir o SQL aqui não garante que ele vai executar sem erro no banco.

Após rodar, confiram as tabelas no Table Editor e o estado de RLS. Depois versionem o `setup.sql`.

</details>

---

## Interação 9 — Primeira carga, atualização incremental e testes

**Data:** 12/11/2026

**Objetivo:** Distinguir a carga histórica das atualizações seguintes e planejar testes de erro.

**Prompt enviado à IA:**

````text
o fetch_nasa.py já está separado em consulta, tratamento e envio pro Supabase, com upsert em lotes e sem repetir activity_id. A dúvida é a primeira carga: como diferenciar ela das atualizações seguintes? E quais erros precisamos testar?
````

**Resumo da resposta:**

A IA sugeriu histórico desde 2010, atualização dos últimos 60 dias, deduplicação, lotes de 500, logs e saída com erro em falhas. Inicialmente propôs janelas históricas de 180 dias e timeout de 15 minutos.

**O que funcionou:**

As orientações sobre atualização incremental, deduplicação e registro de falhas organizaram a validação do pipeline.

**O que precisou ajuste:**

A janela de 180 dias estava incorreta e causou falha na execução seguinte. O timeout também foi ampliado para 30 minutos na discussão posterior sobre enriquecimento.

<details>
<summary>Resposta da IA</summary>

Essa separação está boa. Na primeira carga, busquem o histórico desde 2010. Depois que houver dados, a rotina pode consultar apenas os últimos 60 dias. A execução manual deve aceitar datas de início e fim.

Minha sugestão inicial é dividir o histórico em janelas de 180 dias, o que daria cerca de 35 consultas. Mas confiram na primeira execução se o endpoint aceita esse intervalo.

Antes do upsert, deixem apenas uma versão por `activity_id`, priorizando a mais recente. Isso evita que o mesmo lote tente atualizar duas vezes a mesma linha, situação associada ao erro 21000.

Usem lotes de 500 registros. Registrem quantidade recebida, processada, lotes, falhas e status. Uma resposta vazia deve terminar como `concluido`, com zero registros. Falhas parciais ou críticas precisam produzir o status correspondente e `sys.exit(1)`, para o Actions sinalizar o problema.

Nos testes simulados, incluam duplicatas, resposta vazia, evento sem data e falha de lote. Mesmo quando esses testes passam, ainda falta verificar a integração real com NASA e Supabase.

No workflow, mantenham execução diária às 06h de Brasília, disparo manual, `permissions: contents: read`, controle de concorrência e timeout inicial de 15 minutos. Confiram os três Secrets antes da primeira execução.

</details>

---

## Interação 10 — Correção das janelas de consulta da IPS

**Data:** 12/11/2026

**Objetivo:** Corrigir a execução parcial que gravou nove eventos com janelas de 180 dias.

**Prompt enviado à IA:**

````text
rodamos no Actions. Entraram 9 eventos, mas terminou com erro parcial. Pelo log parece ser a janela de 180 dias. Tem que diminuir esse intervalo?
````

**Resumo da resposta:**

A IA reconheceu o erro e orientou intervalos com até 60 datas inclusivas, equivalentes a no máximo 59 dias de diferença entre início e fim. Recomendou repetir a carga com data_inicio = 2010-01-01.

**O que funcionou:**

A interação identificou a causa da falha e distinguiu registros já gravados de uma carga histórica completa. Na interação seguinte o grupo informou que a nova execução deu certo.

**O que precisou ajuste:**

Foi necessário reduzir as janelas e informar o início histórico explicitamente, pois a presença de registros no banco poderia acionar a rotina incremental.

<details>
<summary>Resposta da IA</summary>

Sim, a sugestão de 180 dias que eu dei estava errada: o endpoint aceita consultas de até 60 dias. Corrijam a divisão para que cada janela tenha, no máximo, 59 dias de diferença entre as datas, cobrindo até 60 datas no intervalo inclusivo.

Nesse histórico, serão cerca de 103 janelas, em vez de 35. A conexão, o upsert e o registro de execução funcionaram, como mostram os 9 eventos gravados. O `erro_parcial` e o workflow vermelho mostram que o tratamento de erro funcionou.

Depois de publicar a correção, iniciem a execução manual com `data_inicio = 2010-01-01`. Isso é necessário porque o banco já tem registros: sem a data explícita, o script entraria na rotina incremental dos últimos 60 dias.

Anotem esse erro na reflexão também: a sugestão da IA precisou ser corrigida depois do teste com a API real.

</details>

---

## Interação 11 — Conferência da carga após o workflow verde

**Data:** 12/11/2026

**Objetivo:** Definir como verificar o período e a persistência dos dados após corrigir as janelas.

**Prompt enviado à IA:**

````text
agora deu certo. Ajustamos as janelas e rodamos de novo. Além do workflow verde, o que precisamos conferir no banco pra saber se carregou tudo?
````

**Resumo da resposta:**

A IA recomendou comparar o log final do Actions, a linha correspondente em execucoes e os registros de ips_eventos. Também orientou guardar evidências do workflow, da tabela e da consulta REST.

**O que funcionou:**

O grupo relatou sucesso após ajustar as janelas. A resposta mostrou que o ícone verde precisa ser analisado junto ao período efetivamente consultado.

**O que precisou ajuste:**

A cobertura desde 2010 não foi comprovada apenas pelo workflow verde. O histórico orienta conferir as datas e distinguir carga histórica de atualização incremental.

<details>
<summary>Resposta da IA</summary>

Confiram três coisas: o final do log no Actions, a linha em `execucoes` e os dados em `ips_eventos`. Vejam se o período carregado é o que vocês pediram.

Também verifiquem se a execução foi histórica ou incremental. O workflow verde, sozinho, não diz se carregou todo o histórico desde 2010. Como a primeira tentativa gravou alguns registros, a data de início explícita continua sendo relevante.

Pra documentação, guardem o workflow concluído, uma visão da tabela de eventos e uma consulta JSON pela API REST do Supabase. Isso mostra a coleta rodando, os dados salvos e a consulta funcionando.

</details>

---

## Interação 12 — Organização do painel e requisitos de consulta

**Data:** 12/11/2026

**Objetivo:** Revisar filtros, cartões, gráfico, tabela, busca e última atualização.

**Prompt enviado à IA:**

````text
no painel pensamos em cabeçalho, filtros por local e ano, cards, gráfico e tabela. Também queremos busca por instrumento ou evento ligado e a última atualização. Essa ordem fica boa? Falta algum requisito?
````

**Resumo da resposta:**

A IA propôs consulta REST no index.html, última execução lida de execucoes, filtros e busca. Orientou paginação além de 1.000 linhas, tratamento de indisponibilidade, escape de HTML e validação de links HTTPS.

**O que funcionou:**

A resposta ajudou a relacionar a organização visual com a consulta ao banco e com os requisitos de segurança.

**O que precisou ajuste:**

A paginação e a apresentação em celular precisaram de verificações posteriores. Nesta etapa a resposta apresenta propostas, sem comprovar que toda a interface já estivesse validada.

<details>
<summary>Resposta da IA</summary>

Essa organização funciona. Um único `index.html`, sem etapa de build, pode consultar a API REST do Supabase.

A faixa de atualização deve usar a tabela `execucoes`, mostrando horário e status da última execução. Os filtros de local podem ser preenchidos com os valores existentes no banco. A busca por instrumento ou evento relacionado complementa os filtros de ano e local.

Nos cartões, vocês podem apresentar total de choques, choques associados ao local Earth, data do último evento e percentual com CME vinculada.

O gráfico de barras pode mostrar eventos por ano, separados por local. Quando um ano estiver selecionado, pode passar a mostrar os meses. Depois vejam se a distribuição dos eventos permite discutir o ciclo solar.

Na tabela, mantenham data, local, catálogo, instrumentos, eventos relacionados e link para o DONKI. A exibição pode começar com 50 registros e oferecer “mostrar mais”.

Prevejam paginação na consulta ao Supabase para ultrapassar 1.000 linhas, tratamento de indisponibilidade, tema claro e escuro e escape dos valores exibidos em HTML. Validem os links para aceitar apenas HTTPS.

No front-end, usem a URL do projeto e a publishable key. A segurança da leitura pública depende também das políticas de RLS e das permissões configuradas.

</details>

---

## Interação 13 — Explicação científica e limites dos dados IPS

**Data:** 12/11/2026

**Objetivo:** Esclarecer o fenômeno, os instrumentos e o que os registros da IPS realmente informam.

**Prompt enviado à IA:**

````text
no texto explicamos o choque como uma frente no vento solar, geralmente ligada a uma CME. Mas ficou confuso o que a IPS mostra de fato. Pode explicar melhor os campos e os instrumentos pra gente ajustar essa parte?
````

**Resumo da resposta:**

A IA explicou choques no vento solar, campos do JSON e instrumentos de plasma e campo magnético. Diferenciou registros de ocorrência das medições físicas e reviu o nome de um catálogo.

**O que funcionou:**

A distinção entre ocorrência do choque e parâmetros físicos ajudou a delimitar o que poderia ser mostrado usando apenas IPS.

**O que precisou ajuste:**

A IA corrigiu a indicação anterior de SWRC_CATALOG para M2M_CATALOG. Velocidade, densidade e intensidade do campo não deveriam ser atribuídas diretamente aos registros IPS discutidos.

<details>
<summary>Resposta da IA</summary>

Vocês podem explicar que o Sol emite continuamente vento solar. Quando um fluxo mais rápido alcança outro mais lento, pode formar uma frente de choque, com mudanças abruptas de velocidade, densidade, temperatura e campo magnético. Dá pra comparar com o estrondo sônico de um avião pra explicar na apresentação.

Entre os fenômenos relacionados estão as CMEs, ejeções de plasma que podem impulsionar choques, e as correntes de vento rápido, ou HSS. A detecção ocorre quando a frente passa pela região observada pelos instrumentos.

Na prática, cada registro traz:

| Campo | Leitura para o trabalho |
| --- | --- |
| `activityID` | Identificador usado como chave natural |
| `eventTime` | Horário do evento em UTC |
| `location` | Local ou missão de detecção, como Earth, STEREO A, STEREO B e MESSENGER |
| `instruments` | Instrumentos associados à observação |
| `linkedEvents` | Eventos relacionados, identificados por tipos como CME, HSS, GST, SEP e MPC |
| `catalog` | Catálogo de origem do registro |
| `sentNotifications` | Notificações associadas |
| `link` | Página do evento no DONKI |
| `submissionTime` e `versionId` | Informações de submissão e revisão |

Um exemplo da consulta é o evento `2024-05-02T07:46:00-IPS-001`, com `eventTime` em 02/05/2024 às 07:46 UTC, local Earth, instrumentos DSCOVR: PLASMAG, ACE: MAG e ACE: SWEPAM e uma GST relacionada. O link do registro era:

https://ccmc.gsfc.nasa.gov/DONKI/view/IPS/30386/-1

Para os instrumentos, basta explicar que MAG mede campo magnético e que instrumentos como SWEPAM, PLASMAG e PLASTIC estão associados a medições de plasma. As observações ligadas a Earth incluem sondas como ACE e DSCOVR na região de L1, aproximadamente 1,5 milhão de quilômetros da Terra na direção do Sol.

Uma correção à indicação inicial: nos dados consultados aparece `M2M_CATALOG`, em vez do `SWRC_CATALOG` mencionado anteriormente.

O ponto principal pra ajustar no texto é que esses registros da IPS não trazem a velocidade do choque, a densidade ou a intensidade do campo magnético. Ela informa a ocorrência, o momento, o local, os instrumentos e os vínculos. Por isso, com IPS isoladamente, o painel trabalha principalmente com contagens, distribuição temporal e relações entre eventos.

O ciclo solar de aproximadamente 11 anos, com os períodos de maior atividade discutidos em torno de 2014 e 2024–2025, pode contextualizar a distribuição. A cadeia CME, choque e tempestade geomagnética também serve para explicar o interesse científico do projeto.

</details>

---

## Interação 14 — Mapa 3D e fontes complementares

**Data:** 12/11/2026

**Objetivo:** Avaliar posições das sondas e dados físicos para complementar a IPS.

**Prompt enviado à IA:**

````text
pensamos em colocar um mapa 3D do Sistema Solar mostrando onde os choques foram detectados. Dá pra conseguir a posição das sondas na data do evento? E tem como buscar dados físicos pra complementar a IPS?
````

**Resumo da resposta:**

A IA apresentou Three.js, posições aproximadas e efemérides do Horizons. Comparou CME, GST, Horizons, OMNI/CDAWeb e Helsinki e sugeriu priorizar o painel obrigatório antes das integrações extras.

**O que funcionou:**

A resposta separou posições aproximadas de efemérides e relacionou cada fonte ao tipo de informação complementar.

**O que precisou ajuste:**

As aproximações precisariam ser identificadas no painel. OMNI e Helsinki foram discutidos como possibilidades, sem confirmação de incorporação ao projeto.

<details>
<summary>Resposta da IA</summary>

Dá pra usar Three.js no mapa pra mostrar o Sol, órbitas e os locais de detecção. Ao selecionar um evento, a cena pode destacar a posição da nave e apresentar uma animação ilustrativa da propagação.

Pra conseguir as posições, há duas opções: aproximações calculadas no navegador, usando movimentos orbitais simplificados, ou consulta ao JPL Horizons no pipeline. O primeiro exige menos integração e precisa ser identificado como aproximado. O segundo fornece efemérides para o instante do evento e exige novos campos no banco.

Pra acrescentar os dados físicos:

| Fonte | Informação complementar | Trabalho envolvido |
| --- | --- | --- |
| DONKI/CME | Velocidade, direção e largura angular da CME | Associação pelos IDs em `linkedEvents` |
| DONKI/GST | Índice Kp da tempestade relacionada | Associação aos registros de GST |
| JPL Horizons | Posição da nave e da Terra | Consulta de efemérides |
| OMNIWeb / CDAWeb, NASA SPDF | Séries de velocidade, densidade e campo magnético do vento solar | Processamento temporal adicional |
| Banco de choques de Helsinki, ipshocks.fi | Parâmetros do choque, como compressão e número de Mach | Associação por horário e outra fonte de dados |

DONKI/CME e DONKI/GST aproveitam a organização de eventos da mesma base. Elas permitem relacionar uma CME, sua detecção como choque e a tempestade associada, além de construir o gráfico de velocidade da CME versus Kp.

Por causa do prazo, façam primeiro o painel obrigatório, depois o enriquecimento e, por último, o mapa 3D. OMNI e Helsinki exigem uma integração maior e podem ficar como possibilidades futuras.

</details>

---

## Interação 15 — Discussão do escopo das APIs complementares

**Data:** 12/11/2026

**Objetivo:** Esclarecer a dúvida sobre usar CME e GST como complementos de IPS.

**Prompt enviado à IA:**

````text
uma dúvida: pelo documento da atividade podemos usar essas outras APIs como complemento? A principal continua sendo IPS, mas CME e GST são de outros grupos.
````

**Resumo da resposta:**

A IA afirmou que o enunciado consultado não era explícito sobre fontes adicionais e recomendou confirmar o escopo. Diferenciou ler linkedEvents de consultar novas APIs e comentou a reserva do grupo 14.

**O que funcionou:**

A resposta manteve a IPS como fonte principal e distinguiu vínculos existentes nos dados de novas consultas.

**O que precisou ajuste:**

A resposta apresentou uma recomendação de confirmação, sem estabelecer uma proibição nem registrar uma autorização recebida. Nas interações seguintes o grupo decidiu prosseguir com CME, GST e Horizons.

<details>
<summary>Resposta da IA</summary>

O enunciado não diz claramente se pode ou não usar outra API como complemento. Ele foi organizado com uma API principal pra cada grupo.

A DONKI/CME aparece vinculada ao grupo 03 e a DONKI/GST ao grupo 04. Vale confirmar com o professor, explicando que CME e GST seriam só complementos e que o foco continua na IPS.

Contar vínculos de CME e GST que já vêm em `linkedEvents` não exige consultar outra API. Calcular posições aproximadas no navegador também não acrescenta uma fonte externa.

Já obter velocidades pela CME, Kp pela GST ou posições pelo Horizons envolve consultas adicionais. O mesmo vale para OMNI.

Outro ponto de organização é conferir a reserva do grupo 14 e da IPS na planilha, pois as tabelas do documento consultado vão até o grupo 13. Confiram isso pra reserva bater com o projeto de vocês.

</details>

---

## Interação 16 — Impacto do enriquecimento no desempenho

**Data:** 12/11/2026

**Objetivo:** Entender onde ficaria o custo das consultas complementares.

**Prompt enviado à IA:**

````text
no nosso fluxo o Actions busca tudo e salva no Supabase, o site só lê o banco. Se colocarmos CME, GST e Horizons, isso pode deixar o site lento ou demora mais só na coleta?
````

**Resumo da resposta:**

A IA explicou que o Actions realiza a coleta e salva no banco, enquanto o painel lê os dados persistidos. Apresentou estimativas de tempo e requisições e comentou o custo gráfico do mapa 3D.

**O que funcionou:**

A explicação esclareceu a separação entre tempo de coleta e tempo de acesso ao painel.

**O que precisou ajuste:**

Os tempos e a quantidade de requisições eram estimativas. Não devem ser tratados como medições, e a renderização 3D ainda precisava ser avaliada em celular.

<details>
<summary>Resposta da IA</summary>

Isso, a demora maior fica na coleta. Quando alguém abre o painel, esses dados já estão salvos no Supabase.

O impacto principal será o tempo da carga e o número de requisições às fontes. A estimativa inicial era de cerca de dois minutos para a coleta simples e cinco a seis minutos para o enriquecimento, sujeitas à resposta dos serviços e à quantidade de dados. A conta de aproximadamente 300 requisições pro histórico também é uma estimativa.

No navegador, o aumento decorre das colunas adicionais, do volume total carregado e da renderização. Consultar a NASA a cada visita acrescentaria dependência e exporia a chave no front-end; manter a coleta no Actions evita essa situação.

O mapa 3D acrescenta biblioteca e processamento gráfico. O carregamento sob demanda do Three.js e a avaliação em celular ajudam a controlar esse custo. Na apresentação, vocês podem explicar que o banco separa a coleta da visualização.

</details>

---

## Interação 17 — Vínculos CME/GST/Horizons e tratamento de falhas

**Data:** 12/11/2026

**Objetivo:** Revisar o enriquecimento já escolhido e o comportamento diante de uma fonte indisponível.

**Prompt enviado à IA:**

````text
ok, vamos usar JPL Horizons, DONKI/CME e DONKI/GST. Já separamos essas consultas pra depois da coleta dos choques e estamos ajustando as colunas no SQL. Confere os vínculos e o que fazer se uma dessas APIs falhar.
````

**Resumo da resposta:**

A IA orientou vínculos por linkedEvents, seleção da CME mais rápida quando houvesse várias, Kp máximo, posições do Horizons e tratamento separado das etapas. Sugeriu SQL reaplicável, testes, timeout de 30 minutos e nova carga histórica.

**O que funcionou:**

A análise explicitou critérios de associação e a necessidade de registrar falhas sem confundir a indisponibilidade de uma fonte com a perda de todas as outras informações.

**O que precisou ajuste:**

A IA informou que não conseguiu abrir todas as consultas e documentações. Era necessário conferir respostas reais; posteriormente foi identificado um campo incorreto na leitura da GST.

<details>
<summary>Resposta da IA</summary>

Essa sequência está certa. Esses campos acrescentam 14 colunas à `ips_eventos`. Façam essa alteração no SQL de um jeito que permita rodar de novo sem apagar o que já está no banco.

Na CME, usem os identificadores presentes em `linkedEvents` para limitar as consultas às datas necessárias. Os dados previstos são velocidade, direção, largura e tipo. Se uma CME tiver várias análises, definam qual delas usar. Quando houver mais de uma CME relacionada, a regra dessa versão é pegar a mais rápida. Deixem isso explicado como um critério do projeto.

Na GST, obtenham o Kp máximo do evento relacionado.

No Horizons, guardem as posições 3D, em unidades astronômicas, para a nave e para a Terra no instante da detecção. Para o local Earth, o cálculo prevê deslocar a posição até a região de L1.

Separem as etapas para uma indisponibilidade do Horizons não impedir a gravação das informações de CME e GST. O problema precisa aparecer no log e no status da execução.

Nos testes simulados, incluam uma CME com várias análises, indisponibilidade do Horizons e resposta em formato inesperado. Não consegui abrir diretamente todas as consultas e a documentação dessas fontes aqui. Então é preciso conferir o formato real das respostas quando rodarem a carga.

Com o enriquecimento, aumentem o timeout para 30 minutos, e a estimativa da carga histórica completa passa a aproximadamente dez minutos. Rodem novamente o SQL, publiquem os ajustes e executem com `data_inicio = 2010-01-01`. Confiram no log quantos choques receberam dados de CME, Kp e posição 3D.

</details>

---

## Interação 18 — Composição do painel 3D

**Data:** 12/11/2026

**Objetivo:** Revisar a disposição do mapa, dos gráficos e da tabela.

**Prompt enviado à IA:**

````text
pro front pensamos em algo parecido com o Apoastro que fizemos, só que 3D. O mapa ficaria em cima e os gráficos e a tabela embaixo. O que acha dessa organização?
````

**Resumo da resposta:**

A IA propôs uma cena 3D, linha do tempo, detalhe do evento e seções de atualização, filtros, gráficos e tabela. Comentou seleção vinculada, rotação, zoom e uso de Kp nos marcadores.

**O que funcionou:**

A resposta ofereceu uma organização coerente com a proposta de mapa acima das demais consultas.

**O que precisou ajuste:**

O projeto Apoastro citado pelo grupo não estava disponível para comparação. Também era necessário verificar o preenchimento do Horizons e identificar o uso de posições aproximadas.

<details>
<summary>Resposta da IA</summary>

Acho que essa divisão funciona. A cena pode destacar o Sol, as órbitas e os eventos, enquanto as seções abaixo oferecem consulta mais objetiva.

Dá pra organizar assim:

1. Cena 3D com fundo escuro, Sol em destaque, órbitas finas e pontos coloridos por local de detecção.
2. Linha do tempo com controle deslizante de 2010 a 2026 e botão de reprodução.
3. Detalhe do evento selecionado, com data, local, instrumentos e cadeia CME → choque → tempestade.
4. Faixa de atualização, filtros, gráficos e tabela.

O tamanho do marcador pode representar Kp quando esse dado estiver disponível. A câmera pode permitir rotação e zoom, e a seleção na tabela deve localizar o evento na cena.

A animação pode utilizar a direção da CME para ilustrar o percurso a partir do Sol. O link para o DONKI deve continuar acessível no detalhe.

Não encontrei o Apoastro aqui. Pra comparar o visual, precisaria da pasta ou do link. Por enquanto dá pra seguir com essa ideia que vocês descreveram. Também é necessário confirmar se as posições do Horizons foram preenchidas; se não foram, o painel deve informar quando usar aproximações.

</details>

---

## Interação 19 — Paginação, segurança e adaptação ao celular

**Data:** 12/11/2026

**Objetivo:** Conferir a consulta ao Supabase, o volume de registros e o uso em telas menores.

**Prompt enviado à IA:**

````text
esquece o Apoastro, vamos pensar no painel sozinho. A URL é https://xxbwvcqpdvdrqmwyfoww.supabase.co e já separamos a publishable key pro front. Quer que eu pegue um SELECT do banco? Precisamos conferir principalmente a paginação e como fica no celular.
````

**Resumo da resposta:**

A IA relatou bloqueio de acesso ao Supabase e testes com dados simulados, inclusive acima de 1.000 registros. Listou elementos do mapa e dos filtros, testes de conteúdo externo e problemas de layout em celular.

**O que funcionou:**

Os testes relatados ajudaram a examinar paginação e interface, incluindo a identificação de rolagem horizontal e sobreposições.

**O que precisou ajuste:**

Os problemas de espaço e sobreposição precisavam ser corrigidos. Dados simulados não confirmavam a carga real nem o enriquecimento; essa conferência continuava pendente nesta interação.

<details>
<summary>Resposta da IA</summary>

A URL e uma chave pública configurada com leitura permitem consultar a API REST, desde que as políticas e permissões estejam corretas. A chave secreta continua restrita ao pipeline.

O acesso direto ao Supabase ficou bloqueado aqui. Pra conferir a interface, usei dados simulados com o mesmo formato da tabela. Foram usados conjuntos acima de 1.000 registros, incluindo testes com cerca de 1.300 e 1.642 eventos. Naquele momento, o banco tinha só 18 eventos e ainda estava sem o enriquecimento completo.

No `index.html`, confiram:

- Cena com Sol, órbitas de Mercúrio a Marte e eventos posicionados conforme os dados disponíveis.
- Cor por local e losango para MESSENGER.
- Tamanho do ponto associado ao Kp, quando existente.
- Seleção abrindo a cadeia do evento, escala G1 a G5 e direção da CME.
- Reprodução temporal e interrupção da rotação automática ao interagir com a cena.
- Filtros por local, ano, Kp e busca aplicados ao mapa e às demais seções.
- Gráficos de contagem temporal e de velocidade da CME versus Kp.
- Tabela vinculada à seleção no mapa e paginação além de 1.000 linhas.

Nos testes de celular, apareceram rolagem horizontal, nomes dos planetas sobrepostos ao detalhe e pouco espaço entre o detalhe e a linha do tempo. Esses são os ajustes prioritários de layout.

Confiram também o escape de conteúdo vindo da API. No teste com uma tag maliciosa, ela precisa aparecer como texto, sem executar. O painel deve aceitar somente a chave pública.

Quando não houver posição do Horizons, o cálculo aproximado pode manter a visualização, desde que o detalhe do evento informe essa condição.

Depois dos ajustes, publiquem no Pages e façam a carga histórica com enriquecimento. Esses testes ajudam a conferir a tela e a paginação. Depois ainda precisa ver se a carga real preencheu os campos.

</details>

---

## Interação 20 — Tempo de viagem e velocidade média estimada

**Data:** 12/11/2026

**Objetivo:** Revisar o cálculo entre a saída da CME e a detecção do choque e sua apresentação.

**Prompt enviado à IA:**

````text
ficou bom. Queremos acrescentar o tempo entre a saída da CME e a detecção do choque, e calcular uma velocidade média com a distância do Horizons. Dá pra comparar com a velocidade inicial? Confere a conta e como mostrar isso no painel.
````

**Resumo da resposta:**

A IA explicou distância dividida pelo tempo, apresentou o exemplo de 0,99 UA em 76,8 horas e propôs campos, gráficos e indicadores. Descreveu tratamento de startTime ausente e descarte de intervalos fora de 12 horas a sete dias.

**O que funcionou:**

A resposta organizou o cálculo com conversão de unidades e relacionou os novos campos às visualizações propostas.

**O que precisou ajuste:**

O tempo e a velocidade eram estimativas dependentes das associações e dos critérios adotados. Padrões produzidos pelo simulador não deveriam ser apresentados como resultados científicos reais.

<details>
<summary>Resposta da IA</summary>

Dá pra fazer com mais três campos: horário de saída da CME, tempo até a detecção na nave e velocidade média estimada no trajeto.

A conta é distância dividida pelo tempo, convertendo as unidades. Por exemplo, 0,99 UA em 76,8 horas dá aproximadamente 536 km/s.

Prevejam o caso em que a CME não tenha `startTime`: dá pra tentar tirar o horário do identificador. Nessa versão, intervalos menores que 12 horas ou maiores que sete dias são descartados como associações suspeitas. Deixem esse critério explicado na documentação.

No painel, a análise pode aparecer em:

- gráfico “A CME freou ou acelerou?”, comparando velocidade inicial e média;
- indicador da mediana do tempo de viagem, em horas e dias;
- etapa adicional na cadeia do evento;
- coluna “Viagem” na tabela.

A linha de igualdade do gráfico ajuda a comparar os dois valores. A ideia é relacionar isso com o arrasto pelo vento solar: CMEs rápidas tendem a perder velocidade e as lentas podem ganhar, aproximando-se das condições do meio.

O padrão dos dados simulados foi produzido pelo simulador. Ele não deve ser apresentado como resultado científico. Pra discutir o resultado no trabalho, usem os dados reais.

Reapliquem o SQL com as três novas colunas, publiquem o script e executem novamente o histórico desde 2010 para preencher os campos.

</details>

---

## Interação 21 — Correção do campo Kp na GST

**Data:** 12/11/2026

**Objetivo:** Investigar por que o Kp não aparecia no gráfico nem no banco após a carga real.

**Prompt enviado à IA:**

````text
rodamos os dados reais, mas o gráfico de Kp está vazio. Achamos que era o clique, só que os valores também não aparecem no banco. Pode conferir se estamos lendo o campo certo da GST?
````

**Resumo da resposta:**

A IA identificou a leitura de allKpValues no lugar de allKpIndex, reconheceu o erro e relatou um teste com resposta real que retornou Kp 7,0. Recomendou contadores de enriquecimento e nova carga histórica.

**O que funcionou:**

O diagnóstico explicou como a execução podia terminar sem erro técnico e ainda deixar o Kp ausente. A interação seguinte começa com o grupo informando que tudo estava funcionando.

**O que precisou ajuste:**

Foi necessário corrigir o nome do campo e reprocessar o histórico. O teste simulado havia repetido o campo incorreto, mostrando a necessidade de comparar com o JSON real.

<details>
<summary>Resposta da IA</summary>

Achei o problema: é o nome do campo. A GST usa `allKpIndex`, mas o script estava lendo `allKpValues`.

Com isso, o pipeline encontrava as tempestades, porém interpretava o Kp como ausente. A execução terminava sem acusar erro técnico, mesmo deixando o enriquecimento incompleto.

Eu tinha indicado o nome errado. Corrijam isso no `fetch_nasa.py`. Com essa correção, o teste usando um exemplo da resposta real retornou Kp 7,0.

A carga já tinha 1.413 choques desde 2010, com posições do Horizons e velocidades de CME preenchidas. Por isso não basta olhar só se o log terminou sem erro: o Kp estava ficando vazio.

Acrescentem um resumo como:

`encontradas: X CME(s) (Y com velocidade) | Z tempestade(s) (W com Kp)`

Depois, rodem novamente com `data_inicio = 2010-01-01` para atualizar os registros históricos. A expectativa é que o gráfico de velocidade da CME versus intensidade da tempestade receba pontos e que a tabela exiba Kp e a escala G.

Esse erro também vale entrar na reflexão: o teste simulado repetiu o mesmo nome incorreto de campo. Só a comparação com a resposta real mostrou o problema.

No gráfico de viagem com dados reais, as CMEs rápidas, acima de aproximadamente 1.000 km/s, ficaram concentradas abaixo da linha de igualdade. Na apresentação, expliquem que essa leitura depende dos registros carregados e dos critérios que vocês usaram.

</details>

---

## Interação 22 — Melhorias usando os dados já existentes

**Data:** 12/11/2026

**Objetivo:** Selecionar funcionalidades adicionais úteis à análise e à demonstração, sem novas fontes.

**Prompt enviado à IA:**

````text
agora tudo funcionando. Alguma ideia a mais usando os dados que já temos? Pensamos em ligar as detecções da mesma CME em naves diferentes e facilitar a demonstração, mas sem complicar muito por causa do prazo.
````

**Resumo da resposta:**

A IA propôs ligações da mesma CME entre naves, tour das maiores tempestades, histórico do pipeline, link direto e CSV. Citou ENLIL e OMNI como expansões que exigiriam trabalho adicional.

**O que funcionou:**

O grupo escolheu na interação seguinte as cinco propostas que aproveitavam os dados existentes.

**O que precisou ajuste:**

ENLIL e OMNI ficaram como possibilidades futuras. A IA também lembrou que a documentação e as evidências ainda precisavam ser finalizadas naquele ponto da conversa.

<details>
<summary>Resposta da IA</summary>

Dá pra acrescentar algumas coisas sem buscar dados novos:

| Funcionalidade | Utilidade |
| --- | --- |
| Mesma CME em várias naves | Relacionar detecções que compartilham a mesma CME |
| Tour “Maiores tempestades” | Percorrer os cinco eventos de maior Kp na demonstração |
| Histórico do pipeline | Exibir status, duração e registros das últimas execuções |
| Link direto para evento | Abrir o painel com um choque selecionado |
| Exportação CSV | Permitir análise externa dos eventos filtrados |

Um exemplo nos dados é a CME de 08/10/2026 às 16:24, associada a detecções em Earth e STEREO A. A ligação visual ajuda a explorar esse compartilhamento.

O tour pode apoiar a demonstração de aproximadamente oito minutos. O histórico do pipeline ajuda a explicar a arquitetura e os logs. Links diretos também podem ser usados nos slides.

Se quiserem ir além, dá pra comparar previsão e chegada real com ENLIL e acrescentar medidas de vento solar pelo OMNI. Com ENLIL, dá pra comparar a previsão com a chegada real. OMNI exige tratar séries de velocidade, densidade e campo magnético. Os dois dão mais trabalho.

Como ainda faltam tutorial, reflexão, apresentação, README, prints e planilha, eu ficaria com as melhorias que usam os dados já carregados.

</details>

---

## Interação 23 — Validação das cinco melhorias e do CSV

**Data:** 12/11/2026

**Objetivo:** Revisar as funções escolhidas e reduzir a confusão visual das ligações no mapa.

**Prompt enviado à IA:**

````text
vamos ficar com essas cinco que usam os dados atuais. Já dividimos os ajustes. Nas ligações do mapa, vamos mostrar só as do evento selecionado, porque tudo junto ficou confuso. O que precisamos conferir nessas funções e no CSV?
````

**Resumo da resposta:**

A IA detalhou ligações do evento selecionado, tour, últimas dez execuções, fragmento de URL e CSV com os filtros ativos. Orientou proteção contra fórmulas em planilhas e testes de navegação e celular.

**O que funcionou:**

A decisão de destacar apenas as ligações do evento selecionado respondeu ao problema visual relatado pelo grupo.

**O que precisou ajuste:**

A visualização de todas as ligações deveria iniciar desligada. As orientações de proteção do CSV e os testes precisavam ser conferidos; esta mensagem não apresenta confirmação de cada teste.

<details>
<summary>Resposta da IA</summary>

Sim, mostrar só as ligações do evento selecionado deixa o mapa mais fácil de entender. A opção de exibir todas as ligações pode continuar disponível, desligada por padrão.

Confiram o seguinte:

1. **Mesma CME em várias naves:** uma linha dourada liga os locais relacionados à CME do choque selecionado. O detalhe apresenta “A mesma CME também atingiu:”, com itens clicáveis.
2. **Maiores tempestades:** o tour percorre os cinco choques de maior Kp, com cerca de sete segundos por evento, e para quando o usuário interage com o mapa.
3. **Histórico do pipeline:** a tabela mostra as últimas dez execuções, incluindo duração, período, registros, lotes, erros e status.
4. **Link direto:** selecionar um choque atualiza o fragmento da URL, como `#2015-07-02T03:17:00-IPS-001`. O botão de cópia permite reutilizar o endereço nos slides.
5. **CSV:** a exportação usa os filtros ativos e inclui as 21 colunas previstas. Protejam a abertura em planilhas contra valores interpretados como fórmulas, como os que começam com `=` ou `+`.

Nos testes simulados, incluam CMEs associadas a mais de uma nave para exercitar as ligações. Confiram a navegação automatizada e a visualização em celular.

Podem manter no histórico a primeira execução, com os 34 erros das janelas de 180 dias. Ela ajuda a mostrar o tratamento de falhas e a correção feita durante o desenvolvimento.

Após publicar as melhorias, ainda é necessário finalizar os documentos, as evidências e a planilha. ENLIL e OMNI continuam como possibilidades de expansão, sem integrar estas cinco funcionalidades.

</details>

---

## Interação 24 — Nome CoronaFlux e identidade visual

**Data:** 12/11/2026

**Objetivo:** Revisar o termo ligado à coroa solar e definir nome, logo e cores.

**Prompt enviado à IA:**

````text
vamos mudar as cores pra dourado, laranja, amarelo e azul. Também pensamos numa logo com o Sol e linhas de campo e num nome ligado à coroa solar e ao fluxo magnético. Escrevemos coronária no rascunho, mas acho que o termo não é esse. Pode conferir e sugerir um nome?
````

**Resumo da resposta:**

A IA corrigiu coronária para coronal, sugeriu CoronaFlux e descreveu uma logo com o Sol e linhas de campo. Distribuiu dourado, laranja e azul nos elementos e comentou contraste, marcadores e celular.

**O que funcionou:**

A resposta reuniu a identidade em torno de CoronaFlux, mantendo DONKI-IPS como identificação do repositório.

**O que precisou ajuste:**

O termo coronária precisava ser substituído por coronal. O amarelo muito claro foi revisto e foram sugeridos ajustes de contraste e legenda no celular; o histórico termina sem apresentar uma nova validação visual.

<details>
<summary>Resposta da IA</summary>

Nesse caso, o termo certo é “coronal”, relacionado à corona, a coroa do Sol. “Coronária” remete às artérias do coração.

Uma sugestão é **CoronaFlux**, juntando corona e fluxo, pelo campo magnético e pelo vento solar. Usem esse nome no painel e mantenham DONKI-IPS no repositório, como pede a atividade.

Pra logo, dá pra combinar o Sol e laços de campo magnético de dipolo. Os laços devem sair de uma região polar e retornar à outra, com formas aninhadas, evitando a aparência de um laço de fita. O arquivo `assets/logo.svg` também pode servir de base para o ícone da aba e para o README. Confiram a legibilidade em tamanho pequeno, inclusive em 16 px.

As cores podem ficar assim:

| Elemento | Cor ou tratamento |
| --- | --- |
| Fundo | Azul-marinho |
| “Corona” | Degradê amarelo para laranja |
| “Flux” | Azul |
| Títulos, indicadores e linha do tempo | Dourado |
| Linha sob o cabeçalho | Transição dourado, laranja e azul |
| Links | Azul |
| Earth | Azul |
| STEREO A | Laranja |
| STEREO B | Dourado mais escuro |
| MESSENGER | Cinza, com marcador em losango |

O amarelo puro ficou claro demais ao lado das outras cores. O dourado mais escuro para STEREO B melhora a diferenciação. Considerem também a leitura com alterações de percepção de cor, usando a forma do marcador como informação adicional.

No celular, quando o detalhe do choque estiver aberto, a legenda pode ser escondida para evitar sobreposição. Confiram a composição no computador e no celular após aplicar a identidade.

Assim o painel fica com a marca CoronaFlux e continua identificado como DONKI-IPS. Pra fechar a entrega, ainda faltam tutorial, reflexão, slides, prints, README com a divisão de responsabilidades e a planilha.

</details>

---

## Resumo final

**Total de interações:** 24.

**Principais contribuições da IA:**

- Comparação das APIs e revisão dos campos e limites dos registros IPS.
- Revisão da sequência de trabalho, da estrutura do repositório, do SQL, das permissões e do workflow.
- Orientação sobre autenticação, carga histórica, atualização incremental, deduplicação e logs.
- Discussão do painel, do mapa 3D, dos filtros e do enriquecimento por CME, GST e Horizons.
- Diagnóstico das falhas, sugestões de funcionalidades e definição do nome e da identidade visual CoronaFlux.

**Principais limitações encontradas:**

- A consulta anual sugerida no teste de autenticação era incompatível com a janela da IPS reconhecida posteriormente.
- A proposta de janelas de 180 dias precisou ser corrigida para até 60 datas inclusivas.
- A indicação de catálogo SWRC_CATALOG foi revista para M2M_CATALOG na discussão dos dados consultados.
- A leitura de allKpValues precisou ser corrigida para allKpIndex; o teste simulado repetia o campo incorreto.
- O acesso direto a fontes e ao Supabase esteve limitado em algumas etapas, e testes com dados simulados não comprovaram o preenchimento real do banco.
- Estimativas de tempo, posições aproximadas e velocidades médias exigiram explicação de seus critérios e limites.

**Avaliação geral do uso da IA:**

A IA ajudou a revisar as ideias do grupo, organizar as etapas e explicar dúvidas sobre a coleta, o banco e o painel.
Também apontou caminhos para o mapa 3D e para aproveitar dados complementares.
As respostas precisaram ser conferidas, porque houve erros nas janelas de consulta, no catálogo e no campo do Kp.
Os testes com dados simulados foram úteis para a interface, mas repetiram uma hipótese incorreta na leitura da GST.
A comparação com respostas reais e a conferência dos logs e do banco foram necessárias para identificar os problemas.
O histórico mostra um processo de sugestões, testes e correções, em que as orientações da IA não substituíram a verificação dos resultados.

---

## Links e referências

- NASA APIs e geração de chave: https://api.nasa.gov
- DONKI/IPS: https://api.nasa.gov/DONKI/IPS
- DONKI/MPC, opção inicialmente considerada: https://api.nasa.gov/DONKI/MPC
- DONKI/CME: https://api.nasa.gov/DONKI/CME
- DONKI/GST: https://api.nasa.gov/DONKI/GST
- Base DONKI/CCMC e páginas de eventos: https://ccmc.gsfc.nasa.gov/DONKI/
- Exemplo de evento consultado: https://ccmc.gsfc.nasa.gov/DONKI/view/IPS/30386/-1
- JPL Horizons, endpoint mencionado: https://ssd.jpl.nasa.gov/api/horizons.api
- Documentação do Horizons mencionada na revisão: https://ssd-api.jpl.nasa.gov/doc/horizons.html
- OMNIWeb / CDAWeb, NASA SPDF: fontes discutidas como expansão.
- Banco de choques de Helsinki: https://ipshocks.fi
- Escala de tempestades geomagnéticas G1–G5 da NOAA: referência discutida na visualização do Kp.
- Enunciado da atividade e modelo de ai-interaction.md fornecidos ao grupo.


