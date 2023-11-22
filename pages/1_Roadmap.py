# STREAMLIT
import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.app_logo import add_logo
from streamlit_echarts import st_echarts
from streamlit_option_menu import option_menu

import plotly.figure_factory as ff
import pandas as pd
from datetime import datetime, timedelta


# --- PAGE CONFIG (BROWSER TAB) ---
st.set_page_config(page_title="Playground", page_icon=":robot_face:",
                   layout="centered", initial_sidebar_state="expanded")
# add_logo("images/gopluslogo.png", height=128)


# ---- LOAD CSS ----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")



# --- MAIN PAGE ---
with st.container():
    st.title("Roadmap")
    
    st.write('''
             The Shape Up methodology, when paired with a billing model that mirrors its cycles, offers an optimized, value-driven approach to project management and financial planning. It promises not just timely and within-budget delivery but also cultivates a relationship of trust and mutual benefit between service providers and clients.
             ''')
    st.divider()
    st.write('''
             ## Shape-Up:
             Traditional project management methodologies have long been scrutinized for their lack of flexibility, often leading to scope creep, budget overruns, and delayed deliveries. Enter the Shape Up methodology, a groundbreaking framework that offers an agile yet focused approach to software development. But the magic doesn't stop there; you can also align billing cycles with Shape Up cycles, creating a win-win scenario for both service providers and clients.
             ### Cycle Types:
             #
             ''')
    
    
    layout = grid([1,1,1] , vertical_align="center")
    with layout.container():
        st.image("images/sCycle.png")
        st.write("#### Short Cycle:")
        st.caption("The Short Cycle is like a quick clean-up. It's about fixing small issues fast with little planning. Teams get to reflect, recharge, and make sure everyone is on the same page. It's best for wrapping up tasks and adjusting to sudden changes.")
    with layout.container():
        st.image("images/mCycle.png")
        st.write("#### Medium Cycle:")
        st.caption("The Medium Cycle is a playground for new ideas. It’s about creating rough versions of ideas with a flexible plan. Teams can innovate, learn from what they find, and steer the project in the right direction. It’s great when things are a bit uncertain and there's room for exploring different solutions.")
    with layout.container():
        st.image("images/lCycle.png")
        st.write("#### Long Cycle:")
        st.caption("The Long Cycle is all about getting things done. It requires a solid plan to create a finished product. Teams review their work thoroughly, hold each other accountable, and aim to grow the project significantly. It’s best for when there's a clear goal and a structured path to achieve it.")    
    
    
    st.write("#")
    st.write("## Timeline")
    st.write("#")
    st.image("images/timeline.png")
    st.write("#")
    
    navbar = option_menu(
        menu_title= None,
        options=["Step-1", "Step-2", "Step-3", "Step-4"],
        icons=["None", "None", "None", "None"],
        orientation="horizontal",
        default_index=0,
    )

    if navbar=="Step-1":
        st.write("#")
        layout = grid([1,3] , vertical_align="center")
        with layout.container():
            st.image("images/phase2.png")
        with layout.container():
            st.image("images/assess.png")
        st.write("#### Step-1: Assess")
        st.write('''
                In this level we are going to collect and clean your database (or given sample) to get fimiliar with the types of data you have.
                At the end of this phase, we are going to have our structured data (tagging system), so we can find the possibilities for further analysis.
                ''')
    
    elif navbar=="Step-2":
        st.write("#")
        layout = grid([1,3] , vertical_align="center")
        with layout.container():
            st.image("images/phase3.png")
        with layout.container():
            st.image("images/define.png")
        st.write("#### Step-2: Define")
        st.write('''
                This is the phase that we start finding correlation between different KPIs and tags, so later we can identify and design the initiative to take forward.
                At the end of this phase, we have an AI model that has been trained on clients data.
                ''')

    elif navbar=="Step-3":
        st.write("#")
        layout = grid([1,3] , vertical_align="center")
        with layout.container():
            st.image("images/phase3.png")
        with layout.container():
            st.image("images/design.png")
        st.write("#### Step-3: Design")
        st.write('''
                After training our model, it's time to design the pipelines of data for the actual outputs.
                At the end of this phase, we will be able to feed the model with resources (notebooks, question banks) and students grades, and then extract the gaps (both in knowledge and resources depth) and predictions about student performance in the future.
                ''')
    
    elif navbar=="Step-4":
        st.write("#")
        layout = grid([1,3] , vertical_align="center")
        with layout.container():
            st.image("images/phase3.png")
        with layout.container():
            st.image("images/pilot.png")
        st.write("#### Step-4: Pilot")
        st.write('''
                Finaly it's time to put all of our achivments together and automate the whole process.
                At the end of this phase, we will have the MVP of **`Pioneer Coach`**, The AI Tutor and Teacher Assistant.
                ''')
