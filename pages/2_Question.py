import streamlit as st
import streamlit_authenticator as auth
from streamlit_option_menu import option_menu
from streamlit_extras.grid import grid
from streamlit_extras.stateful_chat import chat, add_message
from streamlit_extras.mandatory_date_range import date_range_picker
from streamlit_echarts import st_echarts
from streamlit_lottie import st_lottie

import asyncio

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import time
from datetime import datetime, timedelta
import random
import hashlib
import openai
import json

import pandas as pd


# --- PAGE CONFIG (BROWSER TAB) ---
st.set_page_config(page_title="GoPlus", page_icon=":easter_island_statue:", layout="centered", initial_sidebar_state="collapsed")


# ---- LOAD ASSETS ----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")


# ---- TYPING EFFECT ----
def stream_output(_respond):
    for word in _respond.split():
        for letter in word:
            yield letter
            time.sleep(0.025)
        yield " "  # Add a space after each word



# ---- DATABASE ----   
mongodb_url =  st.secrets["db_url"]
client = MongoClient(mongodb_url, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)
Prompts = client.Prompts

# ---- OPENAI ----   
openai.api_key = st.secrets["openai_apikey"]


# ---- CACHE SETTING ----
if 'cache_created' not in st.session_state:
    st.session_state['cache_created'] = True
    st.session_state['question'] = ""
    st.session_state['new_question'] = ""
    st.session_state['answer'] = ""


# ---- QUESTION ----

with st.form("Question Generation"):
    st.markdown("### Question Generation:")
    _question = st.text_area('Write your question template', height=10, placeholder="A car traveling at 10 meters per second (m/s) begins to accelerate uniformly. After 5 seconds, its speed increases to 20 m/s. What is the car's acceleration during this time?")
    if st.form_submit_button("Create Similar Question", use_container_width=True):
        st.session_state['question'] = _question
        
        question = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": Prompts.GeneretiveQA.find_one({"_id": "question_generation"})['_prompt']},
                {"role": "user", "content": st.session_state['question']}
                ],
            presence_penalty = 0.2,
            max_tokens = 250
            )
        st.session_state['new_question'] = question.choices[0].message.content
        st.experimental_rerun()
        
if len(st.session_state['new_question']) > 0:
    st.markdown(st.session_state['new_question'])

    if st.button("Step-by-Step Solution"):
        answer = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": Prompts.GeneretiveQA.find_one({"_id": "answer_generation"})['_prompt']},
                {"role": "user", "content": st.session_state['new_question']}
                ],
            max_tokens = 250
            )
        st.session_state['answer'] = answer.choices[0].message.content
        st.experimental_rerun()
        
if len(st.session_state['answer']) > 0:
    st.markdown(st.session_state['answer'])
        
    
    