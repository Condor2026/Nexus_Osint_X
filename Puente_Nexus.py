#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Este puente sirve para conectar Nexus Osint X a Osint Crime. Sin el puente las dos herramientas no se comunican. (OsintCrime disponible en Diciembre 2026)
# By Condor2026

"""
Puente_Nexus v1.1 — enlace entre OSINT Crimen + Cyber (osint_crimen.py) y NEXUS Osint X (nexus.py)

NO modifica ninguna de las dos herramientas: son procesos independientes (cada una con su puerto y su
base de datos) y este programa, aparte, las lanza, las vigila y hace que se comuniquen por sus APIs HTTP
locales. Solo usa la librería estándar de Python.

QUÉ HACE
  · Lanza / detiene / vigila las dos herramientas (menú de terminal o panel web del puente).
  · SINCRONIZA OsintCrime → NEXUS: los IOCs que OsintCrime extrae de Telegram (IPs, C2, CVE) y los
    nombres de los grupos más citados pasan a la WATCHLIST de NEXUS. Así NEXUS etiqueta (y sube de
    severidad) cualquier evento del mapa que coincida con ellos.
  · COINCIDENCIAS: cruza los eventos recientes de NEXUS con los IOCs / grupos de OsintCrime y las muestra
    (IP vista en Telegram que además aparece como C2 en el mapa, CVE citado en ambos, grupo mencionado…).
  · Sincronización automática periódica mientras las dos estén en marcha.
  · Todo lo que el puente añade a NEXUS queda registrado en puente_estado.json y se puede RETIRAR.

USO
  python3 Puente_Nexus.py              menú de terminal (+ panel web del puente en http://127.0.0.1:8800)
  python3 Puente_Nexus.py --all        lanza OsintCrime + NEXUS + panel y sincroniza solo (Ctrl+C = apaga lo lanzado)
  python3 Puente_Nexus.py --status     estado de las dos herramientas
  python3 Puente_Nexus.py --sync       una sincronización y sale
  python3 Puente_Nexus.py --matches    coincidencias actuales y sale

  Coloca los tres archivos en la misma carpeta (o indica rutas con --osint-path / --nexus-path o las
  variables OSINT_PATH / NEXUS_PATH). Puertos por defecto: OsintCrime 8765, NEXUS 8000, puente 8800
  (OSINT_PORT, NEXUS_PORT, PUENTE_PORT). Intervalo de sincronización: PUENTE_SYNC_SECS (600).
NOVEDADES v1.1: detecta SOLO el puerto real de NEXUS (si el 8000 está ocupado NEXUS arranca en el 8001, 8002…; el puente lo encuentra y
sincroniza igualmente), comprueba que lo que responde ES NEXUS (no otro programa), cruza también las IPs de grupos de NEXUS con OsintCrime,
filtros y exportación (CSV/JSON) de coincidencias, intervalo de sincronización elegible, estado en vivo de NEXUS en el panel.
  PUENTE_KEEP=1 o --keep: no apagar al salir las herramientas que lanzó el puente.
"""
from __future__ import annotations

import argparse, ast, atexit, csv, glob, html, importlib.util, io, json, os, random, secrets, signal, subprocess, sys
import threading, time, urllib.error, urllib.parse, urllib.request, webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

APP_NAME = "Puente_Nexus"
APP_VERSION = "1.1.0"
BASE = os.path.dirname(os.path.abspath(__file__))
HOST = "127.0.0.1"
UA = f"{APP_NAME}/{APP_VERSION}"

# ── límites de lo que se empuja a NEXUS (para no inundar su watchlist) ──────────────────────────
MAX_IPS, MAX_CVES, MAX_GROUPS = 400, 200, 40
INTERVALS = (60, 300, 600, 1800, 3600)            # intervalos de sincronización automática elegibles en el panel (segundos)
MIN_GROUP_LEN = 4


# ══════════════════════════════════════════════════════════════════════════════
# Utilidades
# ══════════════════════════════════════════════════════════════════════════════
class C:
    on = sys.stdout.isatty() and os.name != "nt" or bool(os.environ.get("WT_SESSION"))
    R = "\033[0m" if on else ""; B = "\033[1m" if on else ""; D = "\033[2m" if on else ""
    G = "\033[92m" if on else ""; Y = "\033[93m" if on else ""; RED = "\033[91m" if on else ""
    CY = "\033[96m" if on else ""

def cp(msg="", color="", bold=False, end="\n"):
    print(f"{C.B if bold else ''}{color}{msg}{C.R}", end=end, flush=True)

def now():
    return datetime.now().strftime("%H:%M:%S")

def http(url, method="GET", form=None, timeout=4.0, parse=True):
    """Petición HTTP local. form = dict -> application/x-www-form-urlencoded. Devuelve JSON (o texto)."""
    data = urllib.parse.urlencode(form).encode() if form is not None else (b"" if method == "POST" else None)
    req = urllib.request.Request(url, data=data, method=method, headers={"User-Agent": UA, "Accept": "application/json,*/*"})
    if form is not None:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", "replace")
    return json.loads(raw) if parse else raw

def port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.4)
        return s.connect_ex((HOST, port)) == 0

def find_file(env_key, patterns):
    v = os.environ.get(env_key)
    if v:
        return os.path.abspath(v)
    for pat in patterns:
        hits = sorted(h for h in glob.glob(os.path.join(BASE, pat)) if os.path.basename(h).lower() != os.path.basename(__file__).lower())
        if hits:
            return hits[0]
    return ""

def third_party_missing(path):
    """Módulos de terceros que importa (a nivel superior) un .py y que NO están instalados en este Python."""
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except Exception:
        return []
    mods = set()
    for n in tree.body:
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            mods.add(n.module.split(".")[0])
    std = getattr(sys, "stdlib_module_names", set())
    return sorted(m for m in mods if m not in std and importlib.util.find_spec(m) is None)

PIP_NAMES = {"dotenv": "python-dotenv", "jwt": "PyJWT", "telegram": "python-telegram-bot", "apscheduler": "APScheduler",
             "jinja2": "Jinja2"}


# ══════════════════════════════════════════════════════════════════════════════
# Gestión de procesos: una clase para cada herramienta
# ══════════════════════════════════════════════════════════════════════════════
LAUNCHED: list["Tool"] = []

