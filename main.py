import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if API key loaded
if not GOOGLE_API_KEY:
    st.error("⚠️ GOOGLE_API_KEY not found in .env file.")
    st.stop()

# Configure Gemini with API key
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-1.5-flash-latest")

# Configure Streamlit page
st.set_page_config(
    page_title="Chat with Rocky-AI!",
    page_icon=":brain:",
    layout="centered",
)

# Translate Gemini role to Streamlit role
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# App title
st.title("🤖 Rocky AI - ChatBot")

# Show chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(str(message.parts[0]))

# User input
user_prompt = st.chat_input("Ask Rocky-AI...")

if user_prompt:
    # Show user message
    st.chat_message("user").markdown(user_prompt)

    try:
        # Get Gemini response
        rocky_response = st.session_state.chat_session.send_message(user_prompt)

        # Show AI response
        with st.chat_message("assistant"):
            st.markdown(rocky_response.text)

    except Exception as e:
        st.error("⚠️ Something went wrong while communicating with Gemini.")
        st.exception(e)
