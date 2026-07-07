"""
rtc_config.py
------------------------------------
RTC Configuration
Mendukung:
- Lokal
- Streamlit Cloud
- Metered TURN
"""

import streamlit as st

# ======================================================
# DEFAULT STUN (fallback)
# ======================================================
DEFAULT_STUN = "stun:stun.l.google.com:19302"

# ======================================================
# LOAD SECRETS
# ======================================================
try:
    STUN_URL = st.secrets["STUN_URL"]
    TURN_URL = st.secrets["TURN_URL"]
    TURN_TLS_URL = st.secrets["TURN_TLS_URL"]
    USERNAME = st.secrets["METERED_USERNAME"]
    PASSWORD = st.secrets["METERED_CREDENTIAL"]

except KeyError:
    STUN_URL = DEFAULT_STUN
    TURN_URL = None
    TURN_TLS_URL = None
    USERNAME = None
    PASSWORD = None

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
    "iceServers": ice_servers
}