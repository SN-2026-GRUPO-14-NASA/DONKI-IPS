-- =====================================================================
-- DONKI-IPS — setup do banco (Supabase / PostgreSQL)
-- Grupo: SN-2026-GRUPO-14-NASA   Projeto: DONKI-IPS-DB
--
-- Cria:
--   1. ips_eventos  -> choques interplanetários vindos da API NASA DONKI/IPS
--   2. execucoes    -> log de cada execução do pipeline (GitHub Actions)
--   3. RLS + políticas de leitura pública
--   4. GRANTs explícitos
--
-- Pode ser executado mais de uma vez sem erro (idempotente).
-- Execute no Supabase: SQL Editor -> New query -> colar -> Run
-- =====================================================================


-- ---------------------------------------------------------------------
-- 1. Tabela principal: ips_eventos
-- ---------------------------------------------------------------------
-- Exemplo de registro da API:
-- {"catalog":"M2M_CATALOG","activityID":"2024-05-02T07:46:00-IPS-001",
--  "location":"Earth","eventTime":"2024-05-02T07:46Z",
--  "instruments":[{"displayName":"DSCOVR: PLASMAG"}, ...],
--  "linkedEvents":[{"activityID":"2024-05-02T15:00:00-GST-001"}, ...],
--  "link":"https://ccmc.gsfc.nasa.gov/DONKI/view/IPS/30386/-1",
--  "submissionTime":"2024-05-03T21:34Z","versionId":2}
create table if not exists public.ips_eventos (
    id               bigint generated always as identity primary key,
    activity_id      text        not null,          -- chave natural da API (activityID)
    catalog          text,                          -- ex.: M2M_CATALOG, WINSLOW_MESSENGER_ICME_CATALOG
    location         text,                          -- ex.: Earth, STEREO A, STEREO B, MESSENGER
    event_time       timestamptz not null,          -- momento do choque
    submission_time  timestamptz,                   -- quando o evento foi registrado no DONKI
    version_id       integer,                       -- versão do registro na NASA
    instruments      text[]      not null default '{}',  -- nomes dos instrumentos (displayName)
    linked_events    text[]      not null default '{}',  -- activityIDs ligados (CME, GST, HSS...)
    link             text,                          -- página do evento no DONKI
    coletado_em      timestamptz not null default now(),  -- 1ª vez que o pipeline gravou
    atualizado_em    timestamptz not null default now(),  -- última vez que o pipeline gravou

    -- Constraint UNIQUE na chave natural: permite upsert sem duplicatas
    constraint ips_eventos_activity_id_key unique (activity_id)
);

-- Colunas de enriquecimento (dados físicos). Usamos ALTER ... IF NOT EXISTS
-- para que o script funcione tanto num banco novo quanto num que já tem a tabela.
alter table public.ips_eventos
    -- DONKI/CME: ejeção de massa coronal que causou o choque (a mais rápida, se houver várias)
    add column if not exists cme_id            text,
    add column if not exists cme_velocidade    real,   -- km/s
    add column if not exists cme_latitude      real,   -- graus (direção, coordenadas de Stonyhurst)
    add column if not exists cme_longitude     real,   -- graus (0 = direção da Terra)
    add column if not exists cme_meia_largura  real,   -- graus (meia abertura angular do cone)
    add column if not exists cme_tipo          text,   -- classificação por velocidade: S, C, O, R, ER
    add column if not exists cme_inicio        timestamptz,  -- quando a CME saiu do Sol
    add column if not exists tempo_viagem_h    real,   -- horas do Sol até a nave (event_time - cme_inicio)
    add column if not exists cme_velocidade_media real, -- km/s: distância Sol-nave / tempo de viagem
    -- DONKI/GST: tempestade geomagnética causada pelo choque
    add column if not exists gst_id            text,
    add column if not exists kp_max            real,   -- índice Kp máximo (0 a 9)
    -- JPL Horizons: posições heliocêntricas, plano da eclíptica J2000, em UA
    add column if not exists nave_x            double precision,  -- nave que detectou o choque
    add column if not exists nave_y            double precision,
    add column if not exists nave_z            double precision,
    add column if not exists terra_x           double precision,  -- Terra no mesmo instante
    add column if not exists terra_y           double precision,
    add column if not exists terra_z           double precision;

comment on table  public.ips_eventos is 'Choques interplanetários (NASA DONKI/IPS), enriquecidos com DONKI/CME, DONKI/GST e JPL Horizons';
comment on column public.ips_eventos.activity_id is 'Chave natural da API (activityID) — usada no upsert';

-- Índices para os filtros e ordenações do painel
create index if not exists ips_eventos_event_time_idx on public.ips_eventos (event_time desc);
create index if not exists ips_eventos_location_idx   on public.ips_eventos (location);


-- ---------------------------------------------------------------------
-- 2. Tabela de log: execucoes
-- ---------------------------------------------------------------------
create table if not exists public.execucoes (
    id                     bigint generated always as identity primary key,
    iniciado_em            timestamptz not null default now(),
    finalizado_em          timestamptz,
    data_inicio            date,                    -- início da janela consultada na API
    data_fim               date,                    -- fim da janela consultada na API
    registros_recebidos    integer not null default 0,  -- vindos da API (antes da deduplicação)
    registros_processados  integer not null default 0,  -- enviados ao banco (após deduplicação)
    lotes                  integer not null default 0,
    erros                  integer not null default 0,
    status                 text    not null default 'em_andamento',
    mensagem               text,                    -- detalhe do erro, quando houver

    constraint execucoes_status_check
        check (status in ('em_andamento', 'concluido', 'erro_parcial', 'erro_critico'))
);

comment on table public.execucoes is 'Log das execuções do pipeline (GitHub Actions)';

create index if not exists execucoes_iniciado_em_idx on public.execucoes (iniciado_em desc);


-- ---------------------------------------------------------------------
-- 3. Row Level Security (RLS) + políticas de leitura pública
-- ---------------------------------------------------------------------
-- Com RLS ativo, quem usa a publishable key (anon) só consegue o que a
-- política permitir: aqui, apenas SELECT. A escrita fica só para o
-- service_role (pipeline), que ignora o RLS.
alter table public.ips_eventos enable row level security;
alter table public.execucoes   enable row level security;

drop policy if exists "leitura publica ips_eventos" on public.ips_eventos;
create policy "leitura publica ips_eventos"
    on public.ips_eventos
    for select
    to anon, authenticated
    using (true);

drop policy if exists "leitura publica execucoes" on public.execucoes;
create policy "leitura publica execucoes"
    on public.execucoes
    for select
    to anon, authenticated
    using (true);


-- ---------------------------------------------------------------------
-- 4. GRANTs explícitos
-- ---------------------------------------------------------------------
-- Leitura para o painel (anon) e usuários logados (authenticated)
grant usage on schema public to anon, authenticated, service_role;

revoke all on public.ips_eventos from anon, authenticated;
revoke all on public.execucoes   from anon, authenticated;

grant select on public.ips_eventos to anon, authenticated;
grant select on public.execucoes   to anon, authenticated;

-- Acesso total para o pipeline (service_role / secret key)
grant all on public.ips_eventos to service_role;
grant all on public.execucoes   to service_role;
grant usage, select on all sequences in schema public to service_role;


-- ---------------------------------------------------------------------
-- 5. Conferência (opcional) — rode depois do setup
-- ---------------------------------------------------------------------
-- select tablename, rowsecurity from pg_tables where schemaname = 'public';
-- select * from pg_policies where schemaname = 'public';