class Tool:
    def __init__(self, key, title, path, port, health, args_fn, shutdown_path=None):
        self.key, self.title, self.path, self.port = key, title, path, port
        self.health, self.args_fn, self.shutdown_path = health, args_fn, shutdown_path
        self.proc: subprocess.Popen | None = None
        self.started_at = 0.0
        self.log_path = os.path.join(BASE, "puente_logs", f"{key}.log")

    @property
    def url(self):
        return f"http://{HOST}:{self.port}/"

    def alive_proc(self):
        return bool(self.proc and self.proc.poll() is None)

    def up(self):
        try:
            http(f"http://{HOST}:{self.port}{self.health}", timeout=2.5, parse=False)
            return True
        except urllib.error.HTTPError:
            return True          # responde (aunque sea con 4xx): el servidor está vivo
        except Exception:
            return False

    def state(self):
        """'up' | 'starting' | 'down' | 'crashed'"""
        if self.up():
            return "up"
        if self.alive_proc():
            return "starting"
        if self.proc is not None and self.proc.poll() not in (None, 0):
            return "crashed"
        return "down"

    def log_tail(self, n=14):
        try:
            with open(self.log_path, "rb") as fh:
                lines = fh.read().decode("utf-8", "replace").splitlines()
            i = max((k for k, l in enumerate(lines) if l.startswith("=== lanzamiento")), default=0)
            return lines[i:][-n:]
        except Exception:
            return []

    def start(self):
        """Lanza el proceso (no espera). -> (ok, mensaje)"""
        if not self.path or not os.path.isfile(self.path):
            return False, f"{self.title}: no encuentro el archivo ({self.path or 'sin ruta'}). Ponlo junto al puente o usa --{self.key}-path."
        if self.up():
            return True, f"{self.title} ya está en marcha: {self.url}"
        if self.alive_proc():
            return True, f"{self.title} ya se está iniciando…"
        if port_in_use(self.port):
            old = self.port
            if not self.relocate():
                return False, f"El puerto {self.port} está ocupado por otro programa. Cambia el puerto ({self.key.upper()}_PORT)."
            blog(f"ℹ {self.title}: el puerto {old} estaba ocupado → se usará el {self.port}")
        miss = third_party_missing(self.path)
        if miss:
            pipn = " ".join(PIP_NAMES.get(m, m) for m in miss)
            return False, (f"A este Python ({sys.executable}) le faltan módulos de {self.title}: {', '.join(miss)}.\n"
                           f"    Instálalos con:  \"{sys.executable}\" -m pip install {pipn}")
        env = dict(os.environ)
        env.update(self.env())
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        try:
            lf = open(self.log_path, "ab")
            lf.write(f"\n=== lanzamiento {datetime.now().isoformat(timespec='seconds')} · puerto {self.port} ===\n".encode())
            lf.flush()
            kw = dict(cwd=os.path.dirname(os.path.abspath(self.path)), env=env, stdout=lf, stderr=lf, stdin=subprocess.DEVNULL)
            if os.name == "nt":
                kw["creationflags"] = 0x00000200          # CREATE_NEW_PROCESS_GROUP
            else:
                kw["start_new_session"] = True
            self.proc = subprocess.Popen([sys.executable, self.path] + self.args_fn(self), **kw)
        except Exception as e:
            return False, f"No se pudo lanzar {self.title}: {e}"
        self.started_at = time.time()
        if self not in LAUNCHED:
            LAUNCHED.append(self)
        return True, f"{self.title} lanzado (PID {self.proc.pid}); tarda unos segundos en responder."

    def env(self):
        return {}

    def relocate(self):
        """Busca otro puerto libre si el configurado está ocupado (solo lo implementa NEXUS)."""
        return False

    def wait_up(self, secs):
        t0 = time.time()
        while time.time() - t0 < secs:
            st = self.state()
            if st == "up":
                return True, f"{self.title} en marcha: {self.url}"
            if st == "crashed":
                return False, f"{self.title} terminó al arrancar (código {self.proc.returncode}). Últimas líneas de {self.log_path}:\n    " + "\n    ".join(self.log_tail())
            time.sleep(0.8)
        return False, (f"{self.title} no respondió en {secs}s (el proceso sigue vivo, puede estar arrancando). Últimas líneas del log:\n    "
                       + "\n    ".join(self.log_tail()))

    def stop(self):
        """Parada ordenada y, si no basta, terminación del proceso. -> (ok, mensaje)"""
        if self.up() and self.shutdown_path:
            try:
                http(f"http://{HOST}:{self.port}{self.shutdown_path}", method="POST", timeout=4, parse=False)
            except Exception:
                pass
            for _ in range(14):
                time.sleep(0.5)
                if not self.up():
                    break
        pr = self.proc
        if pr and pr.poll() is None:
            try:
                if os.name == "nt":
                    pr.terminate()
                else:
                    os.killpg(pr.pid, signal.SIGINT)
                pr.wait(timeout=8)
            except Exception:
                try:
                    pr.kill()
                except Exception:
                    pass
        self.proc = None
        if self.up():
            return False, f"{self.title} sigue respondiendo en el puerto {self.port} (¿lo lanzó otra terminal? ciérralo allí)."
        return True, f"{self.title} detenido, puerto {self.port} liberado."


class OsintTool(Tool):
    def env(self):
        return {"PYTHONUNBUFFERED": "1"}

class NexusTool(Tool):
    """NEXUS elige solo el siguiente puerto libre si el suyo está ocupado (8000 → 8001 → …). Este objeto lo ENCUENTRA, y además
    comprueba que lo que responde es NEXUS de verdad (y no otro programa que casualmente use ese puerto)."""
    SCAN = 25                       # puertos que se exploran a partir del configurado
    base_port = 0
    _last_scan = 0.0
    port_note = ""

    def env(self):
        return {"NEXUS_PORT": str(self.port), "NEXUS_HOST": HOST, "PYTHONUNBUFFERED": "1"}

    @staticmethod
    def _is_nexus(port, timeout=1.2):
        try:
            d = http(f"http://{HOST}:{port}/api/health", timeout=timeout)
            return isinstance(d, dict) and d.get("status") == "ok" and "sweep_running" in d and "sources" in d
        except Exception:
            return False

    def _others(self):
        return {CFG.get("bridge_port"), OSINT.port if OSINT else None}

    def up(self):
        if self._is_nexus(self.port):
            return True
        now_t = time.time()
        if now_t - self._last_scan < 4:
            return False
        self._last_scan = now_t
        base = self.base_port or self.port
        for p in [*range(base, base + self.SCAN)]:
            if p == self.port or p in self._others():
                continue
            if self._is_nexus(p, 0.8):
                old, self.port = self.port, p
                self.port_note = f"NEXUS detectado en el puerto {p} (el {old} estaba ocupado o no era NEXUS)"
                blog("🔎 " + self.port_note)
                return True
        return False

    def relocate(self):
        base = self.base_port or self.port
        for p in range(base, base + self.SCAN):
            if p not in self._others() and not port_in_use(p):
                self.port = p
                return True
        return False


CFG = {}          # se rellena en configure()
OSINT: OsintTool
NEXUS: NexusTool

