"""
DONKI-IPS — pipeline de coleta (NASA DONKI/IPS -> Supabase)
Grupo: SN-2026-GRUPO-14-NASA

O que faz:
  1. Registra o início da execução na tabela `execucoes`.
  2. Consulta a API DONKI/IPS (choques interplanetários) em janelas de datas.
  3. Normaliza os campos de cada evento.
  4. Deduplica pela chave natural (activity_id) — evita o erro PostgreSQL 21000.
  5. Enriquece cada choque com dados físicos:
       a. DONKI/CME  -> velocidade, direção e largura da CME que causou o choque
       b. DONKI/GST  -> Kp máximo da tempestade geomagnética causada pelo choque
       c. JPL Horizons -> posição 3D (UA) da nave que detectou o choque e da Terra
       d. Cálculo próprio -> tempo de viagem da CME (Sol -> nave) e velocidade média
  6. Envia ao Supabase em lotes, com upsert (on_conflict=activity_id).
  7. Finaliza o registro em `execucoes` com contadores e status.
  8. Sai com sys.exit(1) se houver qualquer erro (falha visível no Actions).

Variáveis de ambiente:
  SUPABASE_URL          (obrigatória)  ex.: https://xxxx.supabase.co
  SUPABASE_SERVICE_KEY  (obrigatória)  secret key / service_role
  NASA_API_KEY          (opcional)     sem ela usa DEMO_KEY (não recomendado)
  DATA_INICIO           (opcional)     AAAA-MM-DD — se vazio, decide sozinho:
                                       banco vazio -> carga histórica desde 2010-01-01
                                       banco com dados -> últimos DIAS_ATUALIZACAO dias
  DATA_FIM              (opcional)     AAAA-MM-DD — padrão: hoje (UTC)
"""

import math
import os
import sys
import time
from datetime import date, datetime, timedelta, timezone

import requests

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
DONKI_URL = "https://api.nasa.gov/DONKI"
HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
TABELA_EVENTOS = "ips_eventos"
TABELA_EXECUCOES = "execucoes"

INICIO_HISTORICO = date(2010, 1, 1)   # DONKI tem registros a partir de ~2010
DIAS_ATUALIZACAO = 60                 # janela das execuções agendadas
JANELA_IPS_DIAS = 60                  # a API DONKI/IPS aceita no máximo 60 dias por consulta
JANELA_ENRIQ_DIAS = 30                # janelas de CME/GST (margem de segurança)
TAMANHO_LOTE = 500                    # registros por upsert
LOTE_HORIZONS = 25                    # instantes por consulta ao Horizons
TENTATIVAS = 3                        # tentativas por chamada HTTP
TIMEOUT_HTTP = 60                     # segundos

# Códigos das naves no JPL Horizons (centro do Sol, plano da eclíptica)
HORIZONS_ID = {
    "STEREO A": "-234",
    "STEREO B": "-235",
    "MESSENGER": "-236",
}
ID_TERRA = "399"
DIST_L1_UA = 0.01   # L1 fica ~1,5 milhão de km (0,01 UA) da Terra, em direção ao Sol
KM_POR_UA = 149_597_870.7
# Distância típica ao Sol (UA) quando não há posição do Horizons
DIST_APROX_UA = {"Earth": 0.99, "STEREO A": 0.96, "STEREO B": 1.04}
VIAGEM_MIN_H, VIAGEM_MAX_H = 12, 168   # fora disso, o vínculo CME-choque é suspeito


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
# HTTP com novas tentativas
# ---------------------------------------------------------------------------
def http_get(url, params):
    """GET com até TENTATIVAS tentativas em falhas temporárias (429/5xx/rede)."""
    ultimo_erro = None
    for tentativa in range(1, TENTATIVAS + 1):
        try:
            resp = requests.get(url, params=params, timeout=TIMEOUT_HTTP)
            if resp.status_code == 200:
                return resp
            if resp.status_code in (429, 500, 502, 503, 504):
                ultimo_erro = f"HTTP {resp.status_code}"
            else:
                # 4xx (ex.: chave inválida, período longo demais) não adianta repetir
                raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        except requests.RequestException as e:
            ultimo_erro = str(e)
        espera = 5 * tentativa
        log(f"  tentativa {tentativa}/{TENTATIVAS} falhou ({ultimo_erro}); aguardando {espera}s")
        time.sleep(espera)
    raise RuntimeError(f"falha após {TENTATIVAS} tentativas: {ultimo_erro}")


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
# API NASA DONKI (IPS, CME, GST)
# ---------------------------------------------------------------------------
def janelas(inicio, fim, tamanho):
    """Divide [inicio, fim] em janelas de até `tamanho` dias."""
    atual = inicio
    while atual <= fim:
        final = min(atual + timedelta(days=tamanho - 1), fim)
        yield atual, final
        atual = final + timedelta(days=1)


