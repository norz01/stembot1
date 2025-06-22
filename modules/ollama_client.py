# modules/ollama_client.py

import streamlit as st
import requests
import json
import time
from config import OLLAMA_BASE_URL

@st.cache_data(ttl=300)
def get_ollama_models_cached():
    """Mendapatkan senarai model dari Ollama API dan menyimpannya dalam cache."""
    try:
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=10)
        response.raise_for_status()
        models_data = response.json().get('models', [])
        return sorted([model['name'] for model in models_data]) if models_data else []
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal menyambung ke Ollama: {e}")
        return []

def query_ollama_non_stream(prompt, chat_history, selected_model):
    """Menghantar permintaan ke Ollama API dan mengendalikan respons."""
    # ... (Kod asal anda untuk fungsi ini sudah sangat baik dan mantap)
    # ... (Saya sertakan di sini untuk kelengkapan)
    messages_for_api = [{"role": msg["role"], "content": msg["content"]} for msg in chat_history]
    
    # Elak menambah prompt yang sama jika ia sudah menjadi mesej terakhir
    if not (messages_for_api and messages_for_api[-1]["role"] == "user" and messages_for_api[-1]["content"] == prompt):
        messages_for_api.append({"role": "user", "content": prompt})

    start_time = time.time()
    try:
        payload = {'model': selected_model, 'messages': messages_for_api, 'stream': False}
        response = requests.post(f'{OLLAMA_BASE_URL}/api/chat', json=payload, timeout=600)
        response.raise_for_status()
        
        full_response_data = response.json()
        raw_assistant_reply = full_response_data.get('message', {}).get('content', "Tiada kandungan.")
        
        # Logik untuk memisahkan 'thinking process'
        thinking_process = ""
        assistant_reply = raw_assistant_reply
        thinking_start_tag = "<think>"
        thinking_end_tag = "</think>"
        if thinking_start_tag in raw_assistant_reply and thinking_end_tag in raw_assistant_reply:
            start_index = raw_assistant_reply.find(thinking_start_tag)
            end_index = raw_assistant_reply.find(thinking_end_tag)
            if start_index < end_index:
                thinking_process = raw_assistant_reply[start_index + len(thinking_start_tag):end_index].strip()
                assistant_reply = raw_assistant_reply[end_index + len(thinking_end_tag):].strip()

        processing_time = time.time() - start_time
        return assistant_reply, thinking_process, processing_time

    except requests.exceptions.HTTPError as http_err:
        error_msg = f"Ralat HTTP dari Ollama: {http_err}"
        try:
            error_details = http_err.response.json().get("error", "Tiada butiran.")
            error_msg += f" Butiran: {error_details}"
        except json.JSONDecodeError:
            pass
        st.error(error_msg)
        return "Maaf, berlaku ralat HTTP semasa menghubungi Ollama.", "", time.time() - start_time
    except requests.exceptions.Timeout:
        st.error("Permintaan ke Ollama tamat masa.")
        return "Maaf, permintaan tamat masa.", "", time.time() - start_time
    except requests.exceptions.RequestException as e:
        st.error(f"Masalah menyambung ke Ollama: {e}")
        return "Maaf, berlaku masalah semasa menghubungi Ollama.", "", time.time() - start_time
    except Exception as e:
        st.error(f"Ralat tidak dijangka: {e}")
        return "Maaf, ralat tidak dijangka berlaku.", "", time.time() - start_time
