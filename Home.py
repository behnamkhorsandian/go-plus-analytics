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
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go


# --- PAGE CONFIG (BROWSER TAB) ---
st.set_page_config(page_title="GoPlus", page_icon=":easter_island_statue:", layout="centered", initial_sidebar_state="expanded")


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
Users = client.Users
Questions = client.Questions 
Reports = client.Reports 
Instructions = client.Instructions
Chats = client.Chats

# ---- USERNAMES ----      
adjectives = ["Rogue", "Savage", "Bold", "Fierce", "Rebel", "Mystic", "Shadow", "Wild", "Cunning", "Brave", "Daring", "Ferocious", "Ruthless", "Steady", "Untamed","Crimson", "Eclipse", "Phantom", "Stealth", "Inferno", "Midnight", "Obsidian", "Vortex", "Tempest", "Abyss", "Zenith", "Nebula", "Mirage", "Ethereal", "Arcane"]
nouns = ["Voyager", "Warrior", "Pirate", "Nomad", "Wanderer", "Outlaw", "Ranger", "Maverick", "Explorer", "Rebel", "Sorcerer", "Assassin", "Bandit", "Guardian", "Champion","Shadow", "Flame", "Raven", "Viper", "Oracle", "Titan", "Specter", "Enigma", "Phoenix", "Sphinx", "Valkyrie", "Sentinel", "Gladiator", "Mystic", "Templar"]
gapminder = px.data.gapminder()
country_to_iso = gapminder[['country', 'iso_alpha']].drop_duplicates().set_index('country')['iso_alpha'].to_dict()


# ---- CACHE SETTING ----
if 'cache_created' not in st.session_state:
    st.session_state['cache_created'] = True
    st.session_state['stage'] = 0
    st.session_state['current_user'] = ""
    st.session_state['fresh_exam'] = True
    st.session_state['fresh_username'] = False
    st.session_state['detailed_results'] = []
    st.session_state['report'] = {}

if 'history' not in st.session_state:
    st.session_state.history = []

# ---- TIMER SETTING ----
if 'time_set' not in st.session_state or not st.session_state['time_set']:
    st.session_state['last_delay']=0
    st.session_state['user_time'] = int(datetime.utcnow().timestamp())
    st.session_state['time_set'] = True


# ---- SIGN UP ----
if st.session_state['stage'] == 0:
    with st.form("Users Data"):
        st.markdown("### Basic Information:")
        st.info("*For your privacy, we don't request names or contact information. We do that to encourage you to feel comfortable providing the true information we request below, as it aids in more insightful data analysis. After that, a random username is provided for checking your exam results. Please note, our website does not store any data and clears cache upon reloading. Ensure you complete and submit the quiz in one session.*")
        st.markdown("#")
        gender = st.selectbox('What is your gender?', options=('Male', 'Female'), placeholder="Select your gender...")
        country = st.selectbox('Where are you coming from?', options=(px.data.gapminder().country.unique()), index=109, placeholder="Select your country...")
        age = st.slider('How old are you?', value=24, max_value=85, step=1)
        education = st.selectbox('What is your level of education?', options=("None","Primary School","High School or Equivalent","Vocational or Technical Training","Bachelor's Degree","Master's Degree","Doctorate or Higher"), placeholder="Select your highest compeleted level of education...")
        domain = st.text_input("What is your major/profession?", placeholder="Please type your major (if you are a student) or your profession (if working)")
        
        if st.form_submit_button("Create Username", use_container_width=True):
            end_time = int(datetime.utcnow().timestamp())
            time_spent = end_time - st.session_state['user_time']
            unique_ts = str(int(datetime.utcnow().timestamp()*1000000))
            unique_id = unique_ts.encode('utf-8')
            unique_id = hashlib.sha1(unique_id).hexdigest()
            seed = int(unique_id, 16)
            random.seed(seed)
            username = random.choice(adjectives)+ "_" + random.choice(nouns) + str(seed)[-2:]
            username = username.lower()
            
            new_user = {"_id": unique_ts,
                        "_username": username,
                        "_gender": gender,
                        "_country": country,
                        "_geo":country_to_iso.get(country, "Unknown"),
                        "_age": age,
                        "_education": education,
                        "_domain":domain
                        }
            st.session_state['current_user'] = username
            st.session_state['fresh_username'] = True
            Users.Profiles.insert_one(new_user)
            st.session_state['stage'] = 1
            st.experimental_rerun()
    st.markdown("#")
    with st.expander("Already have your username?"):
        with st.form("User Login"):
            username = st.text_input("Enter your username?")
            if st.form_submit_button("Login", use_container_width=True):
                end_time = int(datetime.utcnow().timestamp())
                time_spent = end_time - st.session_state['user_time']
                profile = Users.Profiles.find_one({"_username": username})
                if profile:
                    st.session_state['current_user'] = username
                    st.session_state['stage'] = len(list(Questions.Audited.find({})))+2
                    st.experimental_rerun()
                else:
                    st.warning("User not found!")