def janelas_para_datas(datas, tamanho):
    """Menor conjunto de janelas de `tamanho` dias que cobre todas as datas."""
    resultado = []
    for d in sorted(set(datas)):
        if not resultado or d > resultado[-1][1]:
            resultado.append((d, d + timedelta(days=tamanho - 1)))
    return resultado


def buscar_donki(endpoint, nasa_key, inicio, fim, extra=None):
    """Consulta um endpoint DONKI numa janela de datas. Período vazio -> []."""
    params = {"startDate": inicio.isoformat(), "endDate": fim.isoformat(), "api_key": nasa_key}
    params.update(extra or {})
    resp = http_get(f"{DONKI_URL}/{endpoint}", params)
    if not resp.text.strip():          # a API às vezes devolve corpo vazio
        return []
    dados = resp.json()
    if not isinstance(dados, list):
        raise RuntimeError(f"resposta inesperada de {endpoint}: {str(dados)[:200]}")
    return dados


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


def numero(valor):
    try:
        return float(valor) if valor is not None else None
    except (TypeError, ValueError):
        return None


# Colunas de enriquecimento — sempre presentes (o upsert em lote exige as mesmas chaves)
COLUNAS_ENRIQ = (
    "cme_id", "cme_velocidade", "cme_latitude", "cme_longitude", "cme_meia_largura", "cme_tipo",
    "cme_inicio", "tempo_viagem_h", "cme_velocidade_media",
    "gst_id", "kp_max",
    "nave_x", "nave_y", "nave_z", "terra_x", "terra_y", "terra_z",
)


def normalizar(evento, agora_iso):
    """Converte um evento da API para o formato da tabela ips_eventos.
    Retorna None se faltar a chave natural ou a data do evento."""
    activity_id = (evento.get("activityID") or "").strip()
    event_time = converter_data(evento.get("eventTime"))
    if not activity_id or not event_time:
        return None

    version = numero(evento.get("versionId"))
    registro = {
        "activity_id": activity_id,
        "catalog": evento.get("catalog"),
        "location": evento.get("location"),
        "event_time": event_time,
        "submission_time": converter_data(evento.get("submissionTime")),
        "version_id": int(version) if version is not None else None,
        "instruments": lista_unica(evento.get("instruments"), "displayName"),
        "linked_events": lista_unica(evento.get("linkedEvents"), "activityID"),
        "link": evento.get("link"),
        "atualizado_em": agora_iso,
    }
    registro.update({c: None for c in COLUNAS_ENRIQ})
    return registro


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


def lotes(lista, tamanho):
    for i in range(0, len(lista), tamanho):
        yield lista[i:i + tamanho]


# ---------------------------------------------------------------------------
# Enriquecimento 1 e 2 — DONKI/CME e DONKI/GST (ligados pelo linkedEvents)
# ---------------------------------------------------------------------------
def tipo_evento(activity_id):
    """'2024-05-03T02:48:00-CME-001' -> 'CME'."""
    partes = activity_id.split("-")
    return partes[-2] if len(partes) >= 2 else ""


def data_do_id(activity_id):
    """'2024-05-03T02:48:00-CME-001' -> date(2024, 5, 3)."""
    try:
        return date.fromisoformat(activity_id[:10])
    except ValueError:
        return None


def melhor_analise(cme):
    """Entre as análises de uma CME, usa a marcada como mais precisa (ou a última com velocidade)."""
    analises = [a for a in (cme.get("cmeAnalyses") or []) if isinstance(a, dict)]
    com_vel = [a for a in analises if numero(a.get("speed")) is not None]
    for a in com_vel:
        if a.get("isMostAccurate"):
            return a
    return com_vel[-1] if com_vel else None


