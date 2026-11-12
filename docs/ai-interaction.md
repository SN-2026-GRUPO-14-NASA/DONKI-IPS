# Histórico de Interação com IA

> Preencha este arquivo ao longo do desenvolvimento do projeto. Registre TODOS os prompts utilizados — mesmo os que não funcionaram. Este documento é parte obrigatória da avaliação.

---

## Informações gerais

| Campo | Valor |
| :---- | :---- |
| **Grupo** | SN-2026-GRUPO-14-NASA |
| **Integrantes** | [Nome 1], [Nome 2], [Nome 3] |
| **API NASA escolhida** | DONKI/IPS (Interplanetary Shock) |
| **IA utilizada** | Claude (Anthropic) |
| **Data de início** | 12-11-2026 |
| **Data de conclusão** | DD-MM-AAAA |

---

## Interação 1 — Análise do enunciado e escolha inicial da API (MPC)

**Data:** 12-11-2026
**Objetivo:** Fazer a IA ler o enunciado da atividade e adaptar o projeto a uma API fora da lista (DONKI/MPC).

**Prompt enviado à IA:**

```
olá lei os documentos, considere que estamos usando uma api que não está nessa lista, é a Donki/mpc?7
```

**Resumo da resposta:** A IA resumiu o enunciado e o template, propôs nomenclaturas (repositório `DONKI-MPC`, projeto `DONKI-MPC-DB`), endpoint, chave natural (`mpcID`) e campos principais. Alertou que eventos MPC são raros, o que gera muitas respostas vazias.

**O que funcionou:** O mapeamento dos requisitos do enunciado para a API e o alerta sobre a raridade dos eventos.

**O que precisou ajuste:** Por causa do baixo volume de dados da MPC, o grupo decidiu trocar de API (ver Interação 2).

---

## Interação 2 — Troca para a API DONKI/IPS

**Data:** 12-11-2026
**Objetivo:** Adaptar o planejamento para a API DONKI/IPS.

**Prompt enviado à IA:**

```
ok vamos usar o IPS
```

**Resumo da resposta:** A IA descreveu a API IPS (choques interplanetários), endpoint, parâmetros opcionais (`location`, `catalog`), chave natural `activityID` e campos (`catalog`, `location`, `eventTime`, `instruments`, `linkedEvents`, `link`). Sugeriu usar `location` como filtro do painel.

**O que funcionou:** Nomenclaturas `DONKI-IPS` / `DONKI-IPS-DB`, escolha do `activityID` como UNIQUE e a ideia do filtro por `location`.

**O que precisou ajuste:** Os campos foram confirmados testando o endpoint no navegador.

---

## Interação 3 — Plano de ação

**Data:** 12-11-2026
**Objetivo:** Obter um plano de ação para concluir o projeto até o prazo (13/11, 23h59).

**Prompt enviado à IA:**

```
ok antes de tudo me de um plano de ação para terminarmos o projeto
```

**Resumo da resposta:** Plano dividido em dois dias: infraestrutura (GitHub, Supabase, chave NASA, Secrets) → banco e pipeline → painel → documentação → entrega. Incluiu divisão de papéis e pontos de atenção (secret key, resposta vazia da API, backup em vídeo).

**O que funcionou:** A ordem pelo caminho crítico e o checklist de entrega.

**O que precisou ajuste:** —

---

## Interação 4 — Geração da NASA API key

**Data:** 12-11-2026
**Objetivo:** Saber como gerar a chave da NASA.

**Prompt enviado à IA:**

```
como fazer?
```

**Resumo da resposta:** Passo a passo para gerar a chave em api.nasa.gov, URL de teste no navegador e como cadastrá-la como Secret `NASA_API_KEY`.

**O que funcionou:** O passo a passo e a URL de teste.

**O que precisou ajuste:** Ver Interação 5.

---

## Interação 5 — Erro API_KEY_INVALID

**Data:** 12-11-2026
**Objetivo:** Resolver o erro ao testar a chave.

**Prompt enviado à IA:**

```
API_KEY_INVALID
An invalid api_key was supplied. Get one at https://api.nasa.gov:443
```

**Resumo da resposta:** A IA sugeriu testar com a `DEMO_KEY` para isolar o problema e conferir espaços, caracteres faltando e o nome do parâmetro `api_key`.

