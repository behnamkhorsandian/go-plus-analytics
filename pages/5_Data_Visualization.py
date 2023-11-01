# ESSENTIALS
import json
from pymongo import MongoClient

import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go


# STREAMLIT
import streamlit as st
from streamlit_extras.grid import grid
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
    st.session_state.history = []
    students_count = 30
    student_names = [f'Student_{i+1}' for i in range(students_count)]
    Patient_Assessment = np.random.randint(0, 100, students_count)
    Medication_Administration = np.random.randint(0, 100, students_count)
    Wound_Care = np.random.randint(0, 100, students_count)
    Infection_Control = np.random.randint(0, 100, students_count)
    Emergency_Response = np.random.randint(0, 100, students_count)
    overall = np.mean([Patient_Assessment, Medication_Administration, Wound_Care, Infection_Control, Emergency_Response], axis=0)
    
    st.session_state["grades_df"] = pd.DataFrame({
                                    'Student Name': student_names,
                                    'Technology': Patient_Assessment,
                                    'Environment': Medication_Administration,
                                    'Society': Wound_Care,
                                    'History': Infection_Control,
                                    'Economy': Emergency_Response,
                                    'GRADE': overall
                                })


# --- NAVIGATION BAR ---
with st.sidebar:
    pass


# --- MAIN PAGE ---
with st.container():
    st.title("📊 Data Visualization")
    st.image("images/data_visualization.png")
    st.write('''
             Finally, let's talk Data Visualization. We're using heat maps to point out your strengths and weaknesses, spider graphs to show the effectiveness of different learning resources, and histograms to highlight challenging topics. This isn't just data; it's a visually rich, easy-to-understand report card on your learning journey.
             ''')
    
    st.divider()
    
    st.title("Course Performance:")
    course_layout = grid([1,1] , vertical_align="center")
    overall_grades = {
        'Technology': st.session_state["grades_df"]['Technology'].mean(),
        'Environment': st.session_state["grades_df"]['Environment'].mean(),
        'Society': st.session_state["grades_df"]['Society'].mean(),
        'History': st.session_state["grades_df"]['History'].mean(),
        'Economy': st.session_state["grades_df"]['Economy'].mean()
    }
    fake_values = [70, 30, 75, 55, 90]
    categories = list(overall_grades.keys())
    values = list(overall_grades.values())
    
    # SPIDER GRAPH
    overall_performance = go.Figure()
    overall_performance.add_trace(go.Scatterpolar( r=fake_values, theta=categories, fill='toself', line=dict(color='teal'), name="Image"))
    overall_performance.add_trace(go.Scatterpolar( r=values, theta=categories, fill='toself', line=dict(color='purple'), name="Text"))
    overall_performance.update_layout( polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
    
    # HISTOGRAM
    cource_histogram = px.histogram(st.session_state["grades_df"], x=st.session_state["grades_df"].columns[1:-1], marginal='box', color_discrete_sequence=px.colors.sequential.Viridis)
    cource_histogram.update_layout(bargap=0.1)

    # Display the histogram in Streamlit
    st.plotly_chart(cource_histogram)
    st.plotly_chart(overall_performance)
    
    
    
    
    st.divider()

with st.container():
    st.title("Students Performance:")
    categories = ['Patient Assessment', 'Medication Administration', 'Wound Care', 'Infection Control', 'Emergency Response']
    transposed_df = st.session_state["grades_df"].drop(columns=['GRADE']).set_index('Student Name').transpose()
    single_performance = ff.create_annotated_heatmap(
        z=transposed_df.values,
        x=transposed_df.columns.tolist(),
        y=transposed_df.index.tolist(),
        annotation_text=transposed_df.values,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='Grades')
    )
    
    single_performance.update_layout(
        xaxis=dict(title='Student Name'),
        yaxis=dict(title='Category')
    )
    st.plotly_chart(single_performance, use_container_width=True)
    pass

