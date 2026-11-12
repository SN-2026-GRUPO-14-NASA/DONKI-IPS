"""
DONKI-IPS — pipeline de coleta (NASA DONKI/IPS -> Supabase)
Grupo: SN-2026-GRUPO-14-NASA

O que faz:
  1. Registra o início da execução na tabela `execucoes`.
  2. Consulta a API DONKI/IPS em janelas de datas.
  3. Normaliza os campos de cada evento.
  4. Deduplica pela chave natural (activity_id) — evita o erro PostgreSQL 21000.
  5. Envia ao Supabase em lotes, com upsert (on_conflict=activity_id).
  6. Finaliza o registro em `execucoes` com contadores e status.
  7. Sai com sys.exit(1) se houver qualquer erro (falha visível no Actions).

Variáveis de ambiente:
  SUPABASE_URL          (obrigatória)  ex.: https://xxxx.supabase.co
  SUPABASE_SERVICE_KEY  (obrigatória)  secret key / service_role
  NASA_API_KEY          (opcional)     sem ela usa DEMO_KEY (não recomendado)
  DATA_INICIO           (opcional)     AAAA-MM-DD — se vazio, decide sozinho:
                                       banco vazio -> carga histórica desde 2010-01-01
                                       banco com dados -> últimos DIAS_ATUALIZACAO dias
  DATA_FIM              (opcional)     AAAA-MM-DD — padrão: hoje (UTC)
"""

import os
import sys
import time
from datetime import date, datetime, timedelta, timezone

import requests

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
API_URL = "https://api.nasa.gov/DONKI/IPS"
TABELA_EVENTOS = "ips_eventos"
TABELA_EXECUCOES = "execucoes"

INICIO_HISTORICO = date(2010, 1, 1)   # DONKI tem registros a partir de ~2010
DIAS_ATUALIZACAO = 60                 # janela das execuções agendadas
TAMANHO_JANELA_DIAS = 60              # a API DONKI/IPS aceita no máximo 60 dias por consulta
TAMANHO_LOTE = 500                    # registros por upsert
TENTATIVAS = 3                        # tentativas por chamada HTTP
TIMEOUT_HTTP = 60                     # segundos


def log(msg):
    """Imprime com horário — aparece nos logs do GitHub Actions."""
    agora = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{agora}] {msg}", flush=True)


def ler_config():
    url = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
    chave = os.environ.get("SUPABASE_SERVICE_KEY", "").strip()
    nasa = os.environ.get("NASA_API_KEY", "").strip()

    faltando = [n for n, v in (("SUPABASE_URL", url), ("SUPABASE_SERVICE_KEY", chave)) if not v]
    if faltando:
        log(f"ERRO: variáveis de ambiente ausentes: {', '.join(faltando)}")
        sys.exit(1)

    if not nasa:
        log("AVISO: NASA_API_KEY não definida — usando DEMO_KEY (limite baixo de requisições).")
        nasa = "DEMO_KEY"

    return url, chave, nasa


# ---------------------------------------------------------------------------
# Supabase (API REST / PostgREST)
# ---------------------------------------------------------------------------
class Supabase:
    def __init__(self, url, chave):
        self.base = f"{url}/rest/v1"
        self.headers = {"apikey": chave, "Content-Type": "application/json"}
        # Chaves antigas (JWT "eyJ...") também vão no Authorization.
        # As novas (sb_secret_...) vão apenas no header apikey.
        if chave.startswith("eyJ"):
            self.headers["Authorization"] = f"Bearer {chave}"

    def _req(self, metodo, tabela, params=None, json=None, prefer=None):
        headers = dict(self.headers)
        if prefer:
            headers["Prefer"] = prefer
        resp = requests.request(
            metodo, f"{self.base}/{tabela}",
            headers=headers, params=params, json=json, timeout=TIMEOUT_HTTP,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f"Supabase {metodo} {tabela} -> HTTP {resp.status_code}: {resp.text[:300]}")
        return resp

    def tabela_vazia(self):
        resp = self._req("GET", TABELA_EVENTOS, params={"select": "id", "limit": "1"})
        return len(resp.json()) == 0

    def inserir_execucao(self, dados):
        resp = self._req("POST", TABELA_EXECUCOES, json=dados, prefer="return=representation")
        return resp.json()[0]["id"]

    def atualizar_execucao(self, id_execucao, dados):
        self._req("PATCH", TABELA_EXECUCOES, params={"id": f"eq.{id_execucao}"},
                  json=dados, prefer="return=minimal")

    def upsert_eventos(self, registros):
        self._req("POST", TABELA_EVENTOS, params={"on_conflict": "activity_id"},
                  json=registros, prefer="resolution=merge-duplicates,return=minimal")


