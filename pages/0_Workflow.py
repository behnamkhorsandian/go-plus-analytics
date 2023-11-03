# STREAMLIT
import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.app_logo import add_logo
from streamlit_echarts import st_echarts

import pandas as pd
import random
import numpy as np

import time
import json


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
if 'fresh' not in st.session_state:
    st.session_state.fresh = True
    st.session_state.database =  pd.DataFrame()
    st.session_state.cleaned =  pd.DataFrame()
    st.session_state.raw =  {}
    



# --- MAIN PAGE ---
with st.container():
    st.title("Playground")
    
    st.write("#")
    st.warning('''
            > ### *"Data! Data! Data!" he cried impatiently. "I can't make bricks without clay."*
            >
            > -- Sherlock Holmes by Sir Arthur Conan Doyle
             ''')
    st.write("#")
    
    st.write("## Data Collection")
    st.image("images/data_collection.png")
    st.write('''
                First up is Data Collection. In GoPlus, you can upload a variety of formats—PDFs, Excel files, videos, you name it. 
                They can be Question banks, Grades, or resources.\n
                There are two ways to use our solution for your system:\n\n
                #
                ''')
    
    
    st.image("images/data_collection_process.png")
    st.write("#")
    
    layout = grid([1,1] , vertical_align="center")
    with layout.container():
        st.write('''
                 ### Using via API
                 - ✅ Ease of Implementation
                 - ✅ Automatic Updates
                 - ✅ Scalability 
                 ''')

    
    with layout.container():
        st.write('''
                 ### Accessing DB
                 - ✅ Full Customization
                 - ✅ Independence
                 - ✅ Data Security
                 ''')
    st.write("#")
    

    # DATA COLLECTION
    with st.form("Collect"):
        files = st.file_uploader("Data Collection Demo", type=['csv'], accept_multiple_files=False, help="This is just for demo, you can generate random file instead of uploading")
        
        if st.form_submit_button("Collect", use_container_width=True):
            buffer = st.progress(0.0, text="Data Collecting in process...")
            if files:
                df = pd.read_csv(files)
            else:
                np.random.seed(random.randint(1, 100))
                data = {
                    "Name": [f"Student_{i+1}" for i in range(100)],
                    "Year": [random.choice(["First Year", "Second Year"]) for _ in range(100)],
                    "Program": [random.choice(["School A", "School B"]) for _ in range(100)],
                    "Region": [random.choice(["East", "West"]) for _ in range(100)],
                    "Gender": [random.choice(["Male", "Female"]) for _ in range(100)],
                    "Age": [random.randint(18, 25) for _ in range(100)],
                    "Course_A": [random.choice(["A", "B", "C", "D"]) for _ in range(100)],
                    "Course_B": [random.randint(60, 100) for _ in range(100)],
                    "Exam_Time": [round(random.uniform(15.125, 25.325), 3) for _ in range(100)],
                    "Quiz_Time": [str(random.randint(0, 2))+":"+str(random.randrange(0, 55, 5)) for _ in range(100)],
                }
                df = pd.DataFrame(data)
                df.to_csv("assets/student_performance.csv", index=False)
                
            st.session_state.database = df
            for i in range(25):
                time.sleep(0.05)
                i += 1
                buffer.progress((i/25), text=f"Data Collecting in process...")
            buffer.empty()
            st.dataframe(st.session_state.database)
    st.write("#")
    
    
    st.divider()
    st.write("## Data Collection")
    st.image("images/data_cleaning.png")
    st.write('''
                Now, let's talk Data Cleaning. 
                \n Most of the platforms skip this step go straight to the beautiful charts and graphs. To be honest, we understand in is that the case, because it's a time consuming process.
                \n This is where our AI steps in to make your life easier. It sorts and tags all kinds of documents with your own tagging structure.
                There are three objectives in data cleaning:\n
                ''')
    
    st.write("#")
    st.image("images/data_cleaning_process.png")
    st.write("#")
    

    st.write('''
            ### Normalizing Data:
            In this step we are going to map the data to a more standard `format`, so you can utilize external data for comparing and training purposes as well. \n
            For example in the given dataframe, **Grades** and **Time** columns are not in a uniform shape:
            ''')
    
    # DATA NORMALIZING
    with st.form("Normalize"):
        col = grid([1, 1], vertical_align="center")
        col.code('''
                # Time Formats:
                `01:10` --> `70000ms`
                ''' , language="markdown")
        col.code('''
                # Grade Formats:
                `A` --> `100%`
                ''' , language="markdown")
        if st.form_submit_button("Clean", use_container_width=True):
            with st.spinner("Cleaning in progress..."):
                np.random.seed(random.randint(1, 100))
                data = {
                    "Name": [f"Student_{i+1}" for i in range(100)],
                    "Year": [random.choice(["First Year", "Second Year"]) for _ in range(100)],
                    "Program": [random.choice(["School A", "School B"]) for _ in range(100)],
                    "Region": [random.choice(["East", "West"]) for _ in range(100)],
                    "Gender": [random.choice(["Male", "Female"]) for _ in range(100)],
                    "Age": [random.randint(18, 25) for _ in range(100)],
                    "Course_A": [str(random.randint(20, 60))+"%" for _ in range(100)],
                    "Course_B": [str(random.randint(60, 100))+"%" for _ in range(100)],
                    "Exam_Time": [str(round(random.randint(15000, 60000), 3))+" ms" for _ in range(100)],
                    "Quiz_Time": [str(round(random.randint(15000, 60000), 3))+" ms" for _ in range(100)]
                }
                time.sleep(2)
            df = pd.DataFrame(data)
            df.to_csv("assets/student_performance_CLEANED.csv", index=False)
            st.session_state.cleaned = df
            st.toast("Cleaned!")
            st.dataframe(df)
            
            
    st.write('''
            #
            ### Slicing Data:
            In this step we are going to slice our data based on multiple factors. The goal in this step is to divid our data by their `types`. In this case, our slicces can be like this:
            ''')
    
    # DATA SLICING
    with st.form("Slice"):
        col = grid([1, 1, 1], vertical_align="center")
        col.code('''
                "Student":{
                    "Gender": "M/F",
                    "Age": 20,
                    "Contry": 🇦🇪
                    "Year": 2
                    }
                ''' , language="json")
        
        col.code('''
                "Programs":{
                    "School": "A",
                    "Courses": [
                        "X", "Y", "Z"    
                        ]
                    }
                ''' , language="json")
        col.code('''
                "Courses":{
                    "Sub-Topics": [
                        "A", "B", "C"],
                    "Objectives": [
                        "A-1", "A-2"]
                    }
                ''' , language="json")

        if st.form_submit_button("Slice", use_container_width=True):
            with st.spinner("Slicing in progress..."):
                df = st.session_state.cleaned
                df.to_json("assets/student_performance.json", orient='records', lines=True)
                st.session_state.raw = json.loads(df.to_json(orient='records'))
            st.json(st.session_state.raw, expanded=False)

    st.write('''
            #
            ### Tagging Data:
            In this step we are going to 
            ''')
    
    # DATA TAGGING
    with st.form("Tag"):
        st.image("images/tagging_system.png")
        if st.form_submit_button("Tag", use_container_width=True):
            with st.spinner("Tagging in progress..."):
                with open("data/students.json", "r") as f:
                    students = json.loads(f.read())
                for idx, _ in enumerate(students["children"]):
                    students["children"][idx]["collapsed"] = idx % 2 != 0
                studentsTree = {
                    "name": "studentsTree",
                    "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
                    "series": [
                        {
                            "type": "tree",
                            "data": [students],
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
                st_echarts(studentsTree, height="600px", key="studentsTree")
    
    
    st.divider()
    st.write("## Data Analysis")
    st.image("images/data_analysis.png")
    st.write('''
                Moving on to Data Analysis.
                \n This is the part 
                ''')
    
    st.write("#")
    st.image("images/analysis.png")
    st.write("#")
    
    
    with open("data/topics_graph.json", "r") as f:
        graph = json.loads(f.read())
    for idx, node in enumerate(graph["nodes"]):
        graph["nodes"][idx]["label"] = {"show": node["symbolSize"] > 30}
    
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
    
    
    
    
    
    st.divider()
    st.write("## Data Interpretation")
    st.image("images/data_interpretation.png")
    st.write('''
                Now, let's talk Data Cleaning. 
                \n Most of the platforms skip this step go straight to the beautiful charts and graphs. To be honest, we understand in is that the case, because it's a time consuming process.
                \n This is where our AI steps in to make your life easier. It sorts and tags all kinds of documents with your own tagging structure.
                There are three objectives in data cleaning:\n
                ''')
    
    st.write("#")
    st.image("images/data_cleaning_process.png")
    st.write("#")
    

    st.divider()
    st.write("## Data Visualization")
    st.image("images/data_visualization.png")
    st.write('''
                Now, let's talk Data Cleaning. 
                \n Most of the platforms skip this step go straight to the beautiful charts and graphs. To be honest, we understand in is that the case, because it's a time consuming process.
                \n This is where our AI steps in to make your life easier. It sorts and tags all kinds of documents with your own tagging structure.
                There are three objectives in data cleaning:\n
                ''')
    
    st.write("#")
    st.image("images/data_cleaning_process.png")
    st.write("#")
    
    
    