# DONKI-IPS

Painel de choques interplanetários com dados da NASA DONKI/IPS. O projeto coleta os eventos automaticamente, armazena os resultados no Supabase e apresenta os dados em uma interface web publicada no GitHub Pages.

A **DONKI/IPS é a fonte principal**. DONKI/CME, DONKI/GST e JPL Horizons são usados como complementos para obter informações sobre as ejeções associadas, tempestades geomagnéticas e posições no espaço.

## Identificação e links

| Item | Informação |
| --- | --- |
| Grupo | 14 |
| Organização | [SN-2026-GRUPO-14-NASA](https://github.com/SN-2026-GRUPO-14-NASA) |
| Repositório | [DONKI-IPS](https://github.com/SN-2026-GRUPO-14-NASA/DONKI-IPS) |
| Painel | [Abrir o painel DONKI-IPS](https://sn-2026-grupo-14-nasa.github.io/DONKI-IPS/) |
| Projeto Supabase | DONKI-IPS-DB |
| Região prevista para o banco | South America — São Paulo |
| Período de desenvolvimento informado pelo grupo | 11 a 13 de novembro de 2026 |

## Participação dos integrantes

| Integrante | Participação |
| --- | --- |
| Lorenzo | Principal responsável pelos componentes técnicos, incluindo integração das fontes, banco de dados, pipeline, workflow e painel, com apoio de IA. |
| Vitor | Documentação e apresentação; acompanhamento do desenvolvimento técnico e participação nas decisões e sugestões. |
| Cauan | Documentação e apresentação; acompanhamento do desenvolvimento técnico e participação nas decisões e sugestões. |

A implementação técnica ficou concentrada em Lorenzo. Vitor e Cauan acompanharam o desenvolvimento e opinaram sobre as decisões do projeto, além de assumirem a documentação e a apresentação.

## Dados utilizados

A IPS registra ocorrências de choques interplanetários, com identificador, horário, local de detecção, instrumentos, catálogo e vínculos com outros eventos. O identificador `activityID` é armazenado como `activity_id` e funciona como chave natural.

| Fonte | Utilização |
| --- | --- |
| DONKI/IPS | Eventos principais e seus vínculos. |
| DONKI/CME | Velocidade, direção, largura e horário da CME associada. |
| DONKI/GST | Maior índice Kp das tempestades associadas. |
| JPL Horizons | Posições heliocêntricas da Terra e das naves nas datas dos eventos. |

Velocidade da CME, Kp e posições não são campos fornecidos diretamente pela IPS. Os vínculos entre as fontes são usados para enriquecer cada registro.

## Arquitetura

O GitHub Actions executa `scripts/fetch_nasa.py`. O script consulta IPS e fontes complementares, normaliza os registros, remove duplicatas e faz upsert no Supabase. Cada execução gera um registro na tabela `execucoes`. O painel lê a API REST do Supabase; o navegador do visitante não executa a coleta na NASA.

| Componente | Função |
| --- | --- |
| GitHub Actions | Executar a coleta de forma agendada ou manual. |
| Python e requests | Consultar, normalizar, enriquecer e enviar os dados. |
| Supabase e PostgreSQL | Persistir eventos e registrar as execuções. |
| GitHub Pages | Hospedar o painel estático. |
| HTML, CSS, JavaScript, Three.js e Chart.js | Interface, visualização espacial e gráficos. |

## Organização dos arquivos

| Caminho | Conteúdo |
| --- | --- |
| `index.html` | Painel web. |
| `assets/logo.svg` | Logo do DONKI-IPS. |
| `scripts/fetch_nasa.py` | Pipeline de coleta e enriquecimento. |
| `sql/setup.sql` | Tabelas, índices, UNIQUE, RLS e permissões. |
| `.github/workflows/update-data.yml` | Workflow da coleta. |
| `docs/tutorial.pdf` | Guia para reproduzir o projeto. |
| `docs/ai-interaction.md` | Registro dos prompts e resultados do uso de IA. |
| `docs/reflexao.md` | Reflexão do grupo. |
| `docs/apresentacao.pdf` | Slides do seminário. |

Os caminhos de documentação indicam a organização da entrega. Antes de enviar, confira se os respectivos arquivos foram incluídos.

## Como reproduzir

### 1. Obter o código

Para consultar o projeto localmente:

```bash
git clone https://github.com/SN-2026-GRUPO-14-NASA/DONKI-IPS.git
cd DONKI-IPS
```

Para uma reprodução independente, use uma cópia em um repositório público sob sua organização. O agendamento, os Secrets e o Pages precisam estar configurados nesse repositório. Atualize os links para a nova organização. O tutorial apresenta a sequência completa.

### 2. Gerar a chave da NASA

Acesse [NASA Open APIs](https://api.nasa.gov/), use Generate API Key e guarde a chave recebida. Não publique a chave no repositório.

Teste o endpoint IPS com um intervalo curto e substitua `SUA_CHAVE` apenas no seu ambiente:

```text
https://api.nasa.gov/DONKI/IPS?startDate=2024-05-01&endDate=2024-05-31&api_key=SUA_CHAVE
```

O script divide a coleta em janelas de até 60 datas inclusivas. Não use uma consulta anual única.

### 3. Preparar o Supabase

Crie o projeto DONKI-IPS-DB na região São Paulo. Abra o SQL Editor, copie o conteúdo integral de `sql/setup.sql` e execute-o.

O SQL cria:

- `ips_eventos`, com UNIQUE em `activity_id` e campos básicos e de enriquecimento;
- `execucoes`, com datas, contadores, mensagem e status;
- políticas de leitura pública e RLS nas duas tabelas;
- SELECT para `anon` e `authenticated`, e permissões para `service_role`.

Obtenha a URL do projeto, a publishable key e a secret key. A senha do banco não substitui a chave da API. Se estiver utilizando as chaves legadas, o script também trata o formato JWT.

### 4. Configurar os Secrets do GitHub

Em Settings → Secrets and variables → Actions, crie os Repository secrets:

| Nome | Valor |
| --- | --- |
| `SUPABASE_URL` | URL do projeto Supabase. |
| `SUPABASE_SERVICE_KEY` | Secret key do Supabase ou chave legada service_role. |
| `NASA_API_KEY` | Chave pessoal da NASA. |

O workflow utiliza Python 3.12 e instala `requests==2.32.3`. Não é preciso instalar essas ferramentas no computador para executar pelo Actions.

### 5. Executar o pipeline

Abra Actions → Atualizar dados DONKI-IPS → Run workflow. Para garantir a carga histórica, informe `2010-01-01` em `data_inicio`. Deixe `data_fim` vazia para usar a data atual em UTC.

O código usa:

- janelas IPS de até 60 dias, com extremos inclusivos;
- deduplicação por `activity_id`, mantendo a maior `version_id`;
- lotes de até 500 registros no upsert;
- consultas de CME/GST e posições do Horizons;
- log em `execucoes` e saída com erro quando o status final não for `concluido`.

Quando o banco está vazio, a rotina também escolhe automaticamente o histórico desde 2010. Com dados existentes, a execução sem data inicial usa uma janela incremental próxima aos últimos 60 dias. Após uma carga histórica interrompida, informe a data inicial explicitamente para refazer o período completo.

O cron `0 9 * * *` solicita a execução diária às 09h UTC, equivalentes a 06h de Brasília. O início efetivo depende da fila do GitHub Actions. O workflow possui `permissions: contents: read`, controle de concorrência e timeout de 30 minutos.

### 6. Configurar e publicar o painel

No início do JavaScript de `index.html`, configure `SUPABASE_URL` e `SUPABASE_KEY` para o banco que será consultado. Em `SUPABASE_KEY`, use somente a publishable key.

Em Settings → Pages, selecione Deploy from a branch, branch `main` e pasta `/(root)`. O painel do grupo está no link informado no início deste README. Uma reprodução deve usar o endereço gerado para sua própria organização.

A chave pública identifica a aplicação; as permissões do banco e o RLS controlam quais operações ela pode realizar. A secret key permanece exclusiva do pipeline.

### 7. Conferir o resultado

Abra as tabelas no Table Editor. Confirme o período coletado, a quantidade de eventos e os contadores da última execução. Um workflow verde não garante que todos os campos complementares estejam preenchidos: algumas associações podem não existir.

Abra o painel, teste os filtros, selecione um evento e confira a última atualização. Verifique também o gráfico de Kp e a indicação de posições aproximadas quando não houver efemérides.

## Funcionalidades

- Mapa 3D com Sol, órbitas e locais de detecção.
- Linha do tempo e seleção de eventos.
- Filtros por local, ano, Kp e busca textual.
- Indicadores, gráficos e tabela de eventos.
- Relação entre detecções associadas à mesma CME.
- Tour pelas maiores tempestades nos filtros ativos.
- Histórico das últimas execuções do pipeline.
- Links diretos para eventos e exportação CSV.
- Paginação das consultas ao Supabase e escape de valores externos inseridos em HTML.

## Critérios e limitações

Quando uma CME possui várias análises, o script prioriza uma análise marcada como mais precisa e com velocidade. Havendo várias CMEs associadas ao choque, escolhe a de maior velocidade. Para GST, utiliza o maior Kp disponível entre as tempestades vinculadas.

O tempo de viagem é estimado a partir do início da CME e da detecção do choque. O cálculo aceita intervalos de 12 a 168 horas e estima a velocidade média pela distância ao Sol dividida pelo tempo. Isso depende dos vínculos e não representa uma medição direta da aceleração da mesma estrutura.

Os dados do Horizons são efemérides. Para o local Earth, o script aproxima a região de L1 deslocando a posição da Terra em direção ao Sol. Na ausência de posição, a interface utiliza aproximações e as sinaliza no detalhe do evento.

Falhas nas fontes complementares podem resultar em campos vazios e erro parcial. Ao repetir uma carga, confira o preenchimento anterior: o upsert pode substituir campos de enriquecimento por valores nulos caso uma consulta complementar falhe.

## Problemas encontrados no desenvolvimento

| Problema | Encaminhamento |
| --- | --- |
| `API_KEY_INVALID` | Conferência e correção da chave usada no teste. |
| Consulta IPS com 180 dias | Redução para janelas de até 60 dias e repetição da carga histórica. |
| Kp ausente apesar de execução sem exceções | Correção de `allKpValues` para `allKpIndex` e orientação para atualizar o histórico. |
| Sobreposições e rolagem lateral no celular | Ajustes no layout do painel. |

## Uso de inteligência artificial

O grupo utilizou Claude para explicações, planejamento, geração de código e correções. A IA teve participação extensa nos componentes técnicos. As decisões, configurações e o acompanhamento do projeto ficaram com o grupo.

O registro está em [docs/ai-interaction.md](docs/ai-interaction.md), e a análise crítica está em [docs/reflexao.md](docs/reflexao.md).

## Referências

- [NASA Open APIs](https://api.nasa.gov/)
- [DONKI e seus registros](https://ccmc.gsfc.nasa.gov/DONKI/)
- [Documentação do JPL Horizons](https://ssd-api.jpl.nasa.gov/doc/horizons.html)
- [Chaves de API do Supabase](https://supabase.com/docs/guides/getting-started/api-keys)
- [GitHub Pages](https://docs.github.com/en/pages/quickstart)

