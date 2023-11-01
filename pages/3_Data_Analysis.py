# ESSENTIALS
import json

# STREAMLIT
import streamlit as st
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
with open("data/topics_graph.json", "r") as f:
    graph = json.loads(f.read())
    
for idx, node in enumerate(graph["nodes"]):
    graph["nodes"][idx]["label"] = {"show": node["symbolSize"] > 30}
    

# --- MAIN PAGE ---
with st.container():
    st.title("⛓️ Data Analysis")
    st.image("images/data_analysis.png")
    st.write('''
             Moving on to Data Analysis. Our AI will generate a live quiz based on your uploaded resources. You'll get 5 multiple-choice questions and a long-answer question to test your knowledge. And here's the interactive part: we'll project a QR code on the screen. Scan it, and you're instantly taken to the quiz. You have 2 minutes to complete it. It's a quick and effective way to measure understanding.
             ''')
    

st.divider()
with st.container():
    st.write("### Resource Evaluation:")

    topics_graph = {
        "title": {
            "text": "",
            "subtext": "",
            "top": "bottom",
            "left": "right",
            "color": "#fff",
        },
        "tooltip": {},
        "legend": [{"data": [a["name"] for a in graph["categories"]]}],
        "animationDuration": 1500,
        "animationEasingUpdate": "quinticInOut",
        "series": [
            {
                "name": "Les Miserables",
                "type": "graph",
                "layout": "circular",
                "data": graph["nodes"],
                "links": graph["links"],
                "categories": graph["categories"],
                "roam": True,
                "label": {"position": "right", "formatter": "{b}"},
                "lineStyle": {"color": "source", "curveness": 0.3},
                "emphasis": {"focus": "adjacency", "lineStyle": {"width": 10}},
            }
        ],
    }
    st_echarts(topics_graph, height="500px")
    