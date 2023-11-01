# ESSENTIALS
import json
import time
import asyncio
from streamlit_extras.stateful_chat import chat, add_message

# STREAMLIT
import streamlit as st
from streamlit_extras.app_logo import add_logo 

# --- PAGE CONFIG (BROWSER TAB) ---
st.set_page_config(page_title="GoPlus", page_icon=":robot_face:", layout="centered", initial_sidebar_state="expanded")
add_logo("images/gopluslogo.png", height=128)


# ---- LOAD ASSETS ----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")


# ---- MEMORY SETTINGS ----
if 'history' not in st.session_state:
    st.session_state.history = []


# --- MAIN PAGE ---
with st.container():
    st.title("👽 Pioneer Coach")
    
    st.write('''
             Before we wrap up, let me introduce you to Pioneer Coach, your AI-powered teaching assistant. Whether you need to focus on a specific topic or you're looking for personalized study materials, Pioneer Coach has you covered. And the more you interact with it, the better it gets at helping you learn.
             ''')
    pass

with chat("Debug"):
    history = st.session_state.history
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if prompt := st.chat_input():
        add_message("user", prompt, avatar="💭")
        st.session_state.history.append({"role": "user", "content": prompt})

        
        
        
        
        
        respond = "this is the aswer"
        st.session_state.history.append({"role": "assistant", "content": respond})

        def stream_output():
            for word in respond.split():
                for letter in word:
                    yield letter
                    time.sleep(0.025)
                yield " "  # Add a space after each word
        st.session_state.history.append({"role": "assistant", "content": respond})

    
        add_message("assistant", stream_output, avatar="💬")
        

