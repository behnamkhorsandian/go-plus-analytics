# ESSENTIALS
import json

# STREAMLIT
import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.app_logo import add_logo 
from streamlit_echarts import st_echarts


# --- PAGE CONFIG (BROWSER TAB) ---
st.set_page_config(page_title="GoPlus", page_icon=":robot_face:", layout="centered", initial_sidebar_state="expanded")
add_logo("images/gopluslogo.png", height=128)


# ---- LOAD ASSETS ----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")


# ---- LOAD DATABASE ----
with open("data/ielts_tags.json", "r") as f:
    ielts = json.loads(f.read())
for idx, _ in enumerate(ielts["children"]):
    ielts["children"][idx]["collapsed"] = idx % 2 != 0


# --- MAIN PAGE ---
with st.container():
    st.title("Data Cleaning")
    st.divider()
    layout = grid([1,3] , vertical_align="center")
    layout.image("images/data_cleaning_outline.png")
    layout.write('''
                Now, let's talk Data Cleaning. This is where our AI steps in to make your life easier. It sorts and tags all kinds of documents with your own tagging structure.
                There are three objectives in data cleaning:\n
                ''')
    
    st.write("#")
    st.image("images/data_cleaning_process.png")
    st.write("#")
    st.divider()


    treeA = {
        "name": "treeB",
        "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
        "series": [
            {
                "type": "tree",
                "data": [ielts],
                "top": "10%",
                "left": "15%",
                "bottom": "20%",
                "right": "15%",
                "symbolSize": 7,
                "layout":"orthogonal",
                "label": {
                    "position": "top",
                    "verticalAlign": "top",
                    "align": "right",
                    "fontSize": 16,
                    "color": "#fff",
                    "offset":[3,0]
                },
                "leaves": {
                    "label": {
                        "position": "right",
                        "verticalAlign": "middle",
                        "align": "left",
                        "distance":15,
                        "offset":[3,0]
                    }
                },
                "emphasis": {"focus": "descendant"},
                "expandAndCollapse": True,
                "animationDuration": 550,
                "animationDurationUpdate": 750,
            }
        ],
    }
    st_echarts(treeA, height="500px", key="treeA")

    

