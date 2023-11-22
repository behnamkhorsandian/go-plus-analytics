# STREAMLIT
import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.app_logo import add_logo
from streamlit_echarts import st_echarts
from streamlit_option_menu import option_menu

import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# --- PAGE CONFIG (BROWSER TAB) ---
st.set_page_config(page_title="GoPlus", page_icon=":robot_face:",
                   layout="centered", initial_sidebar_state="expanded")
add_logo("images/gopluslogo.png", height=128)


# ---- LOAD CSS ----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")


# ---- MEMORY SETTINGS ----
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
    st.session_state.sample_size = 5
    st.session_state.population_size = 10
    st.session_state.error_margin = 5

# --- DATA COLLECTION ---
with st.container():
    st.title("Data Collection")
    st.markdown("""
                As we go forward in developing the "GoPlus Analytics" platform, 
                our first step is to gathe comprehensive data that will drive our AI solutions and predictive analytics. 
                Clients contribution to this phase is invaluable, and we want to ensure they understand the importance of each piece of data we request.
                """)
    st.header("Importance of Sample Size")
    st.markdown("""
                Let's begin with the sample size. 
                The amount of data we start with (specifically, the number of student records from the LMS) is crucial. 
                Think of it like a survey: the more responses you have, the clearer the picture of the overall population.
                With a larger sample size, our AI can make more accurate and robust predictions, reducing the margin of error.
                """)
    st.caption("For example, if we only analyze data from 10 students, a single student's unusual performance could skew our results significantly. However, if we analyze 1,000 students, one student's data has less impact on the overall trends, leading to more reliable and applicable insights.")
    
# FUNCTION  
def calculate_sample_size(N, e):
    n = N / (1 + N * (e/100)**2)
    return round(n)
    

# DataCollection:
df = pd.read_csv("assets/kaggle_education.csv")
# DataCleaning:
df['GradeID'] = df['GradeID'].apply(lambda x: int(x.split('-')[1]))
df['GradeID'] = df['GradeID'].apply(lambda x: x / df['GradeID'].max())
df['Discussion'] = df['Discussion'].apply(lambda x: x / df['Discussion'].max())
df['RaisedHands'] = df['RaisedHands'].apply(lambda x: x / df['RaisedHands'].max())
df['ResourcesVisited'] = df['ResourcesVisited'].apply(lambda x: x / df['ResourcesVisited'].max())
df['AnnouncementsViews'] = df['AnnouncementsViews'].apply(lambda x: x / df['AnnouncementsViews'].max())

df = df.reset_index()