**O que funcionou:** O diagnóstico — o grupo estava colando a chave errada. Com a chave correta, a API respondeu.

**O que precisou ajuste:** Erro humano (chave copiada errada), não da IA.

---

## Interação 6 — Estrutura do repositório

**Data:** 12-11-2026
**Objetivo:** Criar a estrutura de pastas do repositório conforme o enunciado e ligar a pasta local ao GitHub.

**Prompt enviado à IA:**

```
essa pasta é a do projeto  e esse é o link do git conecte e faça as subpastas https://github.com/SN-2026-GRUPO-14-NASA/DONKI-IPS
```

**Resumo da resposta:** A IA criou a estrutura mínima (`scripts/`, `sql/`, `.github/workflows/`, `docs/`), README inicial, `.gitignore`, `index.html` provisório e este arquivo já preenchido.

**O que funcionou:** Estrutura de pastas e arquivos-base.

**O que precisou ajuste:** A IA não tinha permissão de push no repositório nem acesso ao terminal local, então o grupo executou os comandos `git` manualmente.

---

## Interação 7 — Script SQL do banco (setup.sql)

**Data:** 12-11-2026
**Objetivo:** Gerar o `sql/setup.sql` com tabela principal, tabela de log, constraint UNIQUE, RLS e GRANTs.

**Prompt enviado à IA:**

```
ok vamos fazer sql
```

**Resumo da resposta:** A IA consultou a API para confirmar os campos reais e gerou o script com as tabelas `ips_eventos` (UNIQUE em `activity_id`, listas `instruments` e `linked_events` como `text[]`) e `execucoes` (registros, lotes, erros e status com CHECK), RLS ativo com política de leitura pública e GRANTs (SELECT para anon/authenticated, ALL para service_role). O script é idempotente.

**O que funcionou:** ...

**O que precisou ajuste:** Ao consultar a API, apareceram campos não previstos na Interação 2 (`submissionTime`, `versionId`, `sentNotifications`); os dois primeiros foram incluídos na tabela.

---

## Interação 8 — Script do pipeline (fetch_nasa.py) e workflow

**Data:** 12-11-2026
**Objetivo:** Gerar o `scripts/fetch_nasa.py` (coleta, normalização, deduplicação e upsert) e o `.github/workflows/update-data.yml`.

**Prompt enviado à IA:**

```
faça
```

**Resumo da resposta:** A IA gerou o script em Python (biblioteca `requests`, usando a API REST do Supabase). Ele busca a API em janelas de 60 dias (carga histórica desde 2010 quando o banco está vazio; últimos 60 dias nas execuções agendadas), normaliza os campos, deduplica por `activity_id` mantendo o maior `versionId` (evita o erro 21000), faz upsert em lotes de 500, registra a execução em `execucoes` e sai com `sys.exit(1)` em caso de erro. Gerou também o workflow com `cron` diário, `workflow_dispatch` (com datas opcionais), `permissions: contents: read`, `concurrency` e `timeout-minutes`.

Trecho da deduplicação:

```python
def deduplicar(registros):
    por_id = {}
    for r in registros:
        atual = por_id.get(r["activity_id"])
        if atual is None or (r["version_id"] or 0) >= (atual["version_id"] or 0):
            por_id[r["activity_id"]] = r
    return list(por_id.values())
```

**O que funcionou:** A IA testou o script com dados simulados: duplicatas removidas, resposta vazia tratada como `concluido`, evento sem `activityID` descartado e falha de lote gerando `erro_critico` com saída 1.

**O que precisou ajuste:** O primeiro teste da própria IA estava errado (os dados simulados não caíam na janela de datas certa) e foi corrigido. A pasta `.github` não pôde ser gravada pela IA no computador do grupo, então o arquivo do workflow foi movido manualmente.

---

## Interação 9 — Erro: limite de 60 dias da API

**Data:** 12-11-2026
**Objetivo:** Corrigir a primeira execução do workflow, que terminou com `erro_parcial`.

**Prompt enviado à IA:** (log do GitHub Actions colado na conversa)

```
[11:47:37]   ERRO na janela 2010-01-01 a 2010-06-29: HTTP 400: API Error: Date range cannot exceed 60 days. You requested 179 days.
...
[11:48:08]   2026-10-04 a 2026-11-12: 9 evento(s)
[11:48:09] Fim: status=erro_parcial | processados=9 | lotes=1 | erros=34
Error: Process completed with exit code 1.
```

