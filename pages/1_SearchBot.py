import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from components.sidebar import render_sidebar
from models.active_models import get_owner

# App title
st.set_page_config(page_title="MultiAI", page_icon="./assets/robot.png")

# Sidebar elements
with st.sidebar:
    render_sidebar(2)

llm = ChatGroq(
    model=st.session_state.selected_model,
    temperature=0.0,
    max_retries=2,
    groq_api_key=st.secrets['groq_api_key']
)

# Page title
st.title('🔎 SearchBot')
st.caption("🚀 Chatbot powered by " + st.session_state.selected_model + " (" + get_owner(st.session_state.selected_model) + ")")

# Session state message variable to hold old messages
if 'search_messages' not in st.session_state:
    st.session_state.search_messages = []

# Display all historical messages
for message in st.session_state.search_messages:
    st.chat_message(message['role']).markdown(message['content'])

# Prompt input template to display the prompts
prompt = st.chat_input('Ask me anything, I can search the web for you!')

# If the user hits enter then
if prompt:
    # Display the prompt
    st.chat_message('user').markdown(prompt)
    # Store user prompt in state
    st.session_state.search_messages.append({'role':'user', 'content':prompt})

    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent(
        [search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True, max_iterations=5
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.search_messages, callbacks=[st_cb])
        st.session_state.search_messages.append({"role": "assistant", "content": response})
        st.write(response)
