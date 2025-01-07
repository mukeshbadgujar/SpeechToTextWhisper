import streamlit as st
import streamlit_authenticator as stauth
import whisper
import tempfile
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(message, level='info'):
    if level == 'info':
        logging.info(message)
        st.write(f"INFO: {message}")
    elif level == 'debug':
        logging.debug(message)
        st.write(f"DEBUG: {message}")
    elif level == 'warning':
        logging.warning(message)
        st.warning(f"WARNING: {message}")
    elif level == 'error':
        logging.error(message)
        st.error(f"ERROR: {message}")
    elif level == 'critical':
        logging.critical(message)
        st.error(f"CRITICAL: {message}")

# ========== USER AUTHENTICATION ==========
credentials = {
    "usernames": {
        "admin": {
            "name": "Admin User",
            "password": "$2b$12$WEAMfkQGjh2WU9mZv1uo.Osj32RxuWUpdTNSyxAFEKVaGcFbCsn.m",
            "email": "admin@gmail.com"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="whisper_app",
    key="random_key",
    cookie_expiry_days=1
)

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

authenticator.login(location='main')

if st.session_state["authentication_status"]:
    st.sidebar.success(f"Welcome {st.session_state["name"]}!")
    authenticator.logout("Logout", "sidebar")

    st.title("Speech-to-Text with OpenAI Whisper")
    audio_file = st.file_uploader("Upload your audio file", type=["mp3", "wav", "m4a"])

    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_file_path = tmp_file.name

        st.info("Transcribing... Please wait.")
        model = whisper.load_model("base")
        result = model.transcribe(tmp_file_path)

        st.subheader("Transcription")
        st.write(result["text"])

        st.download_button(
            label="Download Transcription",
            data=result["text"],
            file_name="transcription.txt",
            mime="text/plain",
        )

        try:
            os.remove(tmp_file_path)
        except Exception as e:
            log_message(f"Error deleting temporary file: {e}", "error")

elif st.session_state["authentication_status"] is False:
    st.error("Invalid username or password.")
else:
    st.info("Please log in to access the app.")