# ---- USERNAME NOTIFICATION ----
if st.session_state['fresh_username']:
    st.toast(f"Your anonymous username is:\n **{st.session_state['current_user']}**", icon="✅")
    st.session_state['fresh_username']=False


# ---- QUIZ ----
if st.session_state['stage']>0 and st.session_state['stage']<=len(list(Questions.Audited.find({}))):
    item = Questions.Audited.find_one({"_id": f"{st.session_state['stage']}"})
    st.markdown(f"### Question {st.session_state['stage']}:")
    st.markdown(f"{item['_question']}")
    
    if 'pattern' not in st.session_state:
        st.session_state['pattern'] = [{"click":"_option_5","delay": st.session_state['last_delay']}]
    if 'current_answer' not in st.session_state:
        st.session_state['current_answer'] = None

    user_answer = st.radio("Answer", 
                           [f"{item['_option_1']['text']}", 
                            f"{item['_option_2']['text']}", 
                            f"{item['_option_3']['text']}", 
                            f"{item['_option_4']['text']}",
                            f"{item['_option_5']['text']}"], 
                            key='user_answer', index=4)
    
    if user_answer != st.session_state['current_answer']:
        st.session_state['current_answer'] = user_answer
        change_time = int(datetime.utcnow().timestamp())
        delay = change_time - st.session_state['user_time']-st.session_state['last_delay']
        st.session_state['last_delay'] = delay
        for i in range(1, 6):
            option_key = f'_option_{i}'
            if item[option_key]['text'] == st.session_state['current_answer']:
                chosen_option = f"_option_{i}"
                change = {"click":chosen_option,"delay": delay}
                st.session_state['pattern'].append(change)
                break
        
    with st.form("Quiz Box"):
        if st.form_submit_button("Submit Answer", use_container_width=True,disabled=user_answer== "Select an option", type="primary"):
            end_time = int(datetime.utcnow().timestamp())
            time_spent = end_time - st.session_state['user_time']
            st.session_state['time_set'] = False
            for i in range(1, 6):
                option_key = f'_option_{i}'
                if item[option_key]['text'] == user_answer:
                    user_score = item[option_key]['score']
                    chosen_option = f"_option_{i}"
                    break
            update_operation = {"$set": {
                f"_{item['_tag'][0]}_answer": f"{chosen_option}", 
                f"_{item['_tag'][0]}_time": time_spent, 
                f"_{item['_tag'][0]}_score":user_score,
                f"_{item['_tag'][0]}_pattern":st.session_state['pattern']}}
            Users = client.Users
            Users.Profiles.update_one({"_username": f"{st.session_state['current_user']}"}, update_operation)
            if st.session_state['stage'] == len(list(Questions.Audited.find({}))):
                st.session_state['fresh_exam'] = False
            st.session_state.pop('pattern', None)
            st.session_state.pop('current_answer', None)
            st.session_state['stage'] = st.session_state['stage'] + 1
            st.experimental_rerun()