**Resumo da resposta:** A IA identificou que o erro era dela: usou janelas de 180 dias, mas a API DONKI/IPS aceita no máximo 60 dias por consulta. Alterou `TAMANHO_JANELA_DIAS` para 60 (carga histórica passa a ter 103 janelas).

**O que funcionou:** O log mostrou que a conexão com o Supabase, o upsert e o registro em `execucoes` funcionaram (9 eventos gravados), e que o tratamento de erro se comportou como esperado: o workflow ficou vermelho com `erro_parcial`.

**O que precisou ajuste:** A IA assumiu um limite de datas sem verificar na documentação nem testar janelas grandes. O limite só apareceu na execução real — boa prova de que o teste com dados simulados não substitui o teste com a API verdadeira.

---

## Interação 10 — Planejamento do painel

**Data:** 12-11-2026
**Objetivo:** Definir o layout e os requisitos do painel (index.html).

**Prompt enviado à IA:**

```
ok como vamos fazer o painel?
```

**Resumo da resposta:** A IA propôs o layout: faixa de última atualização (tabela `execucoes`), filtros por local/ano/busca, cartões de resumo, gráfico de choques por ano empilhado por local (mostrando o ciclo solar) e tabela de eventos. Listou requisitos técnicos: `escapeHtml()`, paginação (limite de 1000 linhas do Supabase) e uso apenas da publishable key.

**O que funcionou:** O layout e o alerta sobre o limite de 1000 linhas por consulta.

**O que precisou ajuste:** —

---

## Interação 11 — Entendimento dos dados da API

**Data:** 12-11-2026
**Objetivo:** Entender exatamente o que a API IPS fornece.

**Prompt enviado à IA:**

```
ok uma duvida o que api mostra? exatamente
```

**Resumo da resposta:** A IA explicou o fenômeno físico (choque no vento solar causado por CMEs ou correntes de vento rápido), descreveu cada campo com um exemplo real de maio/2024 (locais de detecção, instrumentos, eventos ligados, catálogos) e destacou que a API não traz grandezas físicas, apenas ocorrência, local, instrumentos e relações.

**O que funcionou:** A explicação dos campos, útil para a apresentação.

**O que precisou ajuste:** A IA corrigiu uma informação dada antes: o catálogo que aparece nos dados reais é `M2M_CATALOG`, e não `SWRC_CATALOG`.

---

## Interação 12 — Mapa 3D e dados físicos

**Data:** 12-11-2026
**Objetivo:** Avaliar um mapa 3D do Sistema Solar e fontes de dados físicos.

**Prompt enviado à IA:**

```
teria como adicionar uma mapa 3d do sistema solar onde ocorre esses eventos? exite como conseguir os dados fisicos?
```

**Resumo da resposta:** A IA propôs um mapa 3D com Three.js e comparou duas formas de obter as posições (cálculo aproximado por Kepler × JPL Horizons). Para dados físicos, sugeriu DONKI/CME (velocidade da CME), DONKI/GST (índice Kp), OMNIWeb (vento solar) e o banco de choques de Helsinki, com a viabilidade de cada um.

**O que funcionou:** A comparação de custo/benefício das fontes.

**O que precisou ajuste:** —

---

## Interação 13 — Uso de outras APIs segundo o enunciado

**Data:** 12-11-2026
**Objetivo:** Verificar se o enunciado permite usar APIs complementares.

**Prompt enviado à IA:**

```
segundo o documento que te mandei no inicio posso usar outra api?
```

**Resumo da resposta:** A IA citou os trechos do enunciado ("uma API aberta", "uma API diferente para cada grupo"), concluiu que o documento não proíbe nem autoriza explicitamente, alertou que DONKI/CME e DONKI/GST são as APIs dos Grupos 03 e 04 e recomendou consultar o professor.

**O que funcionou:** A leitura cuidadosa do enunciado e o alerta sobre as APIs de outros grupos.

**O que precisou ajuste:** —

---

## Interação 14 — Impacto no desempenho do site

**Data:** 12-11-2026
**Objetivo:** Saber se o enriquecimento deixaria o site mais lento.

**Prompt enviado à IA:**

```
uma pergunta esse fluxo de dados caso implementado atrasaria o site?
```

