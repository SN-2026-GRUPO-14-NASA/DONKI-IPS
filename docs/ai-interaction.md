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
