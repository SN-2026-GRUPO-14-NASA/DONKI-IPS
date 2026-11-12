<img src="assets/logo.svg" width="72" alt="Logo CoronaFlux">

# CoronaFlux — DONKI-IPS

**Pipeline de dados de choques interplanetários (NASA)**

**Organização:** [SN-2026-GRUPO-14-NASA](https://github.com/SN-2026-GRUPO-14-NASA)
**Repositório:** [DONKI-IPS](https://github.com/SN-2026-GRUPO-14-NASA/DONKI-IPS)
**Painel (GitHub Pages):** https://sn-2026-grupo-14-nasa.github.io/DONKI-IPS/
**Projeto Supabase:** DONKI-IPS-DB (região South America — São Paulo)

---

## Sobre a API

A **DONKI** (*Space Weather Database Of Notifications, Knowledge, Information*) é o banco de dados de clima espacial da NASA. O endpoint **IPS** (*Interplanetary Shock*) lista os **choques interplanetários**: frentes de onda no vento solar, geralmente empurradas por ejeções de massa coronal (CMEs), detectadas por sondas e satélites.

- **Endpoint:** `https://api.nasa.gov/DONKI/IPS`
- **Parâmetros:** `startDate`, `endDate` (AAAA-MM-DD), `location` (`Earth`, `STEREO A`, `STEREO B`, `MESSENGER`, `ALL`), `catalog` (`ALL`, `SWRC_CATALOG`, `WINSLOW_MESSENGER_ICME_CATALOG`), `api_key`
- **Chave:** NASA API key (guardada como Secret `NASA_API_KEY`)
- **Chave natural (UNIQUE):** `activityID` — ex.: `2024-05-10T16:36:00-IPS-001`

## Arquitetura

```
NASA DONKI/IPS ──► GitHub Actions (fetch_nasa.py) ──► Supabase (PostgreSQL) ──► GitHub Pages (index.html)
                   cron + workflow_dispatch            ips_eventos + execucoes      API REST pública (leitura)
```

## Estrutura do repositório

```
DONKI-IPS/
├── index.html                    ← painel (GitHub Pages)
├── README.md
├── scripts/
│   └── fetch_nasa.py             ← coleta, deduplicação e upsert
├── sql/
│   └── setup.sql                 ← tabelas, constraint, RLS e GRANTs
├── .github/workflows/
│   └── update-data.yml           ← agendamento do pipeline
└── docs/
    ├── tutorial.pdf              ← guia para replicar o projeto
    ├── ai-interaction.md         ← histórico de prompts com a IA
    ├── reflexao.md               ← análise crítica do uso de IA
    └── apresentacao.pdf          ← slides do seminário
```

## Divisão de responsabilidades

| Papel | Integrante |
|---|---|
| Pipeline (script + workflow) | _[nome]_ |
| Banco de dados (Supabase) | _[nome]_ |
| Painel (index.html) | _[nome]_ |
| Documentação | _[nome]_ |

## Como configurar

_(em construção — será detalhado em `docs/tutorial.pdf`)_

1. Gerar a NASA API key em https://api.nasa.gov
2. Criar o projeto no Supabase e executar `sql/setup.sql` no SQL Editor
3. Cadastrar os Secrets no GitHub (Settings → Secrets and variables → Actions):
   `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `NASA_API_KEY`
4. Rodar o workflow manualmente em Actions → *Run workflow*
5. Ativar o GitHub Pages (Settings → Pages → branch `main`, pasta root)

## Uso de IA generativa

O grupo utilizou o **Claude** (Anthropic) como apoio. Todos os prompts estão registrados em [`docs/ai-interaction.md`](docs/ai-interaction.md) e a análise crítica em [`docs/reflexao.md`](docs/reflexao.md).