# ---- REPORT ----
if st.session_state['stage'] == len(list(Questions.Audited.find({})))+1:
    
    user_profile = Users.Profiles.find_one({"_username": st.session_state['current_user']})
    user_report = {
        "_username": st.session_state['current_user'],
        "_gender": user_profile['_gender'],
        "_country": user_profile['_country'],
        "_geo": user_profile['_geo'],
        "_age": user_profile['_age'],
        "_education": user_profile['_education'],
        "_domain": user_profile['_domain'],
    }
    
    total_time = 0
    total_score = 0
    for question in list(Questions.Audited.find({})):
        user_report[f'question_{question["_id"]}']={
            "_text":question['_question'],
            "_tag":question['_tag'][0],
            "_key": question[question['_key']]['text'],
            "_answer":question[user_profile[f'_{question["_tag"][0]}_answer']]['text'],
            "_result": question[question['_key']]['text']==question[user_profile[f'_{question["_tag"][0]}_answer']]['text'],
            "_time": user_profile[f'_{question["_tag"][0]}_time'],
            "_change": len(user_profile[f'_{question["_tag"][0]}_pattern'])-2,
            "_pattern_time": [change['delay'] for change in (user_profile[f'_{question["_tag"][0]}_pattern'])],
            "_pattern_click": [question[change['click']]['text'] for change in (user_profile[f'_{question["_tag"][0]}_pattern'])],
            "_pattern_score": [question[change['click']]['score'] for change in (user_profile[f'_{question["_tag"][0]}_pattern'])],
        }
        
        user_report[f'question_{question["_tag"][0]}_text']=question['_question']
        user_report[f'question_{question["_tag"][0]}_tag']=question['_tag'][0]
        user_report[f'question_{question["_tag"][0]}_key']= question[question['_key']]['text']
        user_report[f'question_{question["_tag"][0]}_answer']=question[user_profile[f'_{question["_tag"][0]}_answer']]['text']
        user_report[f'question_{question["_tag"][0]}_result']= question[question['_key']]['text']==question[user_profile[f'_{question["_tag"][0]}_answer']]['text']
        user_report[f'question_{question["_tag"][0]}_time']= user_profile[f'_{question["_tag"][0]}_time']
        user_report[f'question_{question["_tag"][0]}_change']= len(user_profile[f'_{question["_tag"][0]}_pattern'])-2
        user_report[f'question_{question["_tag"][0]}_pattern_time']= [change['delay'] for change in (user_profile[f'_{question["_tag"][0]}_pattern'])]
        user_report[f'question_{question["_tag"][0]}_pattern_click']= [question[change['click']]['text'] for change in (user_profile[f'_{question["_tag"][0]}_pattern'])]
        user_report[f'question_{question["_tag"][0]}_pattern_score']= [question[change['click']]['score'] for change in (user_profile[f'_{question["_tag"][0]}_pattern'])]
        
        total_time = total_time + user_profile[f'_{question["_tag"][0]}_time']
    
        if question[question['_key']]['text']==question[user_profile[f'_{question["_tag"][0]}_answer']]['text']:
            total_score = total_score + 1
            user_report[f'question_{question["_tag"][0]}_score'] = 100
        else:
            user_report[f'question_{question["_tag"][0]}_score'] = 0
        user_report[f'question_{question["_tag"][0]}_time'] = user_profile[f'_{question["_tag"][0]}_time']
        
        
    user_report['_total_time']=total_time
    user_report['_total_score']=(total_score/len(list(Questions.Audited.find({}))))*100
    user_report['avarage_time'] = total_time/len(list(Questions.Audited.find({})))
    
    
    
    Reports.Raw.insert_one(user_report)
    st.session_state['report'] = user_report
    st.session_state['stage'] = st.session_state['stage'] + 1
    st.experimental_rerun()


# ---- RESULTS ----
if st.session_state['stage'] == len(list(Questions.Audited.find({})))+2:
    
    st.session_state['report'] = Reports.Raw.find_one({"_username": st.session_state['current_user']})
    if st.session_state['fresh_exam'] == False:
        st.success(f"You can check your results again later by entering **'{st.session_state['current_user']}'** as your username.")
    st.markdown(f"### Results:")
    user_questions = []
    for question in list(Questions.Audited.find({})):
        id = question['_id']
        user_questions.append(Reports.Raw.find_one({"_username": st.session_state['current_user']})[f"question_{id}"])
    details = pd.DataFrame(user_questions)
    st.session_state['results_dataframe'] = details[["_tag","_key","_result","_time","_change","_pattern_time","_pattern_score"]].rename(columns={"_tag":"Topic","_key":"Answer","_result":"Result","_time":"Time","_change":"Changes","_pattern_time":"Pattern","_pattern_score":"Performance"})
    
    correct_answers=0
    for result in st.session_state['results_dataframe']["Result"]:
        if result:
            correct_answers = correct_answers + 1
    student_average=(correct_answers/len(st.session_state['results_dataframe']))*100
    
    answering_time=st.session_state['results_dataframe']["Time"].mean()
    total_time=st.session_state['results_dataframe']["Time"].sum()
    st.session_state['results_dataframe']["Time"] = st.session_state['results_dataframe']["Time"].apply(lambda x: str(timedelta(seconds=x)))
    
    layout = grid([1,1,2], vertical_align="center")
    layout.metric("Final Score", f"{student_average:.0f}%")
    layout.metric("Avarage Answering Time", f"{answering_time}sec")
    layout.markdown(f"You answered :green[**{int(correct_answers)}**] of the questions correctly and took you :blue[**{(total_time/60):.1f} minutes**] to finish the quiz.")

    st.markdown(f"### Details:")

    column_configuration = {
            'Topic':st.column_config.ListColumn(help="Shows the main topic of the question."),
            'Answer':st.column_config.TextColumn(help="Shows the correct answer."),
            'Result':st.column_config.CheckboxColumn(help="Shows if you have answered correctly."),
            'Time': st.column_config.TimeColumn(width="small", help="Shows the time you took to submit your answer."),
            'Changes': st.column_config.NumberColumn(width="small", help="Shows how many times you have changed your answers."),
            'Pattern': st.column_config.BarChartColumn(y_max=int(answering_time), y_min=0, width="small", help="Shows the time it took you to change your answers."),
            'Performance': st.column_config.LineChartColumn(y_max=100, y_min=-5, width="small", help="Shows your performance as you changed your answers."),
        }
    st.dataframe(st.session_state['results_dataframe'],column_config=column_configuration, use_container_width=True)
    
