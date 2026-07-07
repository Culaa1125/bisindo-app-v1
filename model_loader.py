"""
model_loader.py
------------------------------------
Load semua model AI dan label.
Menggunakan cache Streamlit agar model hanya dimuat sekali.
"""

import json
import streamlit as st
import tensorflow as tf

from config import (
    CNN_MODEL_PATH,
    LSTM_MODEL_PATH,
    CNN_LABEL_PATH,
    LSTM_LABEL_PATH,
)


class ModelManager:
    """
    Menyimpan semua model AI beserta labelnya.
    """
    def __init__(self):
        self.cnn_model = None
        self.lstm_model = None
        self.cnn_labels = {}
        self.lstm_labels = {}

    def load(self):
        """
        Load seluruh model dan label.
        """
        if self.cnn_model is None:
            self.cnn_model = tf.keras.models.load_model(
                CNN_MODEL_PATH,
                compile=False
            )

        if self.lstm_model is None:
            self.lstm_model = tf.keras.models.load_model(
                LSTM_MODEL_PATH,
                compile=False
            )

        if not self.cnn_labels:
            with open(CNN_LABEL_PATH, "r", encoding="utf-8") as f:
                self.cnn_labels = json.load(f)

        if not self.lstm_labels:
            with open(LSTM_LABEL_PATH, "r", encoding="utf-8") as f:
                self.lstm_labels = json.load(f)

        return self

    def get_cnn(self):
        return self.cnn_model

    def get_lstm(self):
        return self.lstm_model

    def get_cnn_labels(self):
        return self.cnn_labels

    def get_lstm_labels(self):
        return self.lstm_labels


@st.cache_resource(show_spinner="Loading AI Models...")
def load_models():
    return ModelManager().load()