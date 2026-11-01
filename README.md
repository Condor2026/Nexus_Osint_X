# Nexus_Osint_X · Command Center v3.1

![TheCondor](NEXSUSX.jpg)

> **Radar OSINT autohospedado**: ~110 fuentes públicas, globo 3D con deck.gl, correlación entre dominios, MITRE ATT&CK, panel J.A.R.V.I.S, detector de denuncias en canales públicos de Telegram y bot de Telegram (⚠️ sin probar). Todo en un único `nexus.py` ejecutable con `python nexus.py` o `uvicorn`.

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![deck.gl](https://img.shields.io/badge/deck.gl-9.0-00D4FF?logo=uber&logoColor=white)](https://deck.gl/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![Jinja2](https://img.shields.io/badge/Jinja2-templates-B41717?logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![WebSocket](https://img.shields.io/badge/WebSocket-live-010101?logo=websocket&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[![JWT](https://img.shields.io/badge/JWT-auth-000000?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Telegram](https://img.shields.io/badge/Telegram-sin%20probar-26A5E4?logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![OpenAI](https://img.shields.io/badge/OpenAI-optional-412991?logo=openai&logoColor=white)](https://platform.openai.com/)
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT%26CK-FF0000?logo=mitre&logoColor=white)](https://attack.mitre.org/)
[![OSINT](https://img.shields.io/badge/OSINT-110%2B%20sources-00D4FF)](https://en.wikipedia.org/wiki/Open-source_intelligence)
[![CTI](https://img.shields.io/badge/CTI-threat%20intel-8B5CF6)](https://en.wikipedia.org/wiki/Cyber_threat_intelligence)
[![Defensive](https://img.shields.io/badge/use-defensive-00FF9F)](https://github.com/Condor2026/Nexus_Osint_X)
[![Self-hosted](https://img.shields.io/badge/self--hosted-yes-FFBE0B)](https://github.com/Condor2026/Nexus_Osint_X)
[![Prototype](https://img.shields.io/badge/status-prototype-orange)](https://github.com/Condor2026/Nexus_Osint_X)
[![License](https://img.shields.io/badge/License-MIT-green?logo=opensourceinitiative&logoColor=white)](./LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/Condor2026/Nexus_Osint_X?color=00D4FF&label=last%20commit)](https://github.com/Condor2026/Nexus_Osint_X/commits/main)
[![Repo size](https://img.shields.io/github/repo-size/Condor2026/Nexus_Osint_X?color=8B5CF6)](https://github.com/Condor2026/Nexus_Osint_X)
[![Stars](https://img.shields.io/github/stars/Condor2026/Nexus_Osint_X?style=social)](https://github.com/Condor2026/Nexus_Osint_X/stargazers)
[![Forks](https://img.shields.io/github/forks/Condor2026/Nexus_Osint_X?style=social)](https://github.com/Condor2026/Nexus_Osint_X/network/members)
[![Issues](https://img.shields.io/github/issues/Condor2026/Nexus_Osint_X?color=FF005C)](https://github.com/Condor2026/Nexus_Osint_X/issues)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-FF69B4)](https://github.com/Condor2026/Nexus_Osint_X/pulls)

**Topics:** `osint` · `threat-intelligence` · `cybersecurity` · `dashboard` · `deck-gl` · `mitre-attack` · `cti` · `defensive-security` · `fastapi` · `python` · `globe` · `3d-visualization` · `sqlite` · `ioc` · `threat-hunting` · `security-tools` · `open-source-intelligence` · `cyber-threat-intelligence` · `self-hosted`

---

## ⚠️ Descargo de responsabilidad

- Todos los indicadores (IPs, dominios, hashes) provienen de **fuentes públicas**: CERTs oficiales (GovCERT.ch, CISA), prensa, canales públicos de Telegram, APIs públicas (abuse.ch, Cloudflare Radar, FBI, INTERPOL).
- **Sin verificación independiente.** La atribución a grupos es lo que dicen las fuentes públicas, no una conclusión forense.
- **Uso permitido:** investigación defensiva, threat intelligence, educación, SOC.
- **Uso prohibido:** ataques activos, escaneos no autorizados, acciones legales basadas en estos datos, acoso a personas.
- Los nombres de grupos son **públicos y documentados** por CERTs y prensa (Killnet, NoName057(16), Lazarus, APT28…). No son acusaciones privadas.
- Si eres titular de una IP listada y crees que es un error, abre un issue y se revisa.
- **Este es un prototipo.** No todas las partes están igual de maduras (ver "Estado del proyecto"). Lo que no funciona, se irá arreglando.

### Lo que Nexus_Osint_X NO hace

- ❌ No escanea puertos ni hosts.
- ❌ No explota vulnerabilidades.
- ❌ No contacta con C2 ni con infraestructura maliciosa.
- ❌ No envía tráfico a los indicadores que muestra (las URLs van defangeadas: `hxxp://ejemplo[.]com`).
- ❌ No simula ataques ni genera escenarios hipotéticos.
- ❌ No predice el futuro.
- ❌ No reemplaza a un SOC, un CTI o un analista humano.
- ❌ No verifica independientemente las atribuciones: refleja lo que dice la fuente.

**Nexus_Osint_X es un radar, no un simulador.** Si buscas un war-game o un generador de escenarios, esta no es tu herramienta.

---

## 🚧 Estado del proyecto: prototipo

Nexus_Osint_X es un **prototipo funcional**, hecho con el tiempo y los medios disponibles. **Hice todo lo que pude** con lo que tenía, priorizando que el núcleo (recolección, mapa, correlación, export) funcionara antes que los extras.

| Componente | Estado | Notas |
|---|---|---|
| Recolección de fuentes (~110) | ✅ Funciona | Barrido automático (15 min por defecto) + carril rápido de prensa (4 min) + carril rápido de denuncias (5 min). Fuentes lentas (GDELT crimen ≥40 s) siguen en segundo plano y se incorporan al terminar |
| Globo 3D / mapa plano (deck.gl) | ✅ Funciona | Instancia única en la página, sin iframe, sin recrear WebGL al filtrar. Fallback 2D con Canvas si no hay WebGL/deck.gl |
| Correlación, anomalías, ATT&CK | ✅ Funciona | Scoring ponderado + decaimiento temporal + entidades compartidas |
| Panel JARVIS | ✅ Funciona | Índice de amenaza, radar ATT&CK, timeline, KPIs, temáticas, cripto, buscador de IP |
| Export (12 formatos) | ✅ Funciona | CSV, JSON, NDJSON, GeoJSON, KML, XLSX, Markdown, HTML, lista de IPs, IPs de grupos (CSV/JSON), ZIP |
| Detector de denuncias (Telegram + RSS) | 🟡 En pruebas | Recorre canales públicos `t.me/s/` por tandas rotativas + feeds de seguridad. Puede fallar si Telegram limita (429) o un canal cambia de formato |
| Monitor DDoS (listas vivas) | 🟡 En pruebas | IPs frescas de listas vivas (Blocklist.de, CI Army, GreenSnow, ET, etc.) + ThreatFox + rangos CIDR de NoName057(16); se guardan solo las que coinciden con un grupo, con retención |
| **Bot de Telegram** | ⚠️ **Sin probar** | **No se sabe si funciona.** El código está, pero no se ha ejecutado de principio a fin. **Se arreglará otro día.** |
| LLM (resumen) | 🟡 Opcional | Requiere `OPENAI_API_KEY`; sin ella, devuelve "no disponible" |
| War-gaming / simulación | ❌ No existe | No está previsto (ver Filosofía) |

**Sobre el bot de Telegram:** el código está escrito, pero **no se ha probado**. No sé si arranca, si los comandos responden o si el polling falla. **No lo uses como canal de alertas en producción.** Cuando tenga tiempo, lo probaré y lo arreglaré. Mientras tanto, el resto del sistema funciona sin él: si no defines `TELEGRAM_BOT_TOKEN`, el bot simplemente no arranca y todo lo demás sigue igual.

**Sobre las vulnerabilidades:** hice lo que pude con lo que sé. Las mitigaciones aplicadas están en la sección "Seguridad" de abajo. No es una auditoría formal; si encuentras algo, abre un issue o un aviso privado (ver `SECURITY.md`).

---

## ✨ Qué hace

- **~110 fuentes OSINT** integradas en **Nexus_Osint_X**: ciberataques (DDoS, malware/botnets, fuerza bruta, exploits, ransomware, phishing), MITRE ATT&CK, cibercrimen, crimen mundial/urbano, conflictos, disturbios, naturaleza, salud, economía, sanciones, **FBI Wanted e INTERPOL Red Notices**, **cripto**, **prensa mundial** (BBC, El País, Le Monde, Der Spiegel, Al Jazeera…), búsquedas de disturbios en 6 idiomas.
- **Globo 3D y plano** con `deck.gl` en la propia página (sin iframe) + red neuronal animada de fondo.
- **Arcos reales** atacante→víctima solo cuando ambos extremos son conocidos (Cloudflare Radar, noticias atribuidas, feeds de grupos). Sin dos extremos, no hay arco.
- **Modos temáticos** (todo / ciber / crimen / conflicto / naturaleza-salud / economía / cripto / prensa), ranking de riesgo por país y buscador de IOC.
- **SQLite** con histórico, clustering espacial y retención automática (`NEXUS_RETENTION_DAYS`, 120 días por defecto). La intel de cibercrimen **no se purga nunca** (`NEXUS_KEEP_CYBER=important|all|off`).
- **Correlación** con scoring ponderado, decaimiento temporal y entidades compartidas.
- **Detección de anomalías**: z-score por dominio, entidades nuevas, ráfagas CRÍTICA, sentimiento negativo.
- **Enriquecimiento**: dedupe semántico (SimHash), escalado de severidad, watchlist persistente, tendencias por dominio, búsqueda facetada.
- **Auth** JWT + HTTP Basic + bypass de loopback (`NEXUS_LOCAL_NOAUTH=1` por defecto, solo desde 127.0.0.1 sin proxy y con validación de `Host`/`Origin`/`Sec-Fetch-Site`).
- **Circuit breaker** por fuente: 5 fallos seguidos → pausada 5 min.
- **WebSocket** para actualizaciones en vivo.
- **Export** en 12 formatos: CSV, JSON, NDJSON, GeoJSON, KML, XLSX, Markdown, HTML, lista de IPs, IPs de grupos (CSV/JSON), ZIP.
- **Bot de Telegram** ⚠️ **sin probar** (ver "Estado del proyecto").
- **LLM opcional** con 3 prompts y caché (si defines `OPENAI_API_KEY`).
- **Scheduler** con health monitoring por fuente, retención automática y watchlist persistente.
- **Nuevo: Detector de denuncias** que recorre canales públicos de Telegram (`t.me/s/…`, solo lectura), feeds de seguridad y el monitor DDoS, y guarda cada detección (aunque no se pueda ubicar en el mapa) en la pestaña «🛰 Detector».
- **Nuevo: Buscador de IP** en JARVIS: busca una IP en eventos, listas de grupos y detecciones; avisa si es tu IP pública (con `📡 Mi IP pública`).
- **Nuevo: Criptomonedas** (top 10 por capitalización vía CoinGecko → CoinPaprika) en el panel JARVIS.
- **Nuevo: Export XLSX** (requiere `openpyxl`) y **ZIP** con paquete completo.
- **Nuevo: Anti falsos positivos** en el detector: descarta noticias que *hablan* de un grupo (atribuciones, "según investigadores…") y ataques de un grupo a su aliado.
- **Nuevo: «Eliminar datos»** con modal de confirmación `BORRAR`; **nunca** toca la intel de cibercrimen, IPs de grupos, detecciones, caché de geolocalización, ajustes ni auditoría.
- **Nuevo: Botón «⏻ Apagar»** que cierra NEXUS y libera el puerto (SIGINT + `os._exit(0)` para no dejar hilos colgados).
- **Nuevo: Idioma ES/EN** con conmutador (`🌐 ES/EN`), que se guarda en `localStorage`.
- **Nuevo: Mapa base CARTO** (Oscuro / Claro / Calles) en vista Plano, con atribución © OpenStreetMap · © CARTO. En vista Globo usa el mapa vectorial.
- **Nuevo: nombres de ciudades** (botón `🏙`, más ciudades al acercar), graticule, arcos reales con `GreatCircleLayer`/`ArcLayer`, `ScatterplotLayer` para IPs de grupos (cuadrado = IP única), correlaciones en magenta, y panel de ficha de evento con enlace al original.
- **Nuevo: Circuit breaker + watchlist + «detector» + monitor DDoS** en el mismo proceso, sin cargar meses de intel ni saturar la máquina.

---

## 🚀 Arranque rápido

### 1. Requisitos

- Python **3.11+**
- (Opcional) `GeoLite2-City.mmdb` de MaxMind para geolocalización local. Sin él se usa `ip-api.com/batch` (límite 15 req/min) y, si este limita o falla, `get.geojs.io`.
- (Opcional) `openpyxl` para exportar a Excel (`pip install openpyxl`).

### 2. Instalar y configurar

```bash
git clone https://github.com/Condor2026/Nexus_Osint_X
cd Nexus_Osint_X

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edita .env: como mínimo cambia ADMIN_PASSWORD y genera JWT_SECRET
```

Genera un `JWT_SECRET` fuerte:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Ejecutar

```bash
python nexus.py
# → http://127.0.0.1:8000
```

El primer barrido arranca solo en segundo plano (retrasado ~8 s para que el panel cargue antes). La BD (`nexus.db`) se crea en el primer arranque y se migra automáticamente si ya existía de una versión anterior (añade columnas que falten sin tocar datos).

**Nota:** el host está fijado a `127.0.0.1` por defecto (`NEXUS_HOST`). No se puede poner `0.0.0.0` por error: tendrías que definirlo a propósito en `.env` o editar el `.py`. Si el puerto 8000 está ocupado, usa el siguiente libre (8001…8024) y lo dice en el log.

**Nota sobre instancias:** si arrancas dos NEXUS (p. ej. `dg.py` y `nexus.py`) contra la **misma** `nexus.db`, se bloquean entre sí (`database is locked`) y el panel se cuelga. Al arrancar se avisa en el log con «¡OTRO NEXUS YA ESTÁ USANDO ESTA MISMA BASE DE DATOS!». Cierra el otro (`pkill -f nexus.py`; `pkill -f dg.py`) y deja solo uno.

---

## 🔑 Fuentes y claves

Todas las claves son **opcionales**: sin ellas, la fuente simplemente devuelve 0 eventos y el resto del sistema sigue funcionando. En la pestaña **🩺 Fuentes** se marca con 🔑 la fuente que necesita clave.

| Fuente | Clave necesaria | Dónde obtenerla |
|---|---|---|
| URLhaus, ThreatFox, MalwareBazaar | `ABUSECH_AUTH_KEY` | https://auth.abuse.ch/ (gratis) |
| Cloudflare Radar (DDoS) | `CLOUDFLARE_API_TOKEN` | https://dash.cloudflare.com/profile/api-tokens (permiso Radar) |
| NASA FIRMS | `NASA_FIRMS_MAP_KEY` | https://firms.modaps.eosdis.nasa.gov/api/ |
| OpenSky | `OPENSKY_USER` / `OPENSKY_PASS` | https://opensky-network.org/ |
| FRED | `FRED_API_KEY` | https://fredaccount.stlouisfed.org/apikeys |
| EIA | `EIA_API_KEY` | https://www.eia.gov/opendata/ |
| ACLED | `ACLED_EMAIL` / `ACLED_PASSWORD` | https://developer.acleddata.com/ |
| AISStream | `AISSTREAM_API_KEY` | https://aisstream.io/ |
| ADS-B Exchange | `ADSB_API_KEY` | https://www.adsbexchange.com/ |
| ReliefWeb | `RELIEFWEB_APPNAME` | https://apidoc.reliefweb.int/ |
| OpenSanctions | `OPENSANCTIONS_API_KEY` | https://www.opensanctions.org/api/ |
| Ransomware.live | `RANSOMWARE_LIVE_KEY` | https://www.ransomware.live/ |
| Telegram (⚠️ sin probar) | `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | @BotFather · @userinfobot |
| LLM | `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| Canales de Telegram del detector (opcional) | `NEXUS_TG_CHANNELS` (lista separada por comas, se añaden a los ~600 de Andrómeda) | — |
| Carpeta local de IPs de grupos (opcional) | `NEXUS_GROUP_IP_DIR` (p. ej. `intel/` de Andrómeda con `grupo_<slug>.txt`) | — |

Las fuentes sin clave (Feodo, CISA KEV, SANS ISC, Blocklist.de, ET Compromised, Spamhaus DROP, SSLBL, OpenPhish, RSS de seguridad, GDELT, USGS, EONET, NOAA, WHO, OFAC, FBI Wanted, INTERPOL Red Notices, portales de crimen urbano, cripto —CoinGecko/CoinPaprika—, prensa, etc.) funcionan **desde el primer minuto**.

### Variables de entorno más relevantes

| Variable | Por defecto | Para qué |
|---|---|---|
| `ADMIN_PASSWORD` | `admin123` | **Cámbiala**. Con la de por defecto solo se entra desde 127.0.0.1 |
| `JWT_SECRET` | autogenerado y guardado en `.nexus_jwt_secret` (0600) | Firma JWT; con valor fijo sobrevive a reinicios |
| `NEXUS_HOST` / `NEXUS_PORT` | `127.0.0.1` / `8000` | Escucha |
| `NEXUS_LOCAL_NOAUTH` | `1` | Bypass de loopback para el dashboard (`0` = exige login siempre) |
| `NEXUS_SWEEP_MINUTES` | `15` | Intervalo del barrido completo (se puede cambiar en la barra: manual / 3 / 5 / 15 min / 1 h / 1 día) |
| `NEXUS_NEWS_MINUTES` | `4` | Carril rápido de prensa |
| `NEXUS_GROUPS_MINUTES` | `5` | Carril rápido del detector de denuncias |
| `NEXUS_RETENTION_DAYS` | `120` | Retención de eventos/correlaciones/anomalías/auditoría (0 = nunca) |
| `NEXUS_KEEP_CYBER` | `important` | Qué intel de cibercrimen se conserva siempre (`important`/`all`/`off`) |
| `NEXUS_GROUP_IP_KEEP_DAYS` | `30` | Días que se guarda una IP de grupo sin volver a verla (0 = nunca) |
| `NEXUS_GROUP_IP_CAP` | `1500` | Máx. IPs por grupo |
| `NEXUS_GROUP_FRESH_HOURS` | `72` | «Fresca» = vista en vivo en las últimas N horas |
| `NEXUS_GROUP_SEEDS` | `0` | `1` = añade las IPs fijas de Andrómeda (no frescas) |
| `NEXUS_TG_OFF` | — | `1` = desactiva el detector de Telegram |
| `NEXUS_TG_MINUTES` | `10` | Intervalo mínimo por canal |
| `NEXUS_TG_MAX_AGE_H` | `72` | Edad máxima de un mensaje de Telegram |
| `NEXUS_TG_PER_RUN` | `60` | Canales por tanda (rotan; ~600 canales ≈ 10 pasadas) |
| `NEXUS_DDOS_MON_MINUTES` | `15` | Cada cuánto corre el monitor DDoS |
| `NEXUS_DDOS_MON_GEO` | `600` | Máx. IPs coincidentes que geolocaliza por pasada |
| `NEXUS_SOURCE_CONCURRENCY` | `32` | Fuentes simultáneas del barrido completo |
| `NEXUS_MAP_POINTS` | `1500` | Máx. puntos en el mapa |
| `NEXUS_DECK_URL` / `NEXUS_LAND_URL` | CDN | deck.gl / Natural Earth locales si quieres servir sin CDN |
| `NEXUS_ARC_TARGET` | `38.9072,-77.0369` | Destino por defecto si activas arcos ilustrativos |
| `NEXUS_CONTACT` | `nexus-osint@localhost` | Contacto en el User-Agent fijo de Wikipedia |

---

## 🗺️ Qué significa cada cosa en el mapa

### Puntos
Cada punto es **un evento real** con `source`, `url` y `timestamp` verificables.
- **Tamaño**: severidad + relevancia (CRÍTICA > ALTA > MEDIA > BAJA).
- **Color**: dominio del evento (ver leyenda abajo a la izquierda; clic para filtrar).
- **Halo magenta**: evento CRÍTICA (se dibuja aparte para que no se pierda).
- **Clic en un punto**: abre ficha con fuente, título, descripción, enlace original y coordenadas.

### Arcos (solo ciberataques)
Los arcos **NO son simulaciones ni predicciones**. Solo se dibujan cuando **origen y víctima son conocidos** (etiqueta `flow:XX>YY` en el evento):
- **Cloudflare Radar** mide pares reales `origen → objetivo` de DDoS (capa 3 y 7).
- **Noticias/avisos de ciberseguridad** que atribuyen un ataque a un país/grupo **y** nombran a la víctima (p. ej. *"hackers rusos atacan hospitales de Ucrania"*).
- **Feeds de IPs de grupos** cuando la fuente dice a quién atacó (CERT suizo: IP → Suiza).

Si no hay dos extremos conocidos, **no hay arco**. Una IP maliciosa suelta no tiene víctima: no dibuja nada. Los **conflictos, crimen, naturaleza, economía, cripto… nunca dibujan arcos**, aunque tengan ubicación.

El selector **"Solo flujos reales"** (por defecto) garantiza que solo ves arcos con dato real. Si eliges otro destino (Washington, Londres, Bruselas, Madrid, Berlín, Moscú, Pekín, Tokio, Tel Aviv, Kyiv, São Paulo, Ciudad de México, mi ubicación o centro de la vista), los arcos adicionales son **ilustrativos** (tú eliges el punto), y la interfaz lo indica.

### Correlaciones (círculos magenta)
Agrupaciones de eventos de **dominios distintos** que coinciden en espacio (<5°) y tiempo (<60 min), con entidades compartidas. El `score` se muestra en el tooltip. No son predicciones: son **coincidencias observadas**. Al hacer clic se abre una ficha que explica **de qué hablan** ambos lados, con un veredicto: ✅ vínculo real (comparten IP/CVE), ⚠ vínculo débil (solo comparten país/tema) o ⚠ sin nada en común salvo lugar y hora.

### IPs de grupos (cuadrados)
IPs atribuidas a grupos (Killnet, NoName057(16), DarkStorm, APT28, Lazarus, ransomware…) por **feeds públicos** (GovCERT.ch, SecurityScorecard), **canales públicos de Telegram**, **prensa** o tu **carpeta local de Andrómeda**. El registro es **temporal** (no meses): las IPs caducan a los `NEXUS_GROUP_IP_KEEP_DAYS` días si no se vuelven a ver.
- **Brillante**: vista en vivo en las últimas `NEXUS_GROUP_FRESH_HOURS` horas.
- **Atenuada**: lista histórica (marcar "+históricas" en la toolbar).
- **Borde blanco discontinuo**: IP "reportada" (no verificada, puede ser víctima).
- **Colores por tipo**: hacktivista (naranja), APT (rosa), ransomware (violeta), botnet (verde).

### Lo que NO se dibuja
- Eventos sin país/ciudad reconocible en el texto → se descartan (no se inventan coordenadas).
- Conflictos, crimen, naturaleza, economía, cripto → **no dibujan arcos** (solo ciberataques).
- Escenarios hipotéticos, predicciones, "qué pasaría si" → **no existen en Nexus_Osint_X**.

---

## 🧭 Filosofía: radar, no simulador

Nexus_Osint_X es **OSINT: observación de lo que pasa**, no planificación de lo que podría pasar.

**Lo que Nexus_Osint_X hace:**
- Muestra eventos **reales** con fuente, URL y timestamp.
- Correlaciona **lo que ocurrió** (proximidad espacial + temporal + entidades).
- Alerta de **lo que está pasando** (C2 nuevos, DDoS, anomalías).
- Traza **flujos reales** atacante→víctima solo cuando ambos extremos son conocidos.

**Lo que Nexus_Osint_X deliberadamente NO hace:**
- ❌ No simula cadenas de ataque hipotéticas.
- ❌ No genera escenarios "qué pasaría si" con LLM.
- ❌ No pinta predicciones como si fueran hechos.
- ❌ No reemplaza el juicio del analista con ficción plausible.

**Por qué:** en OSINT, **un dato real con fuente vale más que cien escenarios generados**. Mezclar ficción con señal real convierte el radar en un generador de rumores. Si quieres un simulador de red team, Nexus_Osint_X no es tu herramienta.

**Trazabilidad:** cada punto del mapa tiene `source`, `url`, `timestamp` y `raw_hash` (SHA256). Si no se puede verificar, no se muestra.

---

## 🔒 Seguridad (lo que se ha mitigado)

Este es un **prototipo** y **no ha pasado una auditoría formal**. Aun así, se han aplicado las mitigaciones razonables con el tiempo disponible:

- **Escucha en loopback por defecto** (`127.0.0.1`). No se puede poner `0.0.0.0` por error: hay que definirlo a propósito en `NEXUS_HOST` o editar el `.py`.
- **`NEXUS_HOST=0.0.0.0` NO es seguro por sí solo.** Expone el panel a cualquier IP que pueda llegar a la máquina. Si lo usas, es obligatorio poner algo delante: un proxy inverso con TLS y autenticación (Nginx, Caddy), una VPN (Tailscale, WireGuard) o un firewall que bloquee el puerto salvo desde tu IP. Y en ese caso, `NEXUS_LOCAL_NOAUTH=0` y una `ADMIN_PASSWORD` fuerte.
- **`ADMIN_PASSWORD` por defecto (`admin123`) avisa en el log.** Cámbialo en `.env` antes de usar. Con la de por defecto, **solo se acepta desde 127.0.0.1 y sin cabeceras de proxy** (`X-Forwarded-For`, `X-Real-IP`, `Forwarded`).
- **`JWT_SECRET` autogenerado** si no se define (se guarda en `.nexus_jwt_secret` con permisos 0600 para que las sesiones sobrevivan a reinicios). Si el disco es de solo lectura, cae a un secreto aleatorio por arranque.
- **Bypass de loopback** (`NEXUS_LOCAL_NOAUTH=1`) valida `Host`, `Origin`, `Sec-Fetch-Site` y rechaza `X-Forwarded-For`/`Via`/`X-Forwarded-Host`. No se puede saltar con un proxy mal configurado si lo pones a `0` en producción.
- **Redacción de secretos en el log** (`_RedactFilter`): nunca aparecen claves de `.env` ni parámetros típicos de URL (`key=`, `token=`, `api_key=`…; httpx registra las URL), ni tokens de bot ni `sk-…`. Si `.env` es legible por otros usuarios (permisos), avisa en el log.
- **SQL parametrizado** (`?`): no hay concatenación, no hay SQL injection clásica.
- **Jinja2 con `autoescape=True`** y `esc()` en JS: el contenido externo se escapa antes de insertarse.
- **`_safe_url()`**: solo permite `http(s)://`, bloquea `javascript:` en enlaces externos.
- **URLs de malware defangeadas**: no hay clic accidental a C2 desde el panel.
- **Sin ejecución de código remoto**: los datos externos se tratan como texto.
- **CSRF/DNS-rebinding**: el bypass de loopback exige `Host` loopback y `Origin` igual a `Host` (si hay `Origin`) y `Sec-Fetch-Site` same-origin/none.
- **`.gitignore`** excluye `.env`, `*.db`, `.cache/`, `intel/`, `GeoLite2-City.mmdb`, `.nexus_jwt_secret`.
- **Sin salida a los indicadores**: OpenPhish se resuelve por DNS (nunca se visita la URL); las URLs de malware se muestran defangeadas y el enlace apunta a la ficha de URLhaus; los enlaces de IOC apuntan a servicios externos (VirusTotal, AbuseIPDB…), pero NEXUS no les envía nada por ti.

**Si encuentras una vulnerabilidad**, abre un aviso privado (ver `SECURITY.md`). **No abras un issue público con detalles explotables.**

---

## 📐 Cómo se puntúa

### Severidad de un evento
Cada colector sugiere una severidad base. Luego `assess_severity()` la ajusta:
- **Tipo de dominio**: ransomware +2.5, exploit +2.0, DDoS +1.5, phishing +1.0, fuerza bruta 0.0…
- **Infraestructura crítica afectada** (hospital, energía, gobierno, banca…): +1.5.
- **Escala** (récord, Tbps, millones, nacional…): +1.0.
- **Explotación activa** (0-day, actively exploited, KEV): +1.0.
- **Actor/familia conocida** (LockBit, APT28, Killnet…): +1.0.
- **Vulnerabilidad con ransomware conocido**: +1.5.

Resultado: `CRITICA` (≥4.5) · `ALTA` (≥3.0) · `MEDIA` (≥1.8) · `BAJA` (<1.8).

`escalate_severity()` sube además en casos concretos: nuclear/CBRN → CRÍTICA, 0-day → CRÍTICA, ransomware + hospital → CRÍTICA, terremoto M≥7.0 → CRÍTICA, sentimiento < −5 en MEDIA → ALTA.

### Correlación entre eventos
`compute_correlations()` combina:
- **Peso de dominio** (`WEIGHTS`: ciberataque=3, conflicto=3, ransomware=3, terremoto=2…).
- **Proximidad espacial** (distancia <5°).
- **Decaimiento temporal** (ventana de 60 min).
- **Entidades compartidas** (bonus hasta +1.0).
- **Score final Tienes razón. Continúo **exactamente** desde `Score final`, sin reiniciar nada.

---

**Score final = peso × (1 + 3 × proximidad) × (0.5 + 0.5 × temporal) × (1 + bonus)**

Solo se guardan correlaciones con `score ≥ 5`.

### Índice de amenaza (JARVIS)
`100 × (1 − exp(−carga_ponderada/hora / 80))`. Saturación suave: 0 = calma, 100 = saturación. Se compara siempre contra la **ventana anterior de igual tamaño**. Niveles: `BAJO` (<25), `MODERADO` (25-49), `ALTO` (50-74), `CRÍTICO` (≥75).

### Relevancia de un evento
`relevance_score()` = 0.40 × severidad + 0.20 × |sentimiento| + 0.15 × entidades + 0.25 × correlaciones, escalado a 0-100. Se usa para ordenar el feed y priorizar los puntos del mapa cuando hay más de `NEXUS_MAP_POINTS`.

### Detecciones del detector de denuncias
Cada mensaje/noticia que menciona un grupo o amenaza se guarda como detección (aunque no tenga ubicación), con:
- **Tipo de ataque** (`ddos`, `ransomware`, `phishing`, `bruteforce`, `malware`, `botnet`, `escaneo`, `filtración`, `exploit`, `infraestructura_critica`, `gobierno`, `militar`, `hackeo`, `ataque`) por palabras clave.
- **Salud / energía** (🏥 / ⚡ en la pestaña Detector).
- **IPs citadas** (se geolocalizan y se guardan en el registro temporal de IPs del grupo; marcadas como «no verificadas: puede ser víctima»).
- **Víctimas** (países citados por banderas, ccTLD de dominios o nombres de país; se excluyen aliados del grupo).

---

## 🗺️ Uso del dashboard

| Atajo | Acción |
|---|---|
| `/` | Enfocar el buscador |
| `r` | Refrescar datos |
| `j` | Abrir/cerrar el panel JARVIS |
| `+` / `-` | Acercar / alejar |
| `0` | Restablecer vista |
| `n` | Siguiente alerta crítica/alta |
| `c` | Mostrar/ocultar ciudades |
| `Esc` | Cerrar JARVIS |

- **Clic en un evento del feed** → centra el mapa en su ubicación.
- **Clic en una leyenda de dominio** → filtra por ese dominio.
- **Clic en un país (pestaña Países)** → filtra y centra.
- **Clic en una fila de grupo (pestaña Grupos o Detector)** → filtra el mapa solo por ese grupo (IPs).
- **Pestaña IOC** → pega IP/dominio/hash/CVE (acepta formato _defangeado_ `hxxp://ejemplo[.]com`) y obtiene coincidencias en la BD + enlaces a VirusTotal, AbuseIPDB, Shodan, urlscan, NVD…
- **Buscador de IP (JARVIS)** → escribe una IP y pulsa Enter (o `📡 Mi IP pública`) para saber si está en eventos, listas de grupos o detecciones. **Ojo:** las fuentes suelen listar IPs *origen* de ataques; que aparezca no significa que seas víctima, puede significar que tu IP (o un dispositivo de tu red) está señalada como emisora.
- **Menú Exportar ▾** → CSV, JSON, NDJSON, GeoJSON, KML, Excel, Markdown, informe HTML, lista de IPs, IPs de grupos (CSV/JSON), paquete ZIP. Los enlaces llevan **los filtros actuales** del panel.
- **Barra "Barrido auto"** → `Manual` / 3 min / 5 min / 15 min / 1 h / 1 día. Se guarda en la BD (`app_kv`) y se aplica en el servidor; al acabar cada barrido el panel se refresca solo.
- **Botón 🗑 Eliminar datos** → modal que exige escribir `BORRAR`. Borra eventos no protegidos, correlaciones, anomalías, barridos, salud de fuentes y candidatos. **Conserva**: intel de cibercrimen (según `NEXUS_KEEP_CYBER`), IPs de grupos, detecciones, nombres de grupos, caché de geolocalización, ajustes y auditoría.
- **Botón ⏻** → apaga NEXUS y libera el puerto.
- **Botón 🌐 ES/EN** → conmutador de idioma que se guarda en `localStorage`.

---

## 🧠 Panel JARVIS

Overlay de análisis global (`j` o botón **JARVIS**), con ventana propia (1 h / 6 h / 24 h / 3 d / 7 d / 15 d / 1 mes / 3 meses). Se refresca solo cada 30 s.

- **Índice de amenaza** 0-100 con aguja tipo radar, comparación vs. ventana previa y nivel (BAJO/MODERADO/ALTO/CRÍTICO).
- **KPIs**: C2/botnets, malware, DDoS, fuerza bruta, exploits/0-day, ransomware, phishing, vulnerabilidades KEV, IPs únicas, crimen, conflicto, críticos — cada uno con su delta vs. ventana anterior.
- **Actividad por familia** (Ciber, Crimen, Conflicto, Naturaleza, Economía, Mundo): área apilada + indicadores (total, ritmo/h, hora pico, críticos, país y fuente líderes) + chips por dominio clicables.
- **Tácticas MITRE ATT&CK** en radar polar + **técnicas más vistas** (clic → filtra el mapa).
- **Familias** en anillos concéntricos con brillo.
- **Países en riesgo** y **fuentes más activas** (barras).
- **Qué ha cambiado** vs. ventana anterior (mayores subidas/bajadas por dominio).
- **Corredores de ciberataque** reales (origen → víctima, con dominio y nº de eventos).
- **Grupos activos** (eventos + IPs frescas; clic → mapa filtrado por ese grupo).
- **Secciones temáticas** (Terrorismo, Revueltas callejeras, Crimen urbano, Cripto): total, delta vs. ventana anterior, severidades, países con más actividad y últimos eventos clicables.
- **Criptomonedas · top 10** por capitalización (CoinGecko → CoinPaprika), con precio, cambio 24 h, 1 h y 7 d; se actualiza cada 30 s (caché 2 min).
- **Alertas recientes** (solo CRÍTICA/ALTA, con fuente y título).
- **Buscador de IP** (ver arriba) con enlaces a eventos en el mapa.
- **Paneles temáticos de la ventana** (Ciber, Naturaleza, Economía, Conflicto, Crimen): área apilada por dominio + indicadores + chips.

---

## 🔌 API

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/kpis` | Contadores de la ventana actual (severidad ignora el filtro de severidad; dominio ignora el de dominio) |
| `GET` | `/api/map` | JSON compacto para deck.gl (puntos, correlaciones, flujos reales, destino de arcos) |
| `GET` | `/api/events` | Eventos filtrables |
| `GET` | `/api/correlations` | Correlaciones por score |
| `GET` | `/api/anomalies` | Anomalías |
| `GET` | `/api/stats` | Estadísticas globales |
| `GET` | `/api/search` | Búsqueda facetada (`q`, `entity`, `min_relevance`…) |
| `GET` | `/api/entities` | Top entidades |
| `GET` | `/api/trends` | Tendencias por dominio |
| `GET` | `/api/countries` | Ranking de riesgo por país |
| `GET` | `/api/ioc` | Clasificar y buscar IOC (IP/dominio/URL/hash/CVE/texto) |
| `GET` | `/api/attack` | Técnicas ATT&CK más vistas |
| `GET` | `/api/analytics` | Datos completos del panel JARVIS |
| `GET` | `/api/crypto` | Top 10 cripto (CoinGecko/CoinPaprika), con `stale` si la caché es vieja |
| `GET` | `/api/health` | Estado de fuentes y circuit breakers |
| `GET` | `/api/sweep` | Lanza barrido y **espera** al resultado (bloqueante; el panel usa `/api/sweep/start`) |
| `GET` | `/api/sweep/status` | Estado del barrido (`running`, `last_result`, `last_error`, errores) |
| `GET` | `/api/sweep/interval` | Intervalo actual y opciones válidas (`0,3,5,15,60,1440`) |
| `POST` | `/api/sweep/interval` | Cambiar intervalo (form: `minutes`) — guarda en `app_kv` |
| `POST` | `/api/sweep/start` | Lanzar barrido en segundo plano (devuelve `started` / `already_running`) |
| `POST` | `/api/circuit/reset` | Reiniciar circuit breakers |
| `POST` | `/api/admin/reset` | Borrar datos (exige JSON `{"confirm":"BORRAR"}`); conserva intel de cibercrimen y grupos |
| `GET` | `/api/watchlist` | Ver watchlist |
| `POST` | `/api/watchlist/add` | Añadir (form: `kind`, `value`) |
| `POST` | `/api/watchlist/remove` | Quitar (form: `kind`, `value`) |
| `POST` | `/api/token` | JWT (form: `username`, `password`) |
| `GET` | `/api/group_ips` | IPs atribuidas a grupos (`group`, `limit`, `hist=0/1`) + resumen por grupo |
| `GET` | `/api/threat_groups` | Grupos activos (`hours`) |
| `GET` | `/api/groups` | Modos temáticos (`DOMAIN_GROUPS`) y dominios del mapa |
| `GET` | `/api/detector` | Detecciones + estado del monitor DDoS + IPs por grupo |
| `POST` | `/api/detector/scan` | Lanzar escaneo de canales + feeds + monitor DDoS (en segundo plano) |
| `GET` | `/api/corr_related` | Eventos concretos que forman una correlación (mismos dominios/fuentes, radio `CORR_MAX_DIST_DEG`) |
| `GET` | `/api/ip_check` | ¿Está esta IP en eventos / listas de grupos / detecciones? + avisos |
| `GET` | `/api/myip` | IP pública de la máquina donde corre NEXUS |
| `GET` | `/api/artifacts` | URLs, hashes, IPs y CVEs extraídos de un texto |
| `GET` | `/export/{fmt}` | Exportaciones (12 formatos + `zip`) |
| `POST` | `/api/shutdown` | Apagar NEXUS y liberar el puerto |
| `WS` | `/ws` | Actualizaciones en vivo (`sweep_start`, `sweep`, `reset`) |

Auth: `Authorization: Bearer <jwt>` o HTTP Basic. Desde `127.0.0.1` sin proxy el dashboard no pide login (`NEXUS_LOCAL_NOAUTH=1`), pero `POST /api/sweep/start`, `/api/circuit/reset`, `/api/admin/reset`, `/api/detector/scan`, `/api/shutdown` y los `watchlist/*` siguen exigiendo `require_user_or_local` (loopback válido o auth).

Formatos de export (`/export/{fmt}`): `csv`, `json`, `ndjson`, `geojson`, `kml`, `markdown`, `html`, `xlsx` (requiere `openpyxl`), `ips`, `grupos_csv`, `grupos_json`, `zip`. Parámetros: `hours`, `domain`, `group`, `severity`, `q`, `limit`, `hist` (para grupos).

---

## 🤖 Bot de Telegram (⚠️ sin probar)

> ⚠️ **NO se ha probado.** El código está escrito, pero no se ha ejecutado de principio a fin. **No se sabe si funciona.** **Se arreglará otro día.** Mientras tanto, el resto del sistema funciona sin él: si no defines `TELEGRAM_BOT_TOKEN`, el bot no arranca y todo lo demás sigue igual.

Comandos previstos: `/start`, `/help`, `/brief`, `/sweep`, `/stats`, `/top`, `/health`, `/anomalies`, `/export`, `/search <q>`, `/domains`, `/trends`, `/watch`.

Detalles de implementación que sí están en el código:
- Se registran `CommandHandler` para esos comandos y un `CallbackQueryHandler` que enruta los botones inline (`cmd:brief`, `cmd:stats`, `cmd:top`, `cmd:sweep`, `cmd:health`, `cmd:export`, `cmd:trends`, `cmd:watch`).
- `tg_send()` envía con `Markdown` legacy y, si falla, reintenta en texto plano (sin `parse_mode`).
- `_md_escape()` / `_md_unescape()` escapan `_ * ` [` para no romper el `parse_mode`.
- Las alertas (`dispatch_alerts`) solo mandan **C2 nuevos** (`_new`), **DDoS/malware nuevos** ALTA/CRÍTICA (excluyendo Feodo, que ya va aparte), **anomalías** y **top 3 correlaciones** con un teclado inline.
- `cmd_export` usa `export_csv_path()` (CSV de las últimas 24 h) y lo envía como documento.
- `start_tg()` solo se ejecuta si hay `TELEGRAM_TOKEN`; en `lifespan` se hace `initialize` → `start` → `updater.start_polling`, y al cerrar `updater.stop` → `stop` → `shutdown`.

Requiere `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` en `.env`. Si lo pruebas y falla, abre un issue con:
- Comando usado.
- Salida del log (`nexus.log`).
- Versión de Python.

**Nota:** el bot está en la lista de tareas pendientes. **Hay que descansar.** Se arreglará cuando haya tiempo.

---

## 🧱 Arquitectura

```
nexus.py
├── §0     Configuración global + caché TTL + circuit breaker + User-Agent rotativo + redacción de secretos
├── §0.bis Helpers generales (_num, _str, _records)
├── §1     Auth (JWT + Basic + bypass loopback con Host/Origin/Sec-Fetch-Site)
├── §2     Caché TTL + circuit breaker (5 fallos → 5 min pausada)
├── §3     SQLite (schema, migración, queries, retención, DB_WRITE_LOCK, app_kv, group_ips, group_detections, audit_log)
├── §4     Geolocalización multi-proveedor (GeoLite2 → ip-api /batch → geojs, caché en disco)
├── §5     Texto: sentimiento, países (tabla ISO2 + alias ES/EN), ciudades, entidades, tags
├── §5.bis Enriquecimiento: dedupe SimHash, escalado de severidad, watchlist, tendencias, artifacts
├── §6     Colectores (~110 fuentes, cada una degrada sola; grupos, detector de denuncias, monitor DDoS, prensa, cripto)
├── §7     Correlación (clustering espacial + decaimiento temporal + entidades compartidas)
├── §8     Anomalías (z-score por dominio)
├── §8.bis Anomalías avanzadas (entidad nueva, ráfaga CRITICA, sentimiento negativo)
├── §9     LLM (3 prompts + caché)
├── §10    Telegram + alertas
├── §11    Exportación
├── §12    Orquestación de barrido (serializado, deadline suave, ingestión tardía)
├── §13    Payload del mapa (JSON compacto, palette, flujos)
├── §14    Frontend (HTML/CSS/JS + NeuralNet + deck.gl + JARVIS + mapa base CARTO + i18n ES/EN)
└── §15    FastAPI (rutas, parciales, API, WebSocket, lifespan)
```

**Decisiones de diseño**

- **El mapa no se genera con pydeck en iframe.** El servidor entrega JSON compacto (`/api/map`) y el navegador mantiene _una sola_ instancia de deck.gl; cambiar filtros no recrea WebGL. La cámara la guarda el cliente (`MAP.vs.globe` / `MAP.vs.flat`) y nunca "vuelve atrás" al refrescar.
- **Fuentes que degradan solas.** Cada colector puede lanzar excepciones: `run_source()` las captura, registra y alimenta el circuit breaker. Sin clave → `[]`. Si el temporizador salta tarde (>timeout+3 s) se marca como «bloqueo local» y **no** cuenta como fallo de la fuente.
- **Migración automática de la BD.** Si la tabla `events` no tiene `entities`/`tags`, se añaden con `ALTER TABLE` al arrancar. También se crea el índice único de `raw_hash` si faltaba.
- **Ubicación honesta.** Si un texto no menciona país/ciudad, el evento se descarta (no se inventan coordenadas). Los centroides se _jitterizan_ de forma determinista (hash MD5 del texto) para que 40 noticias del mismo país no se apilen.
- **Arcos solo con dos extremos.** Solo se dibuja flujo si el evento lleva `flow:XX>YY` (Cloudflare Radar, noticias atribuidas, feeds de grupos con víctima). Conflictos, crimen, naturaleza, economía, cripto **nunca** dibujan arcos.
- **IPs de grupos temporales.** Registro en `group_ips` con retención (`NEXUS_GROUP_IP_KEEP_DAYS`, 30 d) y tope por grupo (`NEXUS_GROUP_IP_CAP`, 1500). Las de listas históricas no se "refrescan" solas; solo las vistas en vivo (`live_seen`).
- **Anti falsos positivos en el detector.** Descarta noticias que *hablan* de un grupo (atribuciones, "según investigadores…") y ataques de un grupo a su aliado (`_allied`, `_ALLIED_PAIRS`).
- **Serialización de escrituras.** `_DB_WRITE_LOCK` + reintento con `busy_timeout` 20 s: el barrido y el detector no se pisan.
- **Single-instance.** Lock en `nexus.db.lock` (`fcntl.flock`): si otro NEXUS usa la misma BD, avisa en el log con «¡OTRO NEXUS YA ESTÁ USANDO ESTA MISMA BASE DE DATOS!».
- **Watchdog de event loop.** Si el servidor se bloquea >2 s, lo avisa en el log (así se ve qué lo cuelga: barrido, BD, etc.).
- **Barrido serializado con deadline suave.** Las fuentes lentas (GDELT crimen ≥40 s por el límite de 1 consulta/5 s) siguen en segundo plano y se incorporan con `_ingest_late` al terminar, sin retrasar el resto.

---

## 🩺 Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| El mapa sale vacío | No hay eventos en la ventana o el barrido no ha corrido | Pulsa **⚡ Barrido** o amplía la ventana a 24h/7d |
| "Mapa 2D de reserva" | WebGL deshabilitado o deck.gl no cargó desde CDN | Activa WebGL o sirve deck.gl localmente (`NEXUS_DECK_URL`) |
| Una fuente da 0 eventos | Falta API key o no se pudo geolocalizar | Revisa `.env` y la pestaña **🩺 Fuentes** (🔑 = falta clave) |
| "circuit open" en una fuente | 5 fallos seguidos → pausada 5 min | **🔌 Reiniciar circuit breakers** en la pestaña Fuentes |
| El bot de Telegram no responde | **No está probado; puede no funcionar** | Está en la lista de pendientes. **Se arreglará otro día.** Mientras, usa el dashboard. |
| Error de migración de BD | BD creada con versión anterior | Se migra sola al arrancar; si falla, borra `nexus.db` y reinicia (pierdes histórico) |
| `database is locked` + panel colgado | Dos NEXUS (p. ej. `dg.py` y `nexus.py`) sobre la misma `nexus.db` | Mira el log: «¡OTRO NEXUS YA ESTÁ USANDO ESTA MISMA BASE DE DATOS!». Cierra el otro (`pkill -f nexus.py`; `pkill -f dg.py`) y deja solo uno |
| Puerto 8000 ocupado | Instancia anterior no cerrada | Nexus_Osint_X usa el siguiente libre (8001…8024) y lo dice en el log |
| `sqlite3.IntegrityError` en eventos | Duplicado por `raw_hash` (normal) | Se ignora silenciosamente; no es un error |
| La geolocalización va lenta | `ip-api.com` limita a 15 req/min | Sin `GeoLite2-City.mmdb` es normal; añade el `.mmdb` para ir local |
| El detector de Telegram no avanza | 429 de Telegram (rate limit) | Se reintenta solo; en la pestaña Detector verás «Telegram limitó las peticiones» |
| «Barriendo…» eterno | El barrido tardó más de 90 s (seguro de la UI) | La UI libera sola los controles; si el servidor no responde, mira el log y el watchdog `[RENDIMIENTO]` |

---

## 📁 Estructura del repo

```
.
├── nexus.py                 # Aplicación completa
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
```

Archivos que se crean en runtime (no versionados): `nexus.db`, `nexus.db-wal`, `nexus.db-shm`, `nexus.db.lock`, `.cache/watchlist.json`, `.nexus_jwt_secret`, `GeoLite2-City.mmdb` (opcional, lo pones tú).

---

## ⚠️ Aviso legal y uso responsable

Nexus_Osint_X agrega **fuentes públicas** (feeds de seguridad, agencias gubernamentales, prensa, APIs abiertas). No realiza escaneos activos, no visita URLs de phishing (solo resuelve DNS), no interactúa con infraestructura maliciosa.

Úsalo solo para **investigación defensiva, monitorización de amenazas o docencia**, cumpliendo las leyes de tu jurisdicción y los términos de cada API. El autor no se responsabiliza del uso indebido.

Los indicadores (IPs, hashes, URLs) se muestran _defangeados_ (`hxxp://ejemplo[.]com`) para evitar clics accidentales.

**Este es un prototipo.** No es un producto terminado. Algunas partes (como el bot de Telegram) **no se han probado**. Úsalo bajo tu responsabilidad y no lo despliegues en producción sin revisarlo antes.

---

## 🙏 Créditos

Nexus_Osint_X no sería posible sin el trabajo público de estas organizaciones y proyectos. Todo el mérito de los datos es suyo; los errores de integración son míos.

### Agencias gubernamentales y CERTs
- **FBI** — [Wanted API](https://www.fbi.gov/wanted/api) y [National Press Releases RSS](https://www.fbi.gov/feeds/national-press-releases/rss.xml)
- **INTERPOL** — [Red Notices API pública](https://ws-public.interpol.int/notices/v1/red)
- **CISA** — [Known Exploited Vulnerabilities (KEV)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) y [Cybersecurity Advisories](https://www.cisa.gov/cybersecurity-advisories)
- **GovCERT.ch** (CERT Suiza) — [IPs y CIDR de NoName057(16)](https://github.com/govcert-ch/CTI)
- **US Department of State** — [Travel Advisories RSS](https://travel.state.gov/_res/rss/TAsTWs.xml)
- **US Treasury / OFAC** — [SDN List](https://sanctionslistservice.ofac.treas.gov/)
- **UN Security Council** — [Consolidated Sanctions List](https://main.un.org/securitycouncil/en/content/un-sc-consolidated-list)
- **USGS** — [Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/)
- **NASA** — [EONET](https://eonet.gsfc.nasa.gov/) y [FIRMS](https://firms.modaps.eosdis.nasa.gov/)
- **NOAA** — [Active Weather Alerts](https://api.weather.gov/alerts/active)
- **WHO** — [Disease Outbreak News](https://www.who.int/api/news/diseaseoutbreaknews)
- **ReliefWeb (OCHA)** — [Reports API](https://apidoc.reliefweb.int/)
- **ACLED** — [Armed Conflict Location & Event Data](https://acleddata.com/)
- **FRED (St. Louis Fed)** — [Series API](https://fred.stlouisfed.org/)
- **BLS** — [Public Data API](https://www.bls.gov/developers/)
- **EIA** — [Open Data API](https://www.eia.gov/opendata/)

### Threat intelligence y seguridad
- **abuse.ch** — [Feodo Tracker](https://feodotracker.abuse.ch/), [URLhaus](https://urlhaus.abuse.ch/), [ThreatFox](https://threatfox.abuse.ch/), [SSLBL](https://sslbl.abuse.ch/), [MalwareBazaar](https://bazaar.abuse.ch/)
- **Spamhaus** — [DROP list](https://www.spamhaus.org/drop/)
- **SANS ISC** — [DShield API](https://isc.sans.edu/api/)
- **Blocklist.de** — [API](https://www.blocklist.de/)
- **Emerging Threats** — [Compromised IPs](https://rules.emergingthreats.net/blockrules/compromised-ips.txt)
- **CI Army**, **GreenSnow**, **Binary Defense**, **BruteforceBlocker** — listas de IPs atacantes
- **OpenPhish** — [Public feed](https://openphish.com/)
- **Ransomware.live** y **RansomLook** — [API pública](https://www.ransomware.live/), [RansomLook](https://www.ransomlook.io/)
- **Cloudflare Radar** — [Security & Attacks](https://radar.cloudflare.com/security-and-attacks)
- **SecurityScorecard** — [KillNet DDoS Blocklist](https://github.com/securityscorecard/SSC-Threat-Intel-IoCs)
- **MITRE ATT&CK** — [Framework](https://attack.mitre.org/)
- **OpenSanctions** — [API](https://www.opensanctions.org/api/)

### Datos abiertos de crimen urbano
- **Chicago Police Department** — [Open Data Portal](https://data.cityofchicago.org/)
- **NYPD** — [NYC Open Data](https://data.cityofnewyork.us/)
- **San Francisco Police Department** — [SF Open Data](https://data.sfgov.org/)
- **Los Angeles Police Department** — [LA Open Data](https://data.lacity.org/)
- **Seattle**, **Baltimore** — portales de datos abiertos

### Medios y prensa
- BBC (Mundo, Europa, África, Asia, Latinoamérica, Oriente Medio), The Guardian, Al Jazeera, DW, France 24, RFI, NPR, NYT, CNN, Sky News, Euronews, ABC Australia, The Hindu, Japan Times, SCMP, UN News, El País (Internacional y América), El Mundo, La Vanguardia, elDiario.es, 20minutos, Europa Press, El Correo, Deia, RTVE, Infobae, Le Monde, Le Figaro, Der Spiegel, Tagesschau, ANSA, La Repubblica, Clarín
- **GDELT Project** — [DOC y GEO APIs](https://www.gdeltproject.org/)
- **Wikipedia** — [Portal:Current events](https://en.wikipedia.org/wiki/Portal:Current_events)
- **InSight Crime**, **DOJ Press Releases**, **Krebs on Security**, **BleepingComputer**, **The Hacker News**, **The Record**, **SecurityWeek**, **DarkReading**, **Malwarebytes**
- **Google News RSS** (búsquedas de disturbios y crimen urbano en 6 idiomas)

### Cripto
- **CoinGecko** y **CoinPaprika** — precios y variaciones

### Tecnología
- **deck.gl** — visualización 3D
- **FastAPI** + **Uvicorn** — backend
- **Natural Earth** — datos geográficos (países en `ne_110m_admin_0_countries.geojson`)
- **CARTO** — mapas base (`basemaps.cartocdn.com`), © OpenStreetMap · © CARTO
- **Jinja2**, **Chart.js**, **httpx**, **feedparser**, **APScheduler**, **passlib**, **PyJWT**
- **OpenAI** — LLM opcional
- **Telegram Bot API**

### Agradecimiento especial
A **GovCERT.ch** por publicar abiertamente las IPs y rangos de NoName057(16), y a **SecurityScorecard** por la lista de proxies de Killnet. Sin su transparencia, este proyecto no tendría la capa de grupos que tiene.

Si eres responsable de una de estas fuentes y quieres que ajuste la atribución, abre un issue.

---

## 📄 Licencia

MIT — ver LICENSE.

---

## 💤 Nota final

Este es un **prototipo** hecho con el tiempo y los medios disponibles. **Hice todo lo que pude** con lo que tenía, priorizando que el núcleo funcionara antes que los extras.

**El bot de Telegram no se ha probado** y **no se sabe si funciona**. **Se arreglará otro día. Hay que descansar.**

Si algo no funciona, abre un issue con el log y la versión. Si algo funciona, disfrútalo. Si algo falla y sabes arreglarlo, manda un PR.

Gracias por pasarte. Deja una estrella si te gustó el proyecto.

- Condor2026
