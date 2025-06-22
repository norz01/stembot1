# modules/ui_components.py

import streamlit as st
from datetime import datetime
import os
import time

# Import fungsi dari modul lain
from .session_manager import (
    load_all_session_ids, delete_chat_session_file, 
    delete_all_chat_sessions, load_chat_session
)
from .file_processor import (
    format_conversation_text, save_to_word, save_to_txt, save_to_pdf,
    save_to_excel, save_to_pptx
)
from config import EXPORT_DIR

def display_sidebar(available_models, username):
    """Memaparkan sidebar dengan tetapan dan pengurusan sesi."""
    with st.sidebar:
        st.markdown("## ⚙️ Tetapan & Sesi")
        st.markdown("---")
        
        # Pemilih Model AI
        st.markdown("#### Model AI")
        if available_models:
            try:
                current_model_index = available_models.index(st.session_state.selected_ollama_model)
            except ValueError:
                current_model_index = 0
            
            selected_model_ui = st.selectbox(
                "Pilih Model:", options=available_models, index=current_model_index,
                key="model_selector_widget", label_visibility="collapsed"
            )
            if selected_model_ui != st.session_state.selected_ollama_model:
                st.session_state.selected_ollama_model = selected_model_ui
                st.rerun()
        else:
            st.warning("Tiada model AI ditemui.")
        
        st.markdown("---")
        
        # Pemilih Sesi Perbualan
        st.markdown("#### 💬 Sesi Perbualan")
        session_ids = load_all_session_ids(username)
        options = ["➕ Perbualan Baru"] + session_ids
        
        try:
            current_session_index = options.index(st.session_state.session_id) if st.session_state.session_id != "new" else 0
        except ValueError:
            current_session_index = 0
        
        selected_session_id_ui = st.selectbox(
            "Pilih atau Mulakan Sesi:", options, index=current_session_index,
            key="session_selector_widget", label_visibility="collapsed"
        )
        
        # Logik untuk menukar sesi
        handle_session_logic(username, selected_session_id_ui)

        st.markdown("---")
        
        # Pengurusan Sesi Lanjutan
        with st.expander("🗑️ Urus Sesi Lanjutan"):
            # ... (Kod asal anda untuk butang padam sesi boleh diletakkan di sini)
            pass

def handle_session_logic(username, selected_session_id):
    """Menguruskan logik apabila sesi ditukar."""
    if selected_session_id == "➕ Perbualan Baru" and st.session_state.session_id != "new":
        st.session_state.session_id = "new"
        st.session_state.chat_history = []
        st.session_state.current_filename_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.chat_page_num = 1
        st.rerun()
    elif selected_session_id != "➕ Perbualan Baru" and st.session_state.session_id != selected_session_id:
        st.session_state.chat_history = load_chat_session(username, selected_session_id)
        st.session_state.session_id = selected_session_id
        st.session_state.current_filename_prefix = selected_session_id
        st.session_state.chat_page_num = 1
        st.rerun()

def display_chat_messages_paginated():
    """Memaparkan mesej perbualan dengan paginasi."""
    # ... (Kod asal anda untuk fungsi ini sudah baik, boleh disalin terus)
    pass

def display_export_options():
    """Memaparkan pilihan untuk mengeksport perbualan."""
    # ... (Kod asal anda untuk fungsi ini sudah baik, boleh disalin terus)
    # Pastikan untuk menggunakan EXPORT_DIR dari config
    pass
