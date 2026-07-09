"""
rtc_config.py
------------------------------------
RTC Configuration
Mendukung:
- Lokal
- Streamlit Cloud
- Metered TURN (UDP / TCP / TLS)
"""

import json
import streamlit as st

# ======================================================
# DEFAULT STUN (fallback)
# ======================================================
DEFAULT_STUN = "stun:stun.l.google.com:19302"

# ======================================================
# LOAD SECRETS (per-key, tidak all-or-nothing)
# ======================================================
# PENTING: st.secrets HANYA membaca file .streamlit/secrets.toml lokal.
# Saat deploy ke Streamlit Community Cloud, secrets HARUS di-paste ulang
# secara manual di: App -> Settings -> Secrets (secrets.toml tidak ikut
# ke GitHub / tidak otomatis ter-deploy).

def _get_secret(key, default=None):
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return default

STUN_URL = _get_secret("STUN_URL", DEFAULT_STUN)
USERNAME = _get_secret("METERED_USERNAME")
PASSWORD = _get_secret("METERED_CREDENTIAL")

# Opsi A (disarankan): paste seluruh JSON "iceServers" dari dashboard
# Metered ke satu secret bernama TURN_ICE_SERVERS_JSON, contoh:
#   TURN_ICE_SERVERS_JSON = '''
#   [
#     {"urls": "stun:stun.relay.metered.ca:80"},
#     {"urls": "turn:standard.relay.metered.ca:80", "username": "...", "credential": "..."},
#     {"urls": "turn:standard.relay.metered.ca:80?transport=tcp", "username": "...", "credential": "..."},
#     {"urls": "turn:standard.relay.metered.ca:443", "username": "...", "credential": "..."},
#     {"urls": "turns:standard.relay.metered.ca:443?transport=tcp", "username": "...", "credential": "..."}
#   ]
#   '''
# Ini paling aman karena kamu tidak perlu menebak-nebak format/port TURN,
# tinggal copy-paste persis apa yang diberikan Metered.
_raw_json = _get_secret("TURN_ICE_SERVERS_JSON")

# Opsi B (lama/manual): TURN_URLS berupa string dipisah koma.
_raw_turn_urls = _get_secret("TURN_URLS")
# Kompatibilitas dengan skema lama (TURN_URL + TURN_TLS_URL terpisah)
_legacy_turn_url = _get_secret("TURN_URL")
_legacy_turn_tls_url = _get_secret("TURN_TLS_URL")

# ======================================================
# BANGUN ICE SERVERS
# ======================================================
ice_servers = [{"urls": [STUN_URL]}]
turn_loaded = False
turn_load_error = None

if _raw_json:
    try:
        parsed = json.loads(_raw_json)
        if isinstance(parsed, list) and len(parsed) > 0:
            ice_servers = parsed  # replace sepenuhnya, JSON dari Metered sudah lengkap
            turn_loaded = any(
                any(
                    "turn:" in u or "turns:" in u
                    for u in (
                        server.get("urls")
                        if isinstance(server.get("urls"), list)
                        else [server.get("urls", "")]
                    )
                )
                for server in ice_servers
            )
    except json.JSONDecodeError as e:
        turn_load_error = f"TURN_ICE_SERVERS_JSON tidak valid JSON: {e}"

elif USERNAME and PASSWORD:
    turn_urls = []

    if _raw_turn_urls:
        turn_urls = [u.strip() for u in _raw_turn_urls.split(",") if u.strip()]
    else:
        # fallback ke skema lama
        turn_urls = [u for u in (_legacy_turn_url, _legacy_turn_tls_url) if u]

    if turn_urls:
        ice_servers.append(
            {
                "urls": turn_urls,
                "username": USERNAME,
                "credential": PASSWORD,
            }
        )
        turn_loaded = True

RTC_CONFIGURATION = {
    "iceServers": ice_servers,
    # Untuk DEBUG: set "relay" sementara supaya browser dipaksa
    # hanya lewat TURN. Kalau kamera tetap tidak connect walau
    # "relay", berarti kredensial/kuota TURN yang bermasalah, bukan
    # firewall STUN. Setelah dites, kembalikan ke "all".
    "iceTransportPolicy": "relay",
}

# Diekspor supaya bisa ditampilkan di sidebar/debug expander
TURN_LOADED = turn_loaded
TURN_LOAD_ERROR = turn_load_error
