# app.py

import streamlit as st
import os
from datetime import datetime

# Import dari konfigurasi dan modul
from config import LOGO_PATH, setup_directories
from modules.auth import authentication_ui
from modules.session_manager import initialize_session_state, save_chat_session
from modules.ollama_client import get_ollama_models_cached, query_ollama_non_stream
from modules.file_processor import extract_text_from_file
from modules.ui_components import (
    display_sidebar, 
    display_chat_messages_paginated, 
    display_export_options
)

def main():
    """Fungsi utama untuk menjalankan aplikasi Streamlit."""
    st.set_page_config(
        page_title="DFK Stembot", 
        layout="wide", 
        initial_sidebar_state="expanded", 
        page_icon="🤖"
    )

    # Pastikan semua direktori wujud
    setup_directories()

    # Paparkan logo
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=250)

    # Proses pengesahan pengguna
    if not authentication_ui():
        return  # Hentikan pelaksanaan jika pengguna belum log masuk

    current_username = st.session_state.username

    # Butang log keluar
    with st.sidebar:
        st.markdown(f"#### 👤 Pengguna: {current_username}")
        if st.button("🚪 Log Keluar", use_container_width=True):
            # Reset keadaan sesi dan log keluar
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown("---")

    st.markdown("<h1 style='text-align: center;'>🤖 DFK Stembot</h1>", unsafe_allow_html=True)

    # Muatkan model dan mulakan keadaan sesi
    available_models = get_ollama_models_cached()
    initialize_session_state(available_models)

    st.markdown(f"<p style='text-align: center; color: grey;'>Model Aktif: <b>{st.session_state.selected_ollama_model.split(':')[0]}</b></p>", unsafe_allow_html=True)
    st.markdown("---")

    # Paparkan sidebar dan uruskan logik sesi
    display_sidebar(available_models, current_username)

    # Bahagian muat naik fail
    with st.sidebar:
        st.markdown("#### 📎 Muat Naik & Analisis Fail")
        # ... (Logik muat naik fail anda boleh diletakkan di sini)
        # ... Ia memanggil extract_text_from_file dan query_ollama_non_stream

    # Paparkan mesej perbualan
    display_chat_messages_paginated()

    # Input pengguna
    if user_input := st.chat_input(f"Tanya {st.session_state.selected_ollama_model.split(':')[0].capitalize()}..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner("Sedang berfikir..."):
            assistant_response, thinking, time_taken = query_ollama_non_stream(
                user_input,
                st.session_state.chat_history,
                st.session_state.selected_ollama_model
            )
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": assistant_response,
            "thinking_process": thinking,
            "time_taken": time_taken
        })

        # Jika ini mesej pertama, cipta ID sesi baharu
        if st.session_state.session_id == "new":
            st.session_state.session_id = st.session_state.current_filename_prefix
        
        save_chat_session(current_username, st.session_state.session_id, st.session_state.chat_history)
        st.rerun()

    # Pilihan eksport
    display_export_options()


if __name__ == "__main__":
    main()
