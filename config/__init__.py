# config/__init__.py

import os

# --- Konfigurasi Direktori ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_DIR = os.path.join(BASE_DIR, "chat_sessions")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploaded_files")
EXPORT_DIR = os.path.join(BASE_DIR, "exported_files")
USERS_DIR = os.path.join(BASE_DIR, "user_data")
USERS_FILE = os.path.join(USERS_DIR, "users.json")
FONT_DIR = os.path.join(BASE_DIR, "fonts")

# --- Konfigurasi Aplikasi ---
LOGO_PATH = os.getenv("LOGO_IKM", os.path.join(BASE_DIR, "logo_ikm.jpg"))
WATERMARK_TEXT = os.getenv("CHATBOT_WATERMARK_TEXT", "IKM Besut")

# --- Konfigurasi Ollama ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_OLLAMA_MODEL = os.getenv("DEFAULT_OLLAMA_MODEL", "STEMBot-4B")

# --- Fungsi untuk memastikan direktori wujud ---
def setup_directories():
    """Memastikan semua direktori yang diperlukan wujud."""
    os.makedirs(HISTORY_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(EXPORT_DIR, exist_ok=True)
    os.makedirs(USERS_DIR, exist_ok=True)
    os.makedirs(FONT_DIR, exist_ok=True)