def configure(args):
    global OSINT, NEXUS
    op = args.osint_path or find_file("OSINT_PATH", ["osint_crimen*.py", "*osint*crim*.py", "OsintCrime*.py"])
    npth = args.nexus_path or find_file("NEXUS_PATH", ["nexus.py", "nexus*.py", "Nexus*.py"])
    oport = args.osint_port or int(os.environ.get("OSINT_PORT", "8765"))
    nport = args.nexus_port or int(os.environ.get("NEXUS_PORT", "8000"))
    OSINT = OsintTool("osint", "OsintCrime", op, oport, "/api/escaner",
                      lambda t: ["--web", "--host", HOST, "--port", str(t.port)], None)
    NEXUS = NexusTool("nexus", "NEXUS", npth, nport, "/api/health", lambda t: [], "/api/shutdown")
    NEXUS.base_port = nport
    CFG.update(bridge_port=args.port or int(os.environ.get("PUENTE_PORT", "8800")),
               interval=int(os.environ.get("PUENTE_SYNC_SECS", "600")), keep=args.keep or os.environ.get("PUENTE_KEEP") == "1")


def stop_launched():
    if CFG.get("keep"):
        return
    for t in list(LAUNCHED):
        if t.alive_proc():
            t.stop()

atexit.register(stop_launched)


# ══════════════════════════════════════════════════════════════════════════════
# Comunicación: OsintCrime → NEXUS
# ══════════════════════════════════════════════════════════════════════════════
STATE_PATH = os.path.join(BASE, "puente_estado.json")
LOCK = threading.RLock()
STATE = {"added": {"ip": [], "cve": [], "keyword": []}, "last_sync": None, "matches": [], "log": [], "auto": True}

def load_state():
    try:
        with open(STATE_PATH, encoding="utf-8") as fh:
            d = json.load(fh)
        for k in ("ip", "cve", "keyword"):
            STATE["added"][k] = list(d.get("added", {}).get(k, []))
        STATE["auto"] = bool(d.get("auto", True))
        if int(d.get("interval", 0) or 0) in INTERVALS:
            CFG["interval"] = int(d["interval"])
    except Exception:
        pass

def save_state():
    try:
        with open(STATE_PATH, "w", encoding="utf-8") as fh:
            json.dump({"added": STATE["added"], "auto": STATE["auto"], "interval": CFG.get("interval")}, fh, ensure_ascii=False, indent=1)
    except Exception:
        pass

def blog(msg):
    line = f"{now()} {msg}"
    with LOCK:
        STATE["log"] = (STATE["log"] + [line])[-120:]

def fetch_osint_iocs():
    """IOCs de OsintCrime (todas las IPs, C2 de cualquier tipo y CVE). -> lista de filas únicas por (tipo, valor)."""
    base = OSINT.url.rstrip("/")
    seen, rows = set(), []
    for qs in ("c2=1", "ioc_tipo=ip", "ioc_tipo=cve"):
        try:
            data = http(f"{base}/api/iocs?{qs}", timeout=25)
        except Exception as e:
            raise RuntimeError(f"OsintCrime /api/iocs?{qs}: {type(e).__name__}: {e}")
        for r in data.get("iocs", []):
            k = (r.get("tipo"), str(r.get("valor", "")).lower())
            if k in seen or not k[1]:
                continue
            seen.add(k)
            rows.append(r)
    return rows

def top_groups(rows):
    cnt = {}
    for r in rows:
        for g in r.get("grupos") or []:
            g = str(g).strip()
            if len(g) >= MIN_GROUP_LEN:
                cnt[g] = cnt.get(g, 0) + int(r.get("menciones") or 1)
    return [g for g, _ in sorted(cnt.items(), key=lambda x: -x[1])][:MAX_GROUPS]

def nexus_watch_current():
    w = http(NEXUS.url.rstrip("/") + "/api/watchlist", timeout=6)
    return {k: set(w.get(k, [])) for k in ("ip", "cve", "country", "keyword")}

def sync_now():
    """OsintCrime -> watchlist de NEXUS. -> dict resumen (también guardado como last_sync)."""
    res = {"time": datetime.now().isoformat(timespec="seconds"), "ok": False, "added": {"ip": 0, "cve": 0, "keyword": 0}, "msg": ""}
    try:
        if not OSINT.up():
            raise RuntimeError("OsintCrime no está en marcha")
        if not NEXUS.up():
            raise RuntimeError("NEXUS no está en marcha")
        rows = fetch_osint_iocs()
        cur = nexus_watch_current()
        ips = [r for r in rows if r.get("tipo") == "ip"]
        ips.sort(key=lambda r: (not r.get("c2"), -(int(r.get("menciones") or 0))))
        want = {
            "ip": [f"ip:{str(r['valor']).strip()}" for r in ips[:MAX_IPS]],
            "cve": [str(r["valor"]).upper() for r in rows if r.get("tipo") == "cve"][:MAX_CVES],
            "keyword": [g.lower() for g in top_groups(rows)],
        }
        for kind, vals in want.items():
            for v in vals:
                if v in cur[kind]:
                    continue
                try:
                    http(NEXUS.url.rstrip("/") + "/api/watchlist/add", method="POST", form={"kind": kind, "value": v}, timeout=6)
                except urllib.error.HTTPError as e:
                    if e.code in (401, 403):
                        raise RuntimeError("NEXUS exige autenticación para modificar la watchlist: define NEXUS_LOCAL_NOAUTH=1 (por defecto ya lo está desde el propio equipo)")
                    raise
                res["added"][kind] += 1
                with LOCK:
                    if v not in STATE["added"][kind]:
                        STATE["added"][kind].append(v)
        res["ok"] = True
        res["osint_iocs"] = len(rows)
        res["msg"] = (f"{len(rows)} IOCs leídos de OsintCrime → NEXUS: +{res['added']['ip']} IPs, +{res['added']['cve']} CVE, "
                      f"+{res['added']['keyword']} grupos en la watchlist")
        save_state()
        res["matches"] = len(compute_matches(rows))
    except Exception as e:
        res["msg"] = f"{type(e).__name__}: {e}"
    with LOCK:
        STATE["last_sync"] = res
    blog(("✔ " if res["ok"] else "✖ ") + res["msg"])
    return res