# ---------------------------------------------------------------------------
# API NASA DONKI/IPS
# ---------------------------------------------------------------------------
def janelas(inicio, fim, tamanho=TAMANHO_JANELA_DIAS):
    """Divide [inicio, fim] em janelas de até `tamanho` dias."""
    atual = inicio
    while atual <= fim:
        final = min(atual + timedelta(days=tamanho - 1), fim)
        yield atual, final
        atual = final + timedelta(days=1)


def buscar_janela(nasa_key, inicio, fim):
    """Busca uma janela de datas na API, com novas tentativas em falhas temporárias."""
    params = {
        "startDate": inicio.isoformat(),
        "endDate": fim.isoformat(),
        "location": "ALL",
        "catalog": "ALL",
        "api_key": nasa_key,
    }
    ultimo_erro = None
    for tentativa in range(1, TENTATIVAS + 1):
        try:
            resp = requests.get(API_URL, params=params, timeout=TIMEOUT_HTTP)
            if resp.status_code == 200:
                # Período sem eventos: a API pode devolver [] ou corpo vazio.
                if not resp.text.strip():
                    return []
                dados = resp.json()
                if not isinstance(dados, list):
                    raise RuntimeError(f"resposta inesperada: {str(dados)[:200]}")
                return dados
            if resp.status_code in (429, 500, 502, 503, 504):
                ultimo_erro = f"HTTP {resp.status_code}"
            else:
                # 4xx (ex.: chave inválida) não adianta repetir
                raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        except requests.RequestException as e:
            ultimo_erro = str(e)
        espera = 5 * tentativa
        log(f"  tentativa {tentativa}/{TENTATIVAS} falhou ({ultimo_erro}); aguardando {espera}s")
        time.sleep(espera)
    raise RuntimeError(f"falha após {TENTATIVAS} tentativas: {ultimo_erro}")


# ---------------------------------------------------------------------------
# Normalização e deduplicação
# ---------------------------------------------------------------------------
def converter_data(valor):
    """'2024-05-02T07:46Z' -> '2024-05-02T07:46:00+00:00' (ou None)."""
    if not valor:
        return None
    texto = str(valor).strip().replace("Z", "+00:00")
    for formato in ("%Y-%m-%dT%H:%M%z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z"):
        try:
            return datetime.strptime(texto, formato).isoformat()
        except ValueError:
            continue
    return None


def lista_unica(itens, campo):
    """Extrai `campo` de uma lista de dicts, sem repetições e sem vazios."""
    vistos = []
    for item in itens or []:
        if isinstance(item, dict):
            valor = (item.get(campo) or "").strip()
            if valor and valor not in vistos:
                vistos.append(valor)
    return vistos


def normalizar(evento, agora_iso):
    """Converte um evento da API para o formato da tabela ips_eventos.
    Retorna None se faltar a chave natural ou a data do evento."""
    activity_id = (evento.get("activityID") or "").strip()
    event_time = converter_data(evento.get("eventTime"))
    if not activity_id or not event_time:
        return None

    version = evento.get("versionId")
    try:
        version = int(version) if version is not None else None
    except (TypeError, ValueError):
        version = None

    return {
        "activity_id": activity_id,
        "catalog": evento.get("catalog"),
        "location": evento.get("location"),
        "event_time": event_time,
        "submission_time": converter_data(evento.get("submissionTime")),
        "version_id": version,
        "instruments": lista_unica(evento.get("instruments"), "displayName"),
        "linked_events": lista_unica(evento.get("linkedEvents"), "activityID"),
        "link": evento.get("link"),
        "atualizado_em": agora_iso,
    }


def deduplicar(registros):
    """Mantém um registro por activity_id — o de maior version_id.
    Sem isso, o upsert falha com PostgreSQL 21000
    ('ON CONFLICT DO UPDATE command cannot affect row a second time')."""
    por_id = {}
    for r in registros:
        atual = por_id.get(r["activity_id"])
        if atual is None or (r["version_id"] or 0) >= (atual["version_id"] or 0):
            por_id[r["activity_id"]] = r
    return list(por_id.values())