def kp_maximo(gst):
    # A API usa "allKpIndex" (lista de medições de Kp a cada 3 horas)
    medicoes = gst.get("allKpIndex") or gst.get("allKpValues") or []
    valores = [numero(k.get("kpIndex")) for k in medicoes if isinstance(k, dict)]
    valores = [v for v in valores if v is not None]
    return max(valores) if valores else None


def buscar_por_ids(endpoint, campo_id, ids, nasa_key, info):
    """Baixa só as janelas de datas que contêm os IDs pedidos. Devolve {id: objeto}."""
    encontrados = {}
    datas = [d for d in (data_do_id(i) for i in ids) if d]
    for ini, fim in janelas_para_datas(datas, JANELA_ENRIQ_DIAS):
        try:
            for obj in buscar_donki(endpoint, nasa_key, ini, fim):
                chave = obj.get(campo_id)
                if chave in ids:
                    encontrados[chave] = obj
        except Exception as e:
            info["erros"] += 1
            info["mensagens"].append(f"{endpoint} {ini}..{fim}: {e}")
            log(f"  ERRO {endpoint} {ini} a {fim}: {e}")
        time.sleep(0.5)
    return encontrados


def enriquecer_cme_gst(registros, nasa_key, info):
    ids_cme = {e for r in registros for e in r["linked_events"] if tipo_evento(e) == "CME"}
    ids_gst = {e for r in registros for e in r["linked_events"] if tipo_evento(e) == "GST"}
    log(f"DONKI/CME: {len(ids_cme)} CME(s) ligada(s) | DONKI/GST: {len(ids_gst)} tempestade(s) ligada(s)")

    cmes = buscar_por_ids("CME", "activityID", ids_cme, nasa_key, info) if ids_cme else {}
    gsts = buscar_por_ids("GST", "gstID", ids_gst, nasa_key, info) if ids_gst else {}
    log(f"  encontradas: {len(cmes)} CME(s) ({sum(1 for c in cmes.values() if melhor_analise(c))} com velocidade) | "
        f"{len(gsts)} tempestade(s) ({sum(1 for g in gsts.values() if kp_maximo(g) is not None)} com Kp)")

    com_cme = com_gst = 0
    for r in registros:
        # CME: se houver mais de uma ligada, usa a mais rápida (a provável causa do choque)
        candidatas = []
        for e in r["linked_events"]:
            analise = melhor_analise(cmes[e]) if e in cmes else None
            if analise:
                candidatas.append((numero(analise.get("speed")), e, analise))
        if candidatas:
            vel, cme_id, a = max(candidatas, key=lambda c: c[0])
            r.update({
                "cme_id": cme_id,
                "cme_velocidade": vel,
                "cme_latitude": numero(a.get("latitude")),
                "cme_longitude": numero(a.get("longitude")),
                "cme_meia_largura": numero(a.get("halfAngle")),
                "cme_tipo": a.get("type"),
                # startTime da CME (se faltar, usa o horário embutido no próprio ID)
                "cme_inicio": converter_data(cmes[cme_id].get("startTime"))
                              or converter_data(cme_id[:16] + "Z"),
            })
            com_cme += 1

        # GST: maior Kp entre as tempestades ligadas
        tempestades = [(kp_maximo(gsts[e]), e) for e in r["linked_events"] if e in gsts]
        tempestades = [t for t in tempestades if t[0] is not None]
        if tempestades:
            kp, gst_id = max(tempestades)
            r.update({"gst_id": gst_id, "kp_max": kp})
            com_gst += 1

    log(f"  choques com dados de CME: {com_cme} | com Kp de tempestade: {com_gst}")


# ---------------------------------------------------------------------------
# Enriquecimento 3 — JPL Horizons (posições 3D)
# ---------------------------------------------------------------------------
def para_jd(iso):
    """Data ISO (UTC) -> Dia Juliano."""
    dt = datetime.fromisoformat(iso)
    return dt.timestamp() / 86400.0 + 2440587.5


