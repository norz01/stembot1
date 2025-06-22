# modules/auth.py

import streamlit as st
import json
import os
import bcrypt
from datetime import datetime
from config import USERS_FILE, setup_directories

# Pastikan direktori wujud semasa modul diimport
setup_directories()

def load_users():
    """Memuatkan data pengguna dari fail JSON."""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Menyimpan data pengguna ke fail JSON."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    """Melencongkan kata laluan menggunakan bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    """Mengesahkan kata laluan dengan hash yang disimpan."""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login_page():
    """Memaparkan borang log masuk."""
    st.title("🔐 Log Masuk")
    with st.form("login_form"):
        username = st.text_input("Nama Pengguna", key="login_username")
        password = st.text_input("Kata Laluan", type="password", key="login_password")
        submitted = st.form_submit_button("Log Masuk", type="primary", use_container_width=True)

        if submitted:
            users = load_users()
            if username in users and verify_password(password, users[username]["password"]):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Berjaya log masuk!")
                st.rerun()
            else:
                st.error("Nama pengguna atau kata laluan salah.")

def register_page():
    """Memaparkan borang pendaftaran."""
    st.title("📝 Daftar Akaun")
    with st.form("register_form"):
        username = st.text_input("Nama Pengguna Baru", key="register_username")
        password = st.text_input("Kata Laluan", type="password", key="register_password")
        confirm_password = st.text_input("Sahkan Kata Laluan", type="password", key="confirm_password")
        submitted = st.form_submit_button("Daftar", type="primary", use_container_width=True)

        if submitted:
            if not username or not password:
                st.warning("Sila lengkapkan semua medan.")
                return
            if password != confirm_password:
                st.error("Kata laluan tidak sepadan.")
                return
            
            users = load_users()
            if username in users:
                st.error("Nama pengguna telah wujud.")
                return
            
            users[username] = {
                "password": hash_password(password),
                "created_at": datetime.now().isoformat()
            }
            save_users(users)
            st.success("Akaun berjaya didaftarkan! Sila log masuk.")
            # Tidak perlu rerun di sini, biarkan pengguna lihat mesej kejayaan
            
def authentication_ui():
    """Menguruskan UI untuk log masuk dan pendaftaran."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("## Selamat Datang ke DFK Stembot")
        tab1, tab2 = st.tabs(["Log Masuk", "Daftar Akaun"])
        with tab1:
            login_page()
        with tab2:
            register_page()
        return False
    return True