def lotes(lista, tamanho=TAMANHO_LOTE):
    for i in range(0, len(lista), tamanho):
        yield lista[i:i + tamanho]


# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------
def definir_periodo(db):
    hoje = datetime.now(timezone.utc).date()
    fim_txt = os.environ.get("DATA_FIM", "").strip()
    inicio_txt = os.environ.get("DATA_INICIO", "").strip()

    fim = date.fromisoformat(fim_txt) if fim_txt else hoje
    if inicio_txt:
        inicio = date.fromisoformat(inicio_txt)
        motivo = "informado manualmente"
    elif db.tabela_vazia():
        inicio = INICIO_HISTORICO
        motivo = "banco vazio -> carga histórica"
    else:
        inicio = fim - timedelta(days=DIAS_ATUALIZACAO)
        motivo = f"atualização dos últimos {DIAS_ATUALIZACAO} dias"

    if inicio > fim:
        raise ValueError(f"DATA_INICIO ({inicio}) é posterior a DATA_FIM ({fim})")
    return inicio, fim, motivo


def main():
    url, chave, nasa_key = ler_config()
    db = Supabase(url, chave)

    contadores = {"registros_recebidos": 0, "registros_processados": 0, "lotes": 0, "erros": 0}
    mensagens = []

    # 1. Período e registro inicial da execução
    try:
        inicio, fim, motivo = definir_periodo(db)
        id_execucao = db.inserir_execucao({
            "data_inicio": inicio.isoformat(),
            "data_fim": fim.isoformat(),
            "status": "em_andamento",
        })
    except Exception as e:
        # Sem acesso ao banco não há como registrar a execução
        log(f"ERRO CRÍTICO ao iniciar (verifique SUPABASE_URL / SUPABASE_SERVICE_KEY): {e}")
        sys.exit(1)

    log(f"Execução #{id_execucao} — período {inicio} a {fim} ({motivo})")

    # 2. Coleta
    agora_iso = datetime.now(timezone.utc).isoformat()
    normalizados = []
    descartados = 0
    for ini, fi in janelas(inicio, fim):
        try:
            eventos = buscar_janela(nasa_key, ini, fi)
            contadores["registros_recebidos"] += len(eventos)
            for ev in eventos:
                r = normalizar(ev, agora_iso)
                if r is None:
                    descartados += 1
                else:
                    normalizados.append(r)
            log(f"  {ini} a {fi}: {len(eventos)} evento(s)")
        except Exception as e:
            contadores["erros"] += 1
            mensagens.append(f"API {ini}..{fi}: {e}")
            log(f"  ERRO na janela {ini} a {fi}: {e}")
        time.sleep(0.5)  # gentileza com a API

    # 3. Deduplicação
    unicos = deduplicar(normalizados)
    log(f"Recebidos: {contadores['registros_recebidos']} | válidos: {len(normalizados)} | "
        f"descartados: {descartados} | únicos: {len(unicos)}")

    # 4. Upsert em lotes
    for n, lote in enumerate(lotes(unicos), start=1):
        try:
            db.upsert_eventos(lote)
            contadores["lotes"] += 1
            contadores["registros_processados"] += len(lote)
            log(f"  lote {n}: {len(lote)} registro(s) enviados")
        except Exception as e:
            contadores["erros"] += 1
            mensagens.append(f"lote {n}: {e}")
            log(f"  ERRO no lote {n}: {e}")

    # 5. Status final
    if contadores["erros"] == 0:
        status = "concluido"   # inclui o caso de 0 eventos no período (não é erro)
    elif contadores["registros_processados"] > 0:
        status = "erro_parcial"
    else:
        status = "erro_critico"

    if descartados:
        mensagens.append(f"{descartados} evento(s) descartado(s) sem activityID/eventTime")

    try:
        db.atualizar_execucao(id_execucao, {
            **contadores,
            "status": status,
            "mensagem": " | ".join(mensagens)[:2000] or None,
            "finalizado_em": datetime.now(timezone.utc).isoformat(),
        })
    except Exception as e:
        log(f"ERRO ao finalizar o registro da execução: {e}")
        status = "erro_critico"

    log(f"Fim: status={status} | processados={contadores['registros_processados']} | "
        f"lotes={contadores['lotes']} | erros={contadores['erros']}")

    if status != "concluido":
        sys.exit(1)   # deixa o workflow vermelho no GitHub Actions


if __name__ == "__main__":
    main()
