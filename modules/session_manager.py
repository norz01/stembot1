# modules/session_manager.py

import streamlit as st
import os
import json
from datetime import datetime
from config import HISTORY_DIR, DEFAULT_OLLAMA_MODEL

def get_user_history_dir(username):
    """Mendapatkan direktori sejarah untuk pengguna tertentu dan membinanya jika belum wujud."""
    user_dir = os.path.join(HISTORY_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def save_chat_session(username, session_id, history):
    """Menyimpan sejarah perbualan ke fail JSON."""
    user_history_dir = get_user_history_dir(username)
    filepath = os.path.join(user_history_dir, f"{session_id}.json")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except IOError as e:
        st.error(f"Gagal menyimpan sesi '{session_id}': {e}")

def load_chat_session(username, session_id):
    """Memuatkan sejarah perbualan dari fail JSON."""
    filepath = os.path.join(get_user_history_dir(username), f"{session_id}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, IOError) as e:
        st.error(f"Gagal memuatkan sesi '{session_id}': {e}")
        return []

def load_all_session_ids(username):
    """Memuatkan dan menyusun semua ID sesi untuk pengguna."""
    user_history_dir = get_user_history_dir(username)
    try:
        if not os.path.exists(user_history_dir):
            return []
        files = [f.replace(".json", "") for f in os.listdir(user_history_dir) if f.endswith(".json")]
        
        def sort_key(filename):
            try:
                # Format dijangka: YYYYMMDD_HHMMSS
                return datetime.strptime(filename, "%Y%m%d_%H%M%S")
            except ValueError:
                # Jika format tidak sepadan, letakkan di akhir
                return datetime.min
        
        return sorted(files, key=sort_key, reverse=True)
    except OSError as e:
        st.error(f"Gagal membaca direktori sesi: {e}")
        return []

def delete_chat_session_file(username, session_id):
    """Memadam fail sesi perbualan tunggal."""
    filepath = os.path.join(get_user_history_dir(username), f"{session_id}.json")
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            st.success(f"Sesi '{session_id}' berjaya dipadam.")
            return True
        else:
            st.warning(f"Fail sesi '{session_id}' tidak ditemui.")
            return False
    except OSError as e:
        st.error(f"Gagal memadam sesi '{session_id}': {e}")
        return False

def delete_all_chat_sessions(username):
    """Memadam semua sesi perbualan untuk pengguna."""
    user_history_dir = get_user_history_dir(username)
    # ... (Kod asal anda untuk fungsi ini sudah baik, boleh disalin terus)
    # ... (Saya sertakan di sini untuk kelengkapan)
    deleted_count = 0
    errors = []
    try:
        if not os.path.exists(user_history_dir):
            st.info("Tiada sesi untuk dipadam.")
            return True
        for filename in os.listdir(user_history_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(user_history_dir, filename)
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except OSError as e:
                    errors.append(f"Gagal memadam {filename}: {e}")
        if errors:
            for error in errors: st.error(error)
        if deleted_count > 0:
            st.success(f"{deleted_count} sesi berjaya dipadam.")
        else:
            st.info("Tiada sesi ditemui untuk dipadam.")
        return True
    except OSError as e:
        st.error(f"Gagal mengakses direktori sesi: {e}")
        return False


def initialize_session_state(available_models):
    """Memulakan pembolehubah keadaan sesi jika belum wujud."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = "new"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_filename_prefix" not in st.session_state:
        st.session_state.current_filename_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
    if "selected_ollama_model" not in st.session_state:
        if available_models and DEFAULT_OLLAMA_MODEL in available_models:
            st.session_state.selected_ollama_model = DEFAULT_OLLAMA_MODEL
        elif available_models:
            st.session_state.selected_ollama_model = available_models[0]
        else:
            st.session_state.selected_ollama_model = DEFAULT_OLLAMA_MODEL
    # ... (Teruskan untuk kunci keadaan sesi yang lain seperti 'show_confirm_delete_all_button', dll.)
    if "show_confirm_delete_all_button" not in st.session_state:
        st.session_state.show_confirm_delete_all_button = False
    if "chat_page_num" not in st.session_state:
        st.session_state.chat_page_num = 1
    if "uploader_key_counter" not in st.session_state:
        st.session_state.uploader_key_counter = 0
