"""
processor_TEST_no_inference.py
------------------------------------
VERSI TES SEMENTARA untuk mendiagnosis apakah beban CPU dari
MediaPipe + TensorFlow adalah penyebab koneksi WebRTC terus-menerus
reset sebelum sempat connect.

CARA PAKAI:
1. Backup processor.py asli kamu (jangan dihapus).
2. Rename file ini jadi processor.py (menimpa sementara).
3. Push, redeploy, coba nyalakan kamera.

HASIL YANG DICARI:
- Kalau kamera JADI BISA connect & stabil (walau tanpa deteksi
  BISINDO, cuma nampilin video mentah) -> TERBUKTI CPU/beban
  inference adalah penyebabnya. Lanjut ke langkah optimasi model.
- Kalau kamera TETAP gagal connect (masih ada error yang sama
  persis) -> berarti bukan soal CPU/inference, ada faktor lain
  yang perlu digali lagi.

SETELAH SELESAI TES: kembalikan processor.py yang asli.
"""

import av
import time
import threading

from streamlit_webrtc import VideoProcessorBase


class BISINDOProcessor(VideoProcessorBase):

    def __init__(self):
        self._lock = threading.Lock()
        self.last_time = time.time()
        self.fps = 0

        # Dummy state supaya bisindo_app.py tidak error saat
        # memanggil update_settings() / get_result()
        self.stable_prediction = ""
        self.result_mode = ""
        self.confidence = 0.0
        self.motion_score = 0.0
        self.state = "TEST_NO_INFERENCE"

        self.conf_cnn = 0.80
        self.conf_lstm = 0.80
        self.motion_low = 0.005
        self.motion_high = 0.015

    def update_settings(self, conf_cnn, conf_lstm, motion_low, motion_high):
        self.conf_cnn = conf_cnn
        self.conf_lstm = conf_lstm
        self.motion_low = motion_low
        self.motion_high = motion_high

    def calculate_fps(self):
        current = time.time()
        delta = current - self.last_time
        if delta > 0:
            self.fps = 1 / delta
        self.last_time = current

    def recv(self, frame):
        # TIDAK ADA MediaPipe, TIDAK ADA TensorFlow di sini sama
        # sekali. Cuma lewatkan frame mentah + hitung FPS.
        image = frame.to_ndarray(format="bgr24")
        self.calculate_fps()
        return av.VideoFrame.from_ndarray(image, format="bgr24")

    def get_result(self):
        with self._lock:
            return {
                "prediction": self.stable_prediction,
                "mode": self.result_mode,
                "confidence": self.confidence,
                "motion": self.motion_score,
                "state": self.state,
                "fps": self.fps,
                "has_prediction": False,
            }

    def __del__(self):
        pass
