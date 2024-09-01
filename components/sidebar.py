import streamlit as st
from models.active_models import active_models

# Determine the default model
default_model = "llama3-70b-8192" if "llama3-70b-8192" in active_models else active_models[0]

def clear_chat_history(state):
    if state == 0:
        st.session_state.chatbot_messages = []
    elif state == 1:
        st.session_state.qna_messages = []
    else:
        st.session_state.search_messages = []

def render_sidebar(state):
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = default_model

    if state == 1:
        st.caption("⚠️ Navigating away from this tab will reset the chat.")

    # Sidebar model selection without clearing history on change
    selected_model = st.selectbox("Select LLM", active_models, index=active_models.index(st.session_state.selected_model))

    # Only update the selected model if it has changed
    if selected_model != st.session_state.selected_model:
        st.session_state.selected_model = selected_model
    
    # Add custom CSS to style the button
    st.markdown("""
        <style>
        .full-width-button .stButton button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Add the button with the custom CSS class
    if state < 3:
        st.button("Clear Chat", key="clear_chat", help="Clear the chat history", on_click=lambda: clear_chat_history(state), args=(), kwargs={}, disabled=False, use_container_width=True)
