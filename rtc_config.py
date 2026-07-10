"""
rtc_config.py
------------------------------------
RTC Configuration
Mendukung:
- Lokal
- Streamlit Cloud
- Hugging Face Spaces
- Metered TURN
"""

import os
import streamlit as st

# ======================================================
# DEFAULT STUN (fallback)
# ======================================================
DEFAULT_STUN = "stun:stun.l.google.com:19302"


def _get_secret(key):
    """
    Ambil secret dari st.secrets (Streamlit Cloud, via
    .streamlit/secrets.toml) jika tersedia, jika tidak
    fallback ke environment variable (Hugging Face Spaces
    "Repository secrets" diekspos sebagai env var).
    """
    try:
        # st.secrets akan raise error jika file secrets.toml
        # tidak ada sama sekali (bukan hanya KeyError), jadi
        # dibungkus try/except Exception di sini.
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return os.environ.get(key)


# ======================================================
# LOAD SECRETS
# ======================================================
STUN_URL = _get_secret("STUN_URL") or DEFAULT_STUN
TURN_URL = _get_secret("TURN_URL")
TURN_TLS_URL = _get_secret("TURN_TLS_URL")
USERNAME = _get_secret("METERED_USERNAME")
PASSWORD = _get_secret("METERED_CREDENTIAL")

# ======================================================
# ICE SERVERS
# ======================================================
ice_servers = [
    {
        "urls": [STUN_URL]
    }
]

# Tambahkan TURN jika tersedia
if USERNAME and PASSWORD:
    ice_servers.append(
        {
            "urls": [
                TURN_URL,
                TURN_TLS_URL
            ],
            "username": USERNAME,
            "credential": PASSWORD
        }
    )

RTC_CONFIGURATION = {
    "iceServers": ice_servers,
    "iceTransportPolicy": "all",
}