def compute_matches(rows=None, hours=72):
    """Cruza eventos de NEXUS con IOCs/grupos de OsintCrime. -> lista de coincidencias (y la guarda)."""
    if rows is None:
        rows = fetch_osint_iocs()
    ioc_by = {(r.get("tipo"), str(r.get("valor", "")).lower()): r for r in rows}
    groups = [g for g in top_groups(rows)]
    events = http(NEXUS.url.rstrip("/") + f"/api/events?hours={hours}&limit=3000", timeout=30)
    out = []
    for ev in events if isinstance(events, list) else []:
        ents = [e.strip() for e in str(ev.get("entities") or "").split(",") if e.strip()]
        text = f"{ev.get('title') or ''} {ev.get('description') or ''}".lower()
        base = {"evento": ev.get("title"), "dominio": ev.get("domain"), "severidad": ev.get("severity"), "fuente": ev.get("source"),
                "lat": ev.get("lat"), "lon": ev.get("lon"), "fecha": ev.get("timestamp") or ev.get("created_at")}
        for e in ents:
            el = e.lower()
            if el.startswith("ip:"):
                r = ioc_by.get(("ip", el[3:]))
                if r:
                    out.append(dict(base, tipo="IP", valor=e[3:], c2=bool(r.get("c2")), grupos=r.get("grupos") or [],
                                    canales=r.get("canales") or [], menciones=r.get("menciones"), enlace=r.get("mensaje")))
            elif el.startswith("cve-"):
                r = ioc_by.get(("cve", el))
                if r:
                    out.append(dict(base, tipo="CVE", valor=e.upper(), c2=False, grupos=r.get("grupos") or [],
                                    canales=r.get("canales") or [], menciones=r.get("menciones"), enlace=r.get("mensaje")))
        for g in groups:
            if g.lower() in text:
                out.append(dict(base, tipo="GRUPO", valor=g, c2=False, grupos=[g], canales=[], menciones=None, enlace=None))
    try:        # IPs atribuidas a grupos en NEXUS (monitor DDoS / listas) que OsintCrime también ha visto en Telegram
        gi = http(NEXUS.url.rstrip("/") + "/api/group_ips?hist=1&limit=20000", timeout=30)
        for x in (gi.get("ips") or []) if isinstance(gi, dict) else []:
            r = ioc_by.get(("ip", str(x.get("ip", "")).lower()))
            if r:
                out.append({"evento": f"{x.get('g')} · {x.get('r') or x.get('k') or 'IP de grupo'}", "dominio": "grupo", "severidad": "ALTA",
                            "fuente": x.get("s") or "NEXUS (IPs de grupos)", "lat": x.get("la"), "lon": x.get("lo"), "fecha": None,
                            "tipo": "IP-GRUPO", "valor": x.get("ip"), "c2": bool(r.get("c2")),
                            "grupos": sorted({str(x.get("g"))} | {str(g) for g in (r.get("grupos") or [])}),
                            "canales": r.get("canales") or [], "menciones": r.get("menciones"), "enlace": r.get("mensaje"),
                            "vivo": x.get("f") == "l"})
    except Exception as e:
        blog(f"⚠ IPs de grupos de NEXUS no leídas: {type(e).__name__}")
    order = {"CRITICA": 0, "ALTA": 1, "MEDIA": 2, "BAJA": 3}
    out.sort(key=lambda m: (not m.get("c2"), order.get(m.get("severidad"), 9), m["tipo"] not in ("IP", "IP-GRUPO")))
    with LOCK:
        STATE["matches"] = out[:500]
    return out

def retire_from_nexus():
    """Quita de la watchlist de NEXUS TODO lo que añadió el puente (nunca toca lo que pusiste tú)."""
    if not NEXUS.up():
        return False, "NEXUS no está en marcha"
    n = 0
    for kind in ("ip", "cve", "keyword"):
        for v in list(STATE["added"][kind]):
            try:
                http(NEXUS.url.rstrip("/") + "/api/watchlist/remove", method="POST", form={"kind": kind, "value": v}, timeout=6)
                STATE["added"][kind].remove(v); n += 1
            except Exception:
                pass
    save_state()
    blog(f"↩ retirados {n} elementos de la watchlist de NEXUS")
    return True, f"{n} elementos retirados de la watchlist de NEXUS"