with st.expander("Read more..."):
    st.markdown("""
                ##### About this dataset:
                This is an educational data set which is collected from learning management system (LMS) called **Kalboard 360**. 
                Kalboard 360 is a multi-agent LMS, which has been designed to facilitate learning through the use of leading-edge technology. 
                Such system provides users with a synchronous access to educational resources from any device with Internet connection.
                
                The data is collected using a learner activity tracker tool, which called **experience API (xAPI)**. 
                The xAPI is a component of the training and learning architecture (TLA) that enables to monitor learning progress and learner's actions like reading an article or watching a training video. 
                The experience API helps the learning activity providers to determine the learner, activity and objects that describe a learning experience.
                The dataset consists of **480 student** records and 16 features. The features are classified into three major categories: 
                
                - 1- Demographic features such as gender and nationality. 
                - 2- Academic background features such as educational stage, grade Level and section. 
                - 3- Behavioral features such as raised hand on class, opening resources, answering survey by parents, and school satisfaction.
                
                #
                ##### Data Varaity:
                The dataset consists of 305 males and 175 females. The students come from different origins such as 179 students are from Kuwait, 172 students are from Jordan, 28 students from Palestine, 22 students are from Iraq, 17 students from Lebanon, 12 students from Tunis, 11 students from Saudi Arabia, 9 students from Egypt, 7 students from Syria, 6 students from USA, Iran and Libya, 4 students from Morocco and one student from Venezuela.

                The dataset is collected through two educational semesters: 245 student records are collected during the first semester and 235 student records are collected during the second semester.

                The data set includes also the school attendance feature such as the students are classified into two categories based on their absence days: 191 students exceed 7 absence days and 289 students their absence days under 7.

                This dataset includes also a new category of features; this feature is parent parturition in the educational process. Parent participation feature have two sub features: Parent Answering Survey and Parent School Satisfaction. There are 270 of the parents answered survey and 210 are not, 292 of the parents are satisfied from the school and 188 are not.
                """)
    st.markdown("""
                ##### Data Attributes:
                - 1- Gender: student's gender (nominal: 'Male' or 'Female')

                - 2- Nationality- student's nationality (nominal:' Kuwait',' Lebanon',' Egypt',' SaudiArabia',' USA',' Jordan','
                Venezuela',' Iran',' Tunis',' Morocco',' Syria',' Palestine',' Iraq',' Lybia')

                - 3- Place of birth- student's Place of birth (nominal:' Kuwait',' Lebanon',' Egypt',' SaudiArabia',' USA',' Jordan','
                Venezuela',' Iran',' Tunis',' Morocco',' Syria',' Palestine',' Iraq',' Lybia')

                - 4- Educational Stages- educational level student belongs (nominal: 'lowerlevel','MiddleSchool','HighSchool')

                - 5- Grade Levels- grade student belongs (nominal: 'G-01', 'G-02', 'G-03', 'G-04', 'G-05', 'G-06', 'G-07', 'G-08', 'G-09', 'G-10', 'G-11', 'G-12 ')

                - 6- Section ID- classroom student belongs (nominal:'A','B','C')

                - 7- Topic- course topic (nominal:' English',' Spanish', 'French',' Arabic',' IT',' Math',' Chemistry', 'Biology', 'Science',' History',' Quran',' Geology')

                - 8- Semester- school year semester (nominal:' First',' Second')

                - 9- Parent responsible for student (nominal:'mom','father')

                - 10- Raised hand- how many times the student raises his/her hand on classroom (numeric:0-100)

                - 11- Visited resources- how many times the student visits a course content(numeric:0-100)

                - 12- Viewing announcements-how many times the student checks the new announcements(numeric:0-100)

                - 13- Discussion groups- how many times the student participate on discussion groups (numeric:0-100)

                - 14- Parent Answering Survey- parent answered the surveys which are provided from school or not
                (nominal:'Yes','No')

                - 15- Parent School Satisfaction- the Degree of parent satisfaction from school(nominal:'Yes','No')

                - 16- Student Absence Days-the number of absence days for each student (nominal: above-7, under-7)
                """)
with st.expander("View Dataframe"):
    st.dataframe(df)
    
    
st.divider()
st.header("Request Form:")
# DEFAUL SETTING
scatter_kwargs = {"x": "Discussion", "y": "GradeID"}
# USER INTERFACE
layout = grid([5,1,1], vertical_align="center")
st.session_state.population_size  = layout.slider('Population Size', value=10, min_value=10, max_value=500, step=10, help="How many students do you want to use this solution on?")
st.session_state.error_margin  = layout.number_input('Margin of Error', value=5, min_value=0, step=1)
layout.metric("Sample Size", value=st.session_state.sample_size)

layout = grid(4, vertical_align="center")
show_gender = layout.toggle("Gender")
if show_gender:
    scatter_kwargs["color"] = "Gender"

show_stage = layout.toggle("Class")
if show_stage:
    scatter_kwargs["symbol"] = "Class"
    
show_discussion = layout.toggle("Impact")
if show_discussion:
    scatter_kwargs["size"] = "GradeID"

show_trend = layout.toggle("Trend")
if show_trend:
    scatter_kwargs["trendline"] = "ols"

show_trend = layout.toggle("Topic")
if show_trend:
    scatter_kwargs["facet_col"] = "Topic"
    
show_trend = layout.toggle("Stage")
if show_trend:
    scatter_kwargs["facet_row"] = "StageID"
    
show_trend = layout.toggle("LogX")
if show_trend:
    scatter_kwargs["log_x"] = "True"

show_trend = layout.toggle("LogY")
if show_trend:
    scatter_kwargs["log_y"] = "True"

st.session_state.sample_size = calculate_sample_size(st.session_state.population_size, st.session_state.error_margin)
df=df.head(st.session_state.population_size)
fig = px.scatter(df, **scatter_kwargs,
                 color_discrete_sequence=px.colors.qualitative.D3)


fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
fig.update_layout(showlegend=False)

st.plotly_chart(fig, theme="streamlit")

st.info(f"To use this solution for {st.session_state.population_size} students, with confidence level of {100-st.session_state.error_margin}%, we need data of **{st.session_state.sample_size}** students")
