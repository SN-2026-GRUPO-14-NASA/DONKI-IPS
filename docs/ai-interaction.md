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