def consultar_horizons(alvo, jds):
    """Posições heliocêntricas (eclíptica J2000, em UA) de `alvo` nos instantes `jds`.
    Devolve lista de (x, y, z) na mesma ordem. Lança erro se o Horizons recusar."""
    params = {
        "format": "json",
        "COMMAND": f"'{alvo}'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'VECTORS'",
        "CENTER": "'500@10'",          # centro do Sol
        "REF_PLANE": "'ECLIPTIC'",
        "OUT_UNITS": "'AU-D'",
        "VEC_TABLE": "'1'",            # só posição
        "CSV_FORMAT": "'YES'",
        "TLIST_TYPE": "'JD'",
        "TLIST": "'" + " ".join(f"{jd:.6f}" for jd in jds) + "'",
    }
    resp = http_get(HORIZONS_URL, params)
    dados = resp.json()
    texto = dados.get("result", "")
    if dados.get("error") or "$$SOE" not in texto:
        detalhe = dados.get("error") or texto[-300:]
        raise ValueError(f"Horizons ({alvo}): {detalhe.strip()[:200]}")

    corpo = texto.split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    posicoes = []
    for linha in corpo.strip().splitlines():
        campos = [c.strip() for c in linha.split(",")]
        if len(campos) >= 5:
            posicoes.append((float(campos[2]), float(campos[3]), float(campos[4])))
    if len(posicoes) != len(jds):
        raise ValueError(f"Horizons ({alvo}): {len(posicoes)} posições para {len(jds)} instantes")
    return posicoes


def posicoes_horizons(alvo, jds, info):
    """Consulta em lotes; se um lote falhar, tenta instante por instante
    (ex.: uma data fora do período coberto pela missão)."""
    resultado = {}
    for lote in lotes(sorted(set(jds)), LOTE_HORIZONS):
        try:
            for jd, pos in zip(lote, consultar_horizons(alvo, lote)):
                resultado[jd] = pos
        except ValueError as erro_lote:
            log(f"  lote do Horizons recusado ({erro_lote}); tentando instante por instante")
            falhas = 0
            for jd in lote:
                try:
                    resultado[jd] = consultar_horizons(alvo, [jd])[0]
                except ValueError as e:
                    if "no ephemeris" in str(e).lower():
                        info["avisos"] += 1   # data fora da missão — posição fica vazia (normal)
                        log(f"  aviso: {e}")
                    else:
                        falhas += 1
                except Exception as e:
                    falhas += 1
                    info["erros"] += 1
                    info["mensagens"].append(str(e))
                time.sleep(0.3)
            if falhas and falhas == len(lote):
                # Nenhum instante funcionou: problema sistemático (formato, parâmetro).
                # Para aqui em vez de repetir centenas de consultas.
                info["erros"] += 1
                info["mensagens"].append(f"Horizons {alvo}: todas as consultas falharam: {erro_lote}")
                log(f"  ERRO Horizons {alvo}: lote inteiro falhou — interrompendo esta nave")
                break
            if falhas:
                info["erros"] += 1
                info["mensagens"].append(f"Horizons {alvo}: {falhas} instante(s) falharam: {erro_lote}")
        except Exception as e:
            info["erros"] += 1
            info["mensagens"].append(f"Horizons {alvo}: {e}")
            log(f"  ERRO Horizons {alvo}: {e}")
        time.sleep(0.5)
    return resultado


def enriquecer_posicoes(registros, info):
    jd_de = {r["activity_id"]: round(para_jd(r["event_time"]), 6) for r in registros}

    # Terra: para todos os choques (referência no mapa 3D)
    log(f"JPL Horizons: posição da Terra em {len(registros)} instante(s)")
    terra = posicoes_horizons(ID_TERRA, list(jd_de.values()), info)

    # Naves: só para choques detectados fora da Terra
    naves = {}
    for local, alvo in HORIZONS_ID.items():
        jds = [jd_de[r["activity_id"]] for r in registros if r["location"] == local]
        if jds:
            log(f"JPL Horizons: posição da {local} em {len(jds)} instante(s)")
            naves[local] = posicoes_horizons(alvo, jds, info)

    com_pos = 0
    for r in registros:
        jd = jd_de[r["activity_id"]]
        t = terra.get(jd)
        if t:
            r.update({"terra_x": t[0], "terra_y": t[1], "terra_z": t[2]})
        if r["location"] == "Earth" and t:
            # Detectores da Terra (ACE, DSCOVR) ficam em L1: 0,01 UA mais perto do Sol
            dist = math.sqrt(t[0] ** 2 + t[1] ** 2 + t[2] ** 2)
            f = (dist - DIST_L1_UA) / dist
            n = (t[0] * f, t[1] * f, t[2] * f)
        else:
            n = naves.get(r["location"], {}).get(jd)
        if n:
            r.update({"nave_x": n[0], "nave_y": n[1], "nave_z": n[2]})
            com_pos += 1
    log(f"  choques com posição 3D: {com_pos} de {len(registros)}")


