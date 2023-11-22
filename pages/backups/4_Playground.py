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
    st.title("Data Playground")

# FUNCTION  
def calculate_sample_size(N, e):
    n = N / (1 + N * (e/100)**2)
    return round(n)
    

# DataCollection:
df = pd.read_csv("assets/kaggle_education.csv")
# DataCleaning:
df['GradeID'] = df['GradeID'].apply(lambda x: int(x.split('-')[1]))
df['Nutralized_Discussion'] = df['Discussion'].apply(lambda x: x / df['Discussion'].max())
df['Nutralized_RaisedHands'] = df['RaisedHands'].apply(lambda x: x / df['RaisedHands'].max())
df['Nutralized_ResourcesVisited'] = df['ResourcesVisited'].apply(lambda x: x / df['ResourcesVisited'].max())
df['Nutralized_AnnouncementsViews'] = df['AnnouncementsViews'].apply(lambda x: x / df['AnnouncementsViews'].max())

df = df.reset_index()


st.dataframe(df)
    
coloring_modes = {
    'Dark24': px.colors.qualitative.Dark24,
    'Light24': px.colors.qualitative.Light24,
    'Plotly': px.colors.qualitative.Plotly,
    'Pastel': px.colors.qualitative.Pastel,
    'Safe': px.colors.qualitative.Safe,
    'Vivid': px.colors.qualitative.Vivid,
    'Alphabet': px.colors.qualitative.Alphabet,
    'G10': px.colors.qualitative.G10,
    'T10': px.colors.qualitative.T10,
    'D3': px.colors.qualitative.D3
}

marginal_options = {
    'None': None,
    'Histogram': 'histogram',
    'Rug': 'rug',
    'Box': 'box',
    'Violin': 'violin'
}

column_dict = {col: col for col in df.columns}
quality_columns = [col for col in df.columns if df[col].dtype == 'object']
quantity_columns = [col for col in df.columns if df[col].dtype != 'object']
quality_dict = {col: col for col in quality_columns}
quantity_dict = {col: col for col in quantity_columns}

    
st.divider()
st.header("Request Form:")
# DEFAUL SETTING
scatter_kwargs = {"x": "index", "y": "GradeID"}
# USER INTERFACE
layout = grid([5,1,1], vertical_align="center")
st.session_state.population_size  = layout.slider('Population Size', value=10, min_value=10, max_value=500, step=10, help="How many students do you want to use this solution on?")
st.session_state.error_margin  = layout.number_input('Margin of Error', value=5, min_value=0, step=1)
layout.metric("Sample Size", value=st.session_state.sample_size)

# X-AXIS SETTING:
layout = grid(4, vertical_align="center")
xAxis = layout.selectbox('X-Axis', list(quantity_dict.keys()), index=0)
xSecondaryType = layout.selectbox('Select Marginal X Type', list(marginal_options.keys()), index=0)
xSecondary = layout.selectbox('Marginal X', ["Active", "Deactive"], index=1)
LogX = layout.selectbox('Log X', ["Active", "Deactive"], index=1)
if xSecondary=="Active":
    scatter_kwargs["marginal_x"] = xSecondaryType
if LogX=="Active":
    scatter_kwargs["log_x"] = "True"
    
# Y-AXIS SETTING:
layout = grid(4, vertical_align="center")
yAxis = layout.selectbox('Y-Axis', list(quantity_dict.keys()), index=1)
ySecondaryType = layout.selectbox('Select Marginal Y Type', list(marginal_options.keys()), index=0)
ySecondary = layout.selectbox('Marginal Y', ["Active", "Deactive"], index=1)
LogY = layout.selectbox('Log Y', ["Active", "Deactive"], index=1)
if ySecondary=="Active":
    scatter_kwargs["marginal_y"] = ySecondaryType
if LogY=="Active":
    scatter_kwargs["log_y"] = "True"

# COLORS SETTING:
layout = grid(3, vertical_align="center")
coloring_option = layout.selectbox('Enable Colors', ["Active", "Deactive"], index=1)
coloring_mode = layout.selectbox('Coloring Mode', list(coloring_modes.keys()), index=0)
coloring_source = layout.selectbox('Coloring Logic', list(quality_dict.keys()), index=0)
if coloring_option=="Active":
    scatter_kwargs["color"] = coloring_source
    
# SIZE SETTING:
layout = grid(3, vertical_align="center")
size_option = layout.selectbox('Enable Size', ["Active", "Deactive"], index=1)
size_source = layout.selectbox('Size Logic', list(quantity_dict.keys()), index=0)
size_mode = layout.selectbox('Size Mode', ["Actual", "Nutral"], index=0)
if size_mode=="Nutral":
    df[size_source]=df[size_source].apply(lambda x: x / df[size_source].max())
if size_option=="Active":
    scatter_kwargs["size"] = size_source
    
# # OPACITY SETTING:
# layout = grid(3, vertical_align="center")
# size_option = layout.selectbox('Enable Colors', ["Active", "Deactive"], index=0)
# size_source = layout.selectbox('Coloring Logic', list(quantity_dict.keys()), index=0)
# size_mode = layout.selectbox('Coloring Mode', ["Actual", "Nutral"], index=0)
# if size_mode=="Nutral":
#     df[size_source]=df[size_source].apply(lambda x: x / df[size_source].max())
# if size_option=="Active":
#     scatter_kwargs["size"] = size_source
    

st.session_state.sample_size = calculate_sample_size(st.session_state.population_size, st.session_state.error_margin)
df=df.head(st.session_state.population_size)

fig = px.scatter(df, **scatter_kwargs,
                #  color_discrete_sequence=coloring_modes[coloring_mode]
                 )
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
fig.update_layout(showlegend=False)

st.plotly_chart(fig, theme="streamlit")

st.info(f"To use this solution for {st.session_state.population_size} students, with confidence level of {100-st.session_state.error_margin}%, we need data of **{st.session_state.sample_size}** students")
