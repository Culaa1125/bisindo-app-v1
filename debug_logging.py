"""
debug_logging.py
------------------------------------
Aktifkan logging DEBUG untuk aiortc & aioice supaya kelihatan
persis di log Streamlit Cloud:
- kandidat apa saja yang berhasil di-gather di sisi SERVER
  (host / srflx / relay-udp / relay-tcp / relay-tls)
- hasil connectivity check tiap pasangan kandidat (succeeded/failed)
- kapan TURN allocate dikirim & apakah dapat balasan

Cara pakai: panggil enable_webrtc_debug_logging() SEKALI, di baris
paling atas bisindo_app.py, SEBELUM import streamlit_webrtc / rtc_config.
"""

import logging
import sys


def enable_webrtc_debug_logging():
    fmt = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt))

    # aiortc: level tinggi (ICE state, DTLS, dsb)
    # aioice: level rendah (STUN/TURN request-response mentah)
    for logger_name in ("aiortc", "aioice"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        # Hindari duplikasi handler kalau Streamlit rerun berkali-kali
        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            logger.addHandler(handler)
        logger.propagate = False