# ---------------------------------------------------------------------------
# Enriquecimento 4 — tempo de viagem e velocidade média da CME (cálculo próprio)
# ---------------------------------------------------------------------------
def calcular_viagem(registros):
    """tempo = chegada do choque - saída da CME; velocidade média = distância / tempo.
    Comparada à velocidade inicial (cme_velocidade), mostra se a CME freou ou acelerou."""
    calculados = 0
    for r in registros:
        if not r.get("cme_inicio"):
            continue
        horas = (datetime.fromisoformat(r["event_time"]) - datetime.fromisoformat(r["cme_inicio"])).total_seconds() / 3600
        if not VIAGEM_MIN_H <= horas <= VIAGEM_MAX_H:
            continue
        if r.get("nave_x") is not None:
            dist_ua = math.sqrt(r["nave_x"] ** 2 + r["nave_y"] ** 2 + r["nave_z"] ** 2)
        else:
            dist_ua = DIST_APROX_UA.get(r["location"])
        r["tempo_viagem_h"] = round(horas, 2)
        if dist_ua:
            r["cme_velocidade_media"] = round(dist_ua * KM_POR_UA / (horas * 3600), 1)
        calculados += 1
    log(f"Tempo de viagem da CME calculado para {calculados} choque(s)")


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
    info = {"erros": 0, "avisos": 0, "mensagens": []}   # erros/avisos do enriquecimento

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

    # 2. Coleta (DONKI/IPS)
    agora_iso = datetime.now(timezone.utc).isoformat()
    normalizados = []
    descartados = 0
    for ini, fi in janelas(inicio, fim, JANELA_IPS_DIAS):
        try:
            eventos = buscar_donki("IPS", nasa_key, ini, fi, {"location": "ALL", "catalog": "ALL"})
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
            info["mensagens"].append(f"IPS {ini}..{fi}: {e}")
            log(f"  ERRO na janela {ini} a {fi}: {e}")
        time.sleep(0.5)  # gentileza com a API

    # 3. Deduplicação
    unicos = deduplicar(normalizados)
    log(f"Recebidos: {contadores['registros_recebidos']} | válidos: {len(normalizados)} | "
        f"descartados: {descartados} | únicos: {len(unicos)}")

    # 4. Enriquecimento (cada etapa isolada: uma falha não derruba as outras)
    if unicos:
        for etapa, funcao in (("CME/GST", lambda: enriquecer_cme_gst(unicos, nasa_key, info)),
                              ("Horizons", lambda: enriquecer_posicoes(unicos, info)),
                              ("viagem", lambda: calcular_viagem(unicos))):
            try:
                funcao()
            except Exception as e:
                info["erros"] += 1
                info["mensagens"].append(f"enriquecimento {etapa}: {e}")
                log(f"ERRO no enriquecimento {etapa}: {e}")
        contadores["erros"] += info["erros"]

    # 5. Upsert em lotes
    for n, lote in enumerate(lotes(unicos, TAMANHO_LOTE), start=1):
        try:
            db.upsert_eventos(lote)
            contadores["lotes"] += 1
            contadores["registros_processados"] += len(lote)
            log(f"  lote {n}: {len(lote)} registro(s) enviados")
        except Exception as e:
            contadores["erros"] += 1
            info["mensagens"].append(f"lote {n}: {e}")
            log(f"  ERRO no lote {n}: {e}")

    # 6. Status final
    if contadores["erros"] == 0:
        status = "concluido"   # inclui o caso de 0 eventos no período (não é erro)
    elif contadores["registros_processados"] > 0:
        status = "erro_parcial"
    else:
        status = "erro_critico"

    if descartados:
        info["mensagens"].append(f"{descartados} evento(s) descartado(s) sem activityID/eventTime")
    if info["avisos"]:
        info["mensagens"].append(f"{info['avisos']} instante(s) sem posição no Horizons")

    try:
        db.atualizar_execucao(id_execucao, {
            **contadores,
            "status": status,
            "mensagem": " | ".join(info["mensagens"])[:2000] or None,
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
