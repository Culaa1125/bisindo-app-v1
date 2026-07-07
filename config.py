"""
config.py
-------------
Semua konfigurasi aplikasi BISINDO
"""

from pathlib import Path

# ======================================================
# PROJECT ROOT
# ======================================================
BASE_DIR = Path(__file__).resolve().parent

# ======================================================
# MODEL PATH
# ======================================================
MODEL_DIR = BASE_DIR / "models"
CNN_MODEL_PATH = MODEL_DIR / "model_cnn_abjad.keras"
LSTM_MODEL_PATH = MODEL_DIR / "best_bisindo_lstm_4200dataset.keras"

# ======================================================
# LABEL PATH
# ======================================================
LABEL_DIR = BASE_DIR / "labels"
CNN_LABEL_PATH = LABEL_DIR / "label_abjad.json"
LSTM_LABEL_PATH = LABEL_DIR / "label_map.json"

# ======================================================
# LSTM
# ======================================================
SEQUENCE_LENGTH = 30
LANDMARK_VECTOR_SIZE = 258

# ======================================================
# CNN
# ======================================================
CNN_INPUT_SIZE = 126
CNN_MAX_HANDS = 2

# ======================================================
# CONFIDENCE
# ======================================================
CNN_THRESHOLD = 0.80
LSTM_THRESHOLD = 0.80

# ======================================================
# MEDIAPIPE
# ======================================================
MODEL_COMPLEXITY = 1
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
ENABLE_SEGMENTATION = False
SMOOTH_SEGMENTATION = False
REFINE_FACE_LANDMARKS = False
SMOOTH_LANDMARKS = True

# ======================================================
# DRAWING
# ======================================================
FONT_SCALE = 0.8
FONT_THICKNESS = 2
TEXT_COLOR = (255,255,255)
BOX_COLOR = (20,20,20)
FPS_POSITION = (20,35)
PRED_POSITION = (20,70)
CONF_POSITION = (20,105)
MODE_POSITION = (20,140)
MAX_HISTORY = 100