**Resumo da resposta:** A IA explicou que o enriquecimento roda no pipeline (GitHub Actions) e fica gravado no banco, então o site só lê o Supabase; o custo extra fica na execução agendada. Buscar dados da NASA direto no navegador é que deixaria o site lento e exporia a chave.

**O que funcionou:** O argumento de arquitetura, aproveitado para a apresentação.

**O que precisou ajuste:** —

---

## Interação 15 — Enriquecimento com DONKI/CME, DONKI/GST e JPL Horizons

**Data:** 12-11-2026
**Objetivo:** Implementar o enriquecimento dos dados de cada choque.

**Prompt enviado à IA:**

```
ok vamos implementar o JPL Horizons, e o DONKI/CME e o DONKI/GST
```

**Resumo da resposta:** A IA adicionou 14 colunas ao `setup.sql` (via `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`) e reescreveu o `fetch_nasa.py`: lê os IDs de CME/GST no `linkedEvents`, baixa só as janelas de datas necessárias, escolhe a CME mais rápida e o maior Kp, e consulta o JPL Horizons em lotes de 25 instantes para obter a posição da nave e da Terra. Cada etapa é isolada: uma falha não derruba as outras e é registrada em `execucoes`.

**O que funcionou:** Testes com APIs simuladas (casos normais, Horizons fora do ar e formato inesperado) passaram.

**O que precisou ajuste:** A IA não conseguiu consultar a documentação das APIs CME/GST/Horizons durante o desenvolvimento, então usou janelas de 30 dias por segurança. No primeiro teste, uma data sem efeméride (normal) era tratada como falha geral; a IA corrigiu para tratá-la como aviso.

---

## Interação 16 — Ideia do front-end 3D

**Data:** 12-11-2026
**Objetivo:** Discutir um painel 3D no estilo de um projeto anterior do usuário.

**Prompt enviado à IA:**

```
ok vamos pensar no front, queria algo que nem o apoastro que fizemos o que acha, so que 3d
```

**Resumo da resposta:** A IA propôs uma cena 3D (Three.js) com o Sol, as órbitas e os choques nas posições reais das naves, uma linha do tempo animada de 2010 a 2026, um painel lateral com a cadeia CME → choque → tempestade e, abaixo, as seções obrigatórias (status, filtros, gráficos e tabela).

**O que funcionou:** A estrutura proposta foi adotada.

**O que precisou ajuste:** A IA não encontrou a pasta do projeto anterior no computador; o grupo decidiu não usá-lo como referência.

---

## Interação 17 — Construção do painel (index.html)

**Data:** 12-11-2026
**Objetivo:** Implementar o painel com a URL e a publishable key do Supabase.

**Prompt enviado à IA:**

```
esquece o apoastro vamos pensar independentemente, https://xxbwvcqpdvdrqmwyfoww.supabase.co [publishable key], quer que eu pegue com um select no banco?
```

**Resumo da resposta:** A IA leu o banco pela API REST e descobriu que só havia 18 eventos (a carga histórica não tinha rodado) e que as colunas de enriquecimento estavam vazias. Depois construiu o index.html: cena 3D com Three.js, linha do tempo, painel de detalhe com cone da CME, filtros que valem para todo o painel, indicadores, gráfico de choques por ano (ciclo solar), dispersão velocidade da CME × Kp e tabela. Usou `escapeHtml()` em todo valor externo, aceita só links `https://` e pagina as consultas (limite de 1000 linhas do Supabase). As cores foram validadas para daltonismo; a MESSENGER usa forma diferente (losango) como segunda codificação.

**O que funcionou:** Testado num navegador automatizado com 1.642 eventos simulados: paginação, filtros, seleção, linha do tempo e bloqueio de XSS funcionando.

**O que precisou ajuste:** Nos testes, a IA encontrou e corrigiu: mensagens de "sem dados" aparecendo sobre os gráficos (conflito do atributo `hidden` com CSS), cone da CME opaco demais, rolagem horizontal no celular e rótulos dos planetas sobrepondo o painel de detalhe.

---

<!-- Repita o bloco acima para cada interação com a IA -->

&nbsp;

---

## Resumo final

**Total de interações:** X

**Principais contribuições da IA:**

* ...
* ...

**Principais limitações encontradas:**

* ...
* ...

**Avaliação geral do uso da IA:** Em até 10 linhas, descreva como a IA ajudou (ou atrapalhou) o desenvolvimento do projeto.