def auto_sync_loop():
    last = 0.0
    while True:
        time.sleep(5)
        try:
            if STATE["auto"] and time.time() - last >= CFG["interval"] and OSINT.up() and NEXUS.up():
                last = time.time()
                sync_now()
        except Exception as e:
            blog(f"✖ auto-sync: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# Estado + acciones (compartido por menú y panel web)
# ══════════════════════════════════════════════════════════════════════════════
def tool_status(t: Tool):
    return {"key": t.key, "title": t.title, "state": t.state(), "url": t.url, "port": t.port, "path": t.path,
            "base_port": getattr(t, "base_port", 0) or t.port, "note": getattr(t, "port_note", ""),
            "pid": t.proc.pid if t.alive_proc() else None, "launched_here": t.alive_proc(),
            "log": t.log_tail(6) if t.state() in ("crashed", "starting") else []}

_LIVE = {"t": 0.0, "d": None}
def nexus_live():
    """Resumen en vivo de NEXUS (eventos, críticos, último barrido…). Caché de 6 s; None si NEXUS no responde."""
    if time.time() - _LIVE["t"] < 6:
        return _LIVE["d"]
    _LIVE["t"] = time.time()
    try:
        k = http(NEXUS.url.rstrip("/") + "/api/kpis?hours=24", timeout=2.5)
        iv = {}
        try:
            iv = http(NEXUS.url.rstrip("/") + "/api/sweep/interval", timeout=2)
        except Exception:
            pass
        sev = k.get("by_severity") or {}
        _LIVE["d"] = {"events24": k.get("total"), "critical": sev.get("CRITICA", 0), "high": sev.get("ALTA", 0), "corr": k.get("correlations"),
                      "total_all": k.get("total_all"), "last_sweep": k.get("last_sweep"), "running": bool(k.get("running")),
                      "sweep_every": iv.get("minutes")}
    except Exception:
        _LIVE["d"] = None
    return _LIVE["d"]

def full_status():
    with LOCK:
        sy = STATE["last_sync"]; nm = len(STATE["matches"]); added = {k: len(v) for k, v in STATE["added"].items()}
        log = list(STATE["log"][-30:]); auto = STATE["auto"]
    nx_st = tool_status(NEXUS)
    return {"osint": tool_status(OSINT), "nexus": nx_st, "last_sync": sy, "matches": nm, "added": added,
            "log": log, "auto": auto, "interval": CFG["interval"], "intervals": list(INTERVALS), "version": APP_VERSION,
            "live": nexus_live() if nx_st["state"] == "up" else None}

def run_async(fn, *a):
    threading.Thread(target=fn, args=a, daemon=True).start()

def _start_and_log(t):
    ok, msg = t.start()
    blog(("▶ " if ok else "✖ ") + msg.splitlines()[0])
    if ok and not t.up():
        ok, msg = t.wait_up(75 if t is NEXUS else 30)
        blog(("✔ " if ok else "✖ ") + msg.splitlines()[0])

def _stop_and_log(t):
    ok, msg = t.stop()
    blog(("■ " if ok else "✖ ") + msg)

def _detect_nexus():
    NEXUS._last_scan = 0.0
    if NEXUS.up():
        blog(f"🔎 NEXUS en {NEXUS.url}")
    else:
        blog(f"✖ No encuentro NEXUS en los puertos {NEXUS.base_port}–{NEXUS.base_port + NEXUS.SCAN - 1}")

def action(name, value=None):
    """Acciones del panel web (no bloquean: devuelven enseguida y siguen en segundo plano)."""
    if name == "start_nexus": run_async(_start_and_log, NEXUS)
    elif name == "start_osint": run_async(_start_and_log, OSINT)
    elif name == "start_all":
        run_async(_start_and_log, OSINT); run_async(_start_and_log, NEXUS)
    elif name == "stop_nexus": run_async(_stop_and_log, NEXUS)
    elif name == "stop_osint": run_async(_stop_and_log, OSINT)
    elif name == "stop_all":
        run_async(_stop_and_log, OSINT); run_async(_stop_and_log, NEXUS)
    elif name == "sync": run_async(sync_now)
    elif name == "matches": run_async(lambda: _safe_matches())
    elif name == "retire": run_async(lambda: blog(retire_from_nexus()[1]))
    elif name == "detect": run_async(_detect_nexus)
    elif name == "clear_log":
        with LOCK: STATE["log"] = []
    elif name == "set_interval":
        try: v = int(value)
        except Exception: return False
        if v not in INTERVALS: return False
        CFG["interval"] = v; save_state(); blog(f"⏱ sincronización automática cada {v // 60} min")
    elif name == "set_nexus_port":
        try: v = int(value)
        except Exception: return False
        if not 1024 <= v <= 65535: return False
        NEXUS.port = v; NEXUS.base_port = v; NEXUS._last_scan = 0.0; blog(f"⚙ puerto de NEXUS fijado a {v}")
    elif name == "auto_on": STATE["auto"] = True; save_state()
    elif name == "auto_off": STATE["auto"] = False; save_state()
    else: return False
    return True

def _safe_matches():
    try:
        m = compute_matches()
        blog(f"🔎 {len(m)} coincidencias entre NEXUS y OsintCrime")
    except Exception as e:
        blog(f"✖ coincidencias: {type(e).__name__}: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# Panel web del puente
# ══════════════════════════════════════════════════════════════════════════════
TOKEN = secrets.token_urlsafe(24)

PAGE = r"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Puente_Nexus</title><style>
:root{--bg:#070b16;--card:#0e1526;--line:#1e2a45;--tx:#d7e3ff;--mut:#7f90b5;--cy:#00d4ff;--gr:#2bd67b;--yl:#f5c542;--rd:#ff4d6d;--pu:#8b5cf6}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(1200px 600px at 20% -10%,#12204a55,transparent),var(--bg);color:var(--tx);font:14px/1.45 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
header{display:flex;align-items:center;gap:12px;padding:14px 20px;border-bottom:1px solid var(--line)}
h1{font-size:18px;margin:0;letter-spacing:.08em}.ver{color:var(--mut);font-size:12px}.sp{flex:1}
main{max-width:1180px;margin:0 auto;padding:18px;display:grid;gap:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.card h2{margin:0 0 10px;font-size:14px;letter-spacing:.06em;color:var(--cy)}
.st{display:inline-flex;align-items:center;gap:8px;font-weight:700}.dot{width:10px;height:10px;border-radius:50%;background:#556}
.up .dot{background:var(--gr);box-shadow:0 0 10px var(--gr)}.starting .dot{background:var(--yl)}.crashed .dot{background:var(--rd)}
.mut{color:var(--mut);font-size:12px}.row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
button,a.btn{background:#13203a;color:var(--tx);border:1px solid var(--line);border-radius:8px;padding:8px 12px;cursor:pointer;font:inherit;text-decoration:none}
button:hover,a.btn:hover{border-color:var(--cy)}button.p{background:linear-gradient(135deg,#0aa7d6,var(--pu));border:0;color:#fff;font-weight:700}
button.d{border-color:#5a2434;color:#ffb0bf}.pre{white-space:pre-wrap;background:#0a1020;border:1px solid var(--line);border-radius:8px;padding:8px;font-size:12px;max-height:180px;overflow:auto}
table{width:100%;border-collapse:collapse;font-size:12.5px}th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--mut);font-weight:600}
.tag{padding:1px 7px;border-radius:99px;border:1px solid var(--line);font-size:11px}.t-IP{color:var(--cy)}.t-CVE{color:var(--yl)}.t-GRUPO{color:var(--pu)}.c2{color:var(--rd);font-weight:700}
.sev-CRITICA{color:var(--rd)}.sev-ALTA{color:#ff8a4d}.sev-MEDIA{color:var(--yl)}.sev-BAJA{color:var(--mut)}
.k{font-size:26px;font-weight:700}.kk{display:flex;gap:22px;flex-wrap:wrap}.empty{color:var(--mut);padding:8px}
label{color:var(--mut);display:inline-flex;gap:6px;align-items:center}
.t-IP-GRUPO{color:#ff8ad8}.note{color:var(--yl);font-size:12px;margin-top:6px}.live{color:var(--gr)}.flt{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:4px 0 10px}
input,select{background:#0a1020;color:var(--tx);border:1px solid var(--line);border-radius:8px;padding:6px 8px;font:inherit}input[type=checkbox]{padding:0}
.lv{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px;padding-top:10px;border-top:1px solid var(--line)}.lv b{font-size:18px;color:#fff}.lv span{color:var(--mut);font-size:12px;display:block}
</style></head><body>
<header><h1>🔗 PUENTE_NEXUS</h1><span class="ver" id="ver"></span><span class="sp"></span>
<button id="lang" onclick="toggleLang()">🌐 ES</button></header>
<main>
<div class="grid">
 <div class="card" id="c-osint"></div>
 <div class="card" id="c-nexus"></div>
</div>
<div class="card"><h2 data-i="sync">SINCRONIZACIÓN OsintCrime → NEXUS</h2>
 <div class="kk" id="kpis"></div>
 <div class="mut" id="lastsync" style="margin-top:8px"></div>
 <div class="row">
  <button class="p" onclick="act('start_all')" data-i="startall">▶ Lanzar las dos</button>
  <button class="p" onclick="act('sync')" data-i="syncnow">⇄ Sincronizar ahora</button>
  <button onclick="act('matches')" data-i="refmatch">🔎 Buscar coincidencias</button>
  <button class="d" onclick="act('stop_all')" data-i="stopall">■ Detener las dos</button>
  <label><input type="checkbox" id="auto" onchange="act(this.checked?'auto_on':'auto_off')"> <span data-i="auto">Sincronización automática</span></label>
<label><span data-i="every">cada</span> <select id="ivl" onchange="act('set_interval',this.value)"></select></label>
  <button class="d" onclick="if(confirm(T('confretire')))act('retire')" data-i="retire">↩ Retirar de NEXUS lo añadido</button>
 </div></div>
<div class="card"><h2 data-i="matches">COINCIDENCIAS (eventos de NEXUS que también aparecen en OsintCrime)</h2><div class="flt">
<select id="f-type" onchange="drawMatches()"><option value="" data-i="alltypes">Todos los tipos</option><option>IP</option><option>IP-GRUPO</option><option>CVE</option><option>GRUPO</option></select>
<select id="f-sev" onchange="drawMatches()"><option value="" data-i="allsev">Toda severidad</option><option>CRITICA</option><option>ALTA</option><option>MEDIA</option><option>BAJA</option></select>
<label><input type="checkbox" id="f-c2" onchange="drawMatches()"> <span data-i="onlyc2">solo C2</span></label>
<input id="f-q" placeholder="buscar…" oninput="drawMatches()" style="min-width:160px">
<a class="btn" href="/api/matches.csv" download>⬇ CSV</a><a class="btn" href="/api/matches.json" download>⬇ JSON</a><span class="mut" id="f-count"></span></div>
<div id="matches"></div></div>
<div class="card"><h2 data-i="log">REGISTRO <button style="float:right;padding:2px 8px" onclick="act('clear_log')" data-i="clear">limpiar</button></h2><div class="pre" id="log"></div></div>
</main>
<script>
const TOKEN="__TOKEN__";
const L={es:{sync:"SINCRONIZACIÓN OsintCrime → NEXUS",startall:"▶ Lanzar las dos",syncnow:"⇄ Sincronizar ahora",refmatch:"🔎 Buscar coincidencias",stopall:"■ Detener las dos",auto:"Sincronización automática",retire:"↩ Retirar de NEXUS lo añadido",matches:"COINCIDENCIAS (eventos de NEXUS que también aparecen en OsintCrime)",log:"REGISTRO",
 up:"EN MARCHA",starting:"INICIANDO…",crashed:"CAÍDA",down:"DETENIDA",start:"▶ Lanzar",stop:"■ Detener",open:"↗ Abrir panel",none:"Sin coincidencias todavía. Lanza las dos herramientas, sincroniza y pulsa «Buscar coincidencias».",
 added:"Añadido a NEXUS",ips:"IPs",cves:"CVE",groups:"grupos",found:"Coincidencias",never:"Aún no se ha sincronizado.",last:"Última sincronización",confretire:"¿Quitar de la watchlist de NEXUS todo lo que añadió el puente? (lo que pusiste tú no se toca)",
 type:"Tipo",value:"Valor",event:"Evento",sev:"Sev.",src:"Fuente",grp:"Grupos",link:"Mensaje",cmd:"Código",pid:"PID",
every:"cada",alltypes:"Todos los tipos",allsev:"Toda severidad",onlyc2:"solo C2",clear:"limpiar",detect:"🔎 Detectar NEXUS",port:"Puerto",usedport:"detectado en el puerto",
ev24:"Eventos 24 h",crit:"Críticos",high:"Altas",corr:"Correlaciones",lastsw:"Último barrido",every_sw:"Barrido auto",running:"barriendo…",showing:"mostrando",of:"de",min:"min"},
en:{sync:"SYNC OsintCrime → NEXUS",startall:"▶ Start both",syncnow:"⇄ Sync now",refmatch:"🔎 Find matches",stopall:"■ Stop both",auto:"Automatic sync",retire:"↩ Remove what was added to NEXUS",matches:"MATCHES (NEXUS events that also appear in OsintCrime)",log:"LOG",
 up:"RUNNING",starting:"STARTING…",crashed:"CRASHED",down:"STOPPED",start:"▶ Start",stop:"■ Stop",open:"↗ Open panel",none:"No matches yet. Start both tools, sync, then press “Find matches”.",
 added:"Added to NEXUS",ips:"IPs",cves:"CVEs",groups:"groups",found:"Matches",never:"Not synced yet.",last:"Last sync",confretire:"Remove from NEXUS's watchlist everything the bridge added? (your own entries are untouched)",
 type:"Type",value:"Value",event:"Event",sev:"Sev.",src:"Source",grp:"Groups",link:"Message",cmd:"Code",pid:"PID",
every:"every",alltypes:"All types",allsev:"Any severity",onlyc2:"C2 only",clear:"clear",detect:"🔎 Detect NEXUS",port:"Port",usedport:"detected on port",
ev24:"Events 24 h",crit:"Critical",high:"High",corr:"Correlations",lastsw:"Last sweep",every_sw:"Auto sweep",running:"sweeping…",showing:"showing",of:"of",min:"min"}};
let lang=localStorage.getItem("puente.lang")||"es";const T=k=>(L[lang]||L.es)[k]||k;
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function safeUrl(u){try{const x=new URL(u);return(x.protocol==="http:"||x.protocol==="https:")?x.href:""}catch(e){return""}}
function toggleLang(){lang=lang==="es"?"en":"es";localStorage.setItem("puente.lang",lang);render(LAST)}
async function act(a,v){await fetch("/api/action",{method:"POST",headers:{"Content-Type":"application/json","X-Token":TOKEN},body:JSON.stringify({action:a,value:v})});setTimeout(poll,400)}
function card(t,key){const stl=t.state;return `<h2>${esc(t.title.toUpperCase())}</h2>
 <div class="st ${esc(stl)}"><span class="dot"></span>${esc(T(stl))}</div>
 <div class="mut">${esc(t.url)}${t.pid?" · "+T("pid")+" "+esc(t.pid):""}</div><div class="mut">${T("cmd")}: ${esc(t.path||"—")}</div>
${t.note?`<div class="note">⚠ ${esc(t.note)}</div>`:(stl==="up"&&t.base_port&&t.port!==t.base_port?`<div class="note">⚠ ${T("usedport")} ${esc(t.port)}</div>`:"")}
 <div class="row">${stl==="up"||stl==="starting"?`<button class="d" onclick="act('stop_${key}')">${T("stop")}</button>`:`<button class="p" onclick="act('start_${key}')">${T("start")}</button>`}
 ${stl==="up"?`<a class="btn" href="${esc(t.url)}" target="_blank" rel="noopener">${T("open")}</a>`:""}
${key==="nexus"?`<button onclick="act('detect')">${T("detect")}</button>`:""}</div>
 ${t.log&&t.log.length?`<div class="pre" style="margin-top:10px">${esc(t.log.join("\n"))}</div>`:""}`}
let LAST=null;
function liveBlock(l){if(!l)return"";const ls=l.last_sweep?new Date(l.last_sweep).toLocaleTimeString():"—";
const c=(n,k)=>`<div><b>${esc(n==null?"—":n)}</b><span>${T(k)}</span></div>`;
return `<div class="lv">${c(l.events24,"ev24")}${c(l.critical,"crit")}${c(l.high,"high")}${c(l.corr,"corr")}<div><b>${esc(ls)}</b><span>${T("lastsw")}${l.running?" · "+T("running"):""}</span></div>${l.sweep_every!=null?`<div><b>${l.sweep_every?esc(l.sweep_every)+" "+T("min"):"manual"}</b><span>${T("every_sw")}</span></div>`:""}</div>`}
function render(s){if(!s)return;LAST=s;document.getElementById("ver").textContent="v"+s.version;document.getElementById("lang").textContent="🌐 "+lang.toUpperCase();
 document.querySelectorAll("[data-i]").forEach(e=>{e.textContent=T(e.dataset.i)});
 document.getElementById("c-osint").innerHTML=card(s.osint,"osint");document.getElementById("c-nexus").innerHTML=card(s.nexus,"nexus")+liveBlock(s.live);
const iv=document.getElementById("ivl");if(iv&&document.activeElement!==iv){iv.innerHTML=(s.intervals||[]).map(x=>`<option value="${x}" ${x===s.interval?"selected":""}>${x/60} ${T("min")}</option>`).join("")}
 document.getElementById("auto").checked=!!s.auto;
 document.getElementById("kpis").innerHTML=[[s.added.ip,T("ips")],[s.added.cve,T("cves")],[s.added.keyword,T("groups")],[s.matches,T("found")]].map(([n,l])=>`<div><div class="k">${esc(n)}</div><div class="mut">${l}</div></div>`).join("");
 const ls=s.last_sync;document.getElementById("lastsync").textContent=ls?`${T("last")}: ${ls.time} · ${ls.ok?"✔":"✖"} ${ls.msg}`:T("never");
 document.getElementById("log").textContent=s.log.join("\n");}
async function poll(){try{const s=await(await fetch("/api/status")).json();render(s);}catch(e){}}
let MATCHES=[];
function drawMatches(){const el=document.getElementById("matches");const ty=document.getElementById("f-type").value,sv=document.getElementById("f-sev").value,c2=document.getElementById("f-c2").checked,q=document.getElementById("f-q").value.trim().toLowerCase();
const m=MATCHES.filter(x=>(!ty||x.tipo===ty)&&(!sv||x.severidad===sv)&&(!c2||x.c2)&&(!q||JSON.stringify([x.valor,x.evento,x.fuente,x.grupos,x.canales]).toLowerCase().includes(q)));
document.getElementById("f-count").textContent=MATCHES.length?`${T("showing")} ${Math.min(150,m.length)} ${T("of")} ${MATCHES.length}`:"";
if(!m.length){el.innerHTML=`<div class="empty">${esc(MATCHES.length?"—":T("none"))}</div>`;return}
el.innerHTML=`<table><tr><th>${T("type")}</th><th>${T("value")}</th><th>${T("event")}</th><th>${T("sev")}</th><th>${T("src")}</th><th>${T("grp")}</th><th>${T("link")}</th></tr>`+
m.slice(0,150).map(x=>{const u=safeUrl(x.enlace);return `<tr><td><span class="tag t-${esc(x.tipo)}">${esc(x.tipo)}</span>${x.c2?' <span class="c2">C2</span>':""}${x.vivo?' <span class="live">●</span>':""}</td><td>${esc(x.valor)}</td><td>${esc(x.evento)}</td><td class="sev-${esc(x.severidad)}">${esc(x.severidad)}</td><td>${esc(x.fuente)}</td><td>${esc((x.grupos||[]).join(", "))}</td><td>${u?`<a href="${esc(u)}" target="_blank" rel="noopener noreferrer">↗</a>`:""}</td></tr>`}).join("")+"</table>"}
async function pollMatches(){try{MATCHES=await(await fetch("/api/matches")).json();drawMatches()}catch(e){}}
poll();pollMatches();setInterval(poll,3000);setInterval(pollMatches,8000);
</script></body></html>"""

class Handler(BaseHTTPRequestHandler):
    server_version = APP_NAME

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8", filename=None):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def _host_ok(self):
        h = (self.headers.get("Host") or "").split(":")[0].lower()
        return h in ("127.0.0.1", "localhost", "[::1]")        # frena DNS-rebinding

    def do_GET(self):
        if not self._host_ok():
            return self._send(403, "forbidden", "text/plain")
        path = urllib.parse.urlparse(self.path).path
        try:
            if path == "/":
                self._send(200, PAGE.replace("__TOKEN__", TOKEN), "text/html; charset=utf-8")
            elif path == "/api/status":
                self._send(200, json.dumps(full_status(), ensure_ascii=False))
            elif path == "/api/matches":
                with LOCK:
                    self._send(200, json.dumps(STATE["matches"], ensure_ascii=False))
            elif path in ("/api/matches.json", "/api/matches.csv"):
                with LOCK:
                    rows = list(STATE["matches"])
                stamp = datetime.now().strftime("%Y%m%d_%H%M")
                if path.endswith(".json"):
                    self._send(200, json.dumps(rows, ensure_ascii=False, indent=1), "application/json; charset=utf-8", f"puente_coincidencias_{stamp}.json")
                else:
                    buf = io.StringIO(); cols = ["tipo", "valor", "c2", "severidad", "evento", "dominio", "fuente", "grupos", "canales", "menciones", "lat", "lon", "fecha", "enlace"]
                    w = csv.writer(buf); w.writerow(cols)
                    for r in rows:
                        w.writerow([(";".join(map(str, r.get(c) or [])) if isinstance(r.get(c), list) else ("" if r.get(c) is None else r.get(c))) for c in cols])
                    self._send(200, "\ufeff" + buf.getvalue(), "text/csv; charset=utf-8", f"puente_coincidencias_{stamp}.csv")
            else:
                self._send(404, "not found", "text/plain")
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:
            self._send(500, json.dumps({"error": str(e)}))

    def do_POST(self):
        if not self._host_ok() or self.headers.get("X-Token") != TOKEN:
            return self._send(403, json.dumps({"error": "forbidden"}))
        org = self.headers.get("Origin")
        if org and urllib.parse.urlparse(org).hostname not in ("127.0.0.1", "localhost", "::1"):
            return self._send(403, json.dumps({"error": "origin"}))
        try:
            n = min(int(self.headers.get("Content-Length") or 0), 4096)
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, json.dumps({"error": "bad request"}))
        if urllib.parse.urlparse(self.path).path == "/api/action" and action(str(body.get("action", "")), body.get("value")):
            return self._send(200, json.dumps({"ok": True}))
        self._send(400, json.dumps({"error": "acción desconocida"}))

WEB = {"srv": None}

def start_web(open_browser=False):
    if WEB["srv"]:
        return True
    port = CFG["bridge_port"]
    try:
        srv = ThreadingHTTPServer((HOST, port), Handler)
    except OSError as e:
        cp(f"  ✖ No se pudo abrir el panel del puente en {HOST}:{port}: {e}", C.RED)
        return False
    srv.daemon_threads = True
    WEB["srv"] = srv
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    if open_browser:
        try: webbrowser.open(f"http://{HOST}:{port}/")
        except Exception: pass
    return True


# ══════════════════════════════════════════════════════════════════════════════
# Terminal
# ══════════════════════════════════════════════════════════════════════════════
STATE_TXT = {"up": ("● EN MARCHA", C.G), "starting": ("◐ iniciando…", C.Y), "crashed": ("✖ caída", C.RED), "down": ("○ detenida", C.Y)}

def print_status():
    for t in (OSINT, NEXUS):
        s = t.state(); txt, col = STATE_TXT[s]
        cp(f"  {t.title:<10} {txt:<14}", col, True, end="")
        cp(f" {t.url}" + (f"  (PID {t.proc.pid}, lanzado por el puente)" if t.alive_proc() else ""), C.D)
        if not t.path:
            cp(f"             ⚠ no encuentro el archivo; ponlo junto al puente o usa --{t.key}-path", C.Y)
    if getattr(NEXUS, "port_note", ""):
        cp(f"  ⚠ {NEXUS.port_note}", C.Y)
    ls = STATE["last_sync"]
    if ls:
        cp(f"  Última sincronización {ls['time']}: {'✔' if ls['ok'] else '✖'} {ls['msg']}", C.D)
    cp(f"  Panel del puente: http://{HOST}:{CFG['bridge_port']}/" + ("" if WEB["srv"] else "  (apagado)"), C.D)

def ask(label="  ➤ "):
    try:
        return input(f"{C.B}{C.CY}{label}{C.R}").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return "0"

def start_and_wait(t):
    ok, msg = t.start(); cp("  " + msg, C.G if ok else C.RED)
    if ok and not t.up():
        cp("  Esperando a que responda…", C.D)
        ok, msg = t.wait_up(75 if t is NEXUS else 30); cp("  " + msg, C.G if ok else C.RED)
    return ok

def print_matches(m, limit=25):
    if not m:
        cp("  Sin coincidencias (¿están las dos en marcha y sincronizadas? ¿hay eventos en NEXUS?).", C.Y); return
    cp(f"  {len(m)} coincidencias (primeras {min(limit, len(m))}):", C.G, True)
    for x in m[:limit]:
        cp(f"   [{x['tipo']}{' C2' if x.get('c2') else ''}] {x['valor']}  ·  {x['severidad']}  ·  {str(x['evento'])[:70]}", C.RED if x.get("c2") else C.D)
        if x.get("grupos"): cp(f"        grupos: {', '.join(x['grupos'])}", C.D)

def menu():
    while True:
        print("\033[2J\033[H" if C.on else "\n" * 2, end="")
        cp("═" * 70, C.CY); cp(f"  {APP_NAME} v{APP_VERSION} — enlace OsintCrime ⇄ NEXUS", C.CY, True); cp("═" * 70, C.CY)
        print_status(); cp("─" * 70, C.D)
        for k, l in [("1", "Lanzar las dos herramientas"), ("2", "Lanzar solo OsintCrime"), ("3", "Lanzar solo NEXUS"),
                     ("4", "Sincronizar ahora (OsintCrime → watchlist de NEXUS)"), ("5", "Ver coincidencias NEXUS ⇄ OsintCrime"),
                     ("6", "Abrir paneles en el navegador"), ("7", "Detener las dos"), ("8", "Detener solo NEXUS"),
                     ("9", "Detener solo OsintCrime"), ("a", "Sincronización automática: " + ("ACTIVADA" if STATE["auto"] else "desactivada")),
                     ("r", "Retirar de NEXUS lo que añadió el puente"), ("l", "Ver registro"), ("p", "Detectar el puerto real de NEXUS"), ("0", "Salir")]:
            cp(f"  {k:>2}  {l}", C.R)
        sel = ask()
        try:
            if sel == "0":
                return
            elif sel == "1": start_and_wait(OSINT); start_and_wait(NEXUS); ask("  Enter… ")
            elif sel == "2": start_and_wait(OSINT); ask("  Enter… ")
            elif sel == "3": start_and_wait(NEXUS); ask("  Enter… ")
            elif sel == "4":
                r = sync_now(); cp("  " + r["msg"], C.G if r["ok"] else C.RED); ask("  Enter… ")
            elif sel == "5":
                try: print_matches(compute_matches())
                except Exception as e: cp(f"  ✖ {type(e).__name__}: {e}", C.RED)
                ask("  Enter… ")
            elif sel == "6":
                for t in (OSINT, NEXUS):
                    if t.up(): webbrowser.open(t.url)
                if WEB["srv"]: webbrowser.open(f"http://{HOST}:{CFG['bridge_port']}/")
            elif sel == "7":
                for t in (NEXUS, OSINT): cp("  " + t.stop()[1], C.G)
                ask("  Enter… ")
            elif sel == "8": cp("  " + NEXUS.stop()[1], C.G); ask("  Enter… ")
            elif sel == "9": cp("  " + OSINT.stop()[1], C.G); ask("  Enter… ")
            elif sel == "a": STATE["auto"] = not STATE["auto"]; save_state()
            elif sel == "r":
                if ask("  ¿Quitar de NEXUS todo lo que añadió el puente? (s/N) ") in ("s", "si", "sí", "y", "yes"):
                    cp("  " + retire_from_nexus()[1], C.G); ask("  Enter… ")
            elif sel == "p":
                NEXUS._last_scan = 0.0
                cp("  " + (f"NEXUS encontrado en {NEXUS.url}" if NEXUS.up() else f"No encuentro NEXUS en los puertos {NEXUS.base_port}–{NEXUS.base_port + NEXUS.SCAN - 1}"), C.G); ask("  Enter… ")
            elif sel == "l":
                for line in STATE["log"][-30:]: cp("  " + line, C.D)
                ask("  Enter… ")
        except KeyboardInterrupt:
            print()


# ══════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(prog="Puente_Nexus", description="Enlace OsintCrime ⇄ NEXUS")
    ap.add_argument("--all", action="store_true", help="lanza las dos herramientas + panel y sincroniza solo")
    ap.add_argument("--status", action="store_true"); ap.add_argument("--sync", action="store_true"); ap.add_argument("--matches", action="store_true")
    ap.add_argument("--osint-path"); ap.add_argument("--nexus-path")
    ap.add_argument("--osint-port", type=int); ap.add_argument("--nexus-port", type=int); ap.add_argument("--port", type=int, help="puerto del panel del puente")
    ap.add_argument("--keep", action="store_true", help="no apagar al salir lo que lanzó el puente")
    ap.add_argument("--no-web", action="store_true", help="no abrir el panel web del puente")
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()
    configure(args); load_state()

    if args.status:
        print_status(); return
    if args.sync:
        r = sync_now(); cp(r["msg"], C.G if r["ok"] else C.RED); sys.exit(0 if r["ok"] else 1)
    if args.matches:
        try: print_matches(compute_matches())
        except Exception as e: cp(f"✖ {type(e).__name__}: {e}", C.RED); sys.exit(1)
        return

    for _s in (getattr(signal, "SIGTERM", None), getattr(signal, "SIGHUP", None)):
        if _s is not None:
            try: signal.signal(_s, lambda *a: (stop_launched(), os._exit(0)))
            except (ValueError, OSError): pass
    threading.Thread(target=auto_sync_loop, daemon=True).start()
    if not args.no_web:
        start_web(open_browser=args.all and not args.no_browser)

    if args.all:
        cp(f"\n  {APP_NAME} v{APP_VERSION}", C.CY, True)
        for t in (OSINT, NEXUS):
            _start_and_log(t); st = t.state(); cp(f"  {t.title}: {STATE_TXT[st][0]}  {t.url}", STATE_TXT[st][1])
        cp(f"  Panel del puente: http://{HOST}:{CFG['bridge_port']}/   ·   Ctrl+C para apagar lo lanzado.\n", C.G, True)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            cp("\n  Apagando…", C.Y); stop_launched()
        return
    try:
        menu()
    finally:
        stop_launched()

if __name__ == "__main__":
    main()
