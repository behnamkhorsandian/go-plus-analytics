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

# --- MAIN PAGE ---
with st.container():
    st.title("GoPlus Analytics Demo")
    
    st.write('''
            Welcome to GoPlus, your gateway to next-level learning through the power of AI. \n
            In the following presentation, we have decided to use the **4D Framework** which is the prefect way to demonstrate a data-driven solution for the clients.
             ''')

    st.image("images/4d_framework.png")
    
    st.write('''
             ## Problem:
             How to identify the gaps in students performance across the different subjects and domains to be able to provide personalized solutions to enhance the performance of each student.
             ''')
    
    st.write('''
             ## Outcome:
             Enhance Student's scores in standardized tests - this will have a direct impact on the perception of the school.
             ''')
    
    st.write('''
             ## Metrics:
             Tools we can use to highlight the problem, monitor the effectiveness, and define the achievement of the desired outcome.
             This is the part that clients start to interect with our platform.
             Out solution provides a visualization of all data points in easy to understand format with the ability to interact with the platform through questions to obtain the desired data on the fly. 
             ''')
    
    st.write('''
             ## Solution:
             To give you an idea of how we do this, let's take a look at our workflow, beautifully captured in the chart you see on the screen.
             ''')
    
    st.image("images/goplus_workflow.png")
    
    st.write('''
            This chart is more than just a visual; it's the backbone of today's demo and, more importantly, it's how GoPlus functions at its core. We'll use a simple demo to walk you through each step for the rest of the presentation.
             ''')
    
    st.divider()
    layout = grid([1,3] , vertical_align="center")
    
    layout.image("images/data_collection_outline.png")
    layout.write('''
            ##### **`Data Collection`**\n
            Here's where we gather all the educational resources. Think of it as the 'input' stage for our AI.
             ''')
    
    layout.image("images/data_cleaning_outline.png")
    layout.write('''
            ##### `Data Cleaning`\n
            Our AI sorts and tags everything, making it easy to find what you're looking for later.
             ''')
    
    layout.image("images/data_analysis_outline.png")
    layout.write('''
            ##### `Data Analysis`\n
            Next, the AI creates a live quiz, offering real-time insights into your understanding of the material.
             ''')
    
    layout.image("images/data_interpretation_outline.png")
    layout.write('''
            ##### `Data Interpretation`\n
            The results from the quiz are then analyzed to provide you with valuable feedback.
             ''')
    
    layout.image("images/data_visualization_outline.png")
    layout.write('''
            ##### `Data Visualization`\n
            Finally, all this data is turned into easy-to-understand visuals, giving you a clear picture of where you stand.
             ''')
    
    st.write('''
            \n
            ---
            ###### *So, that's the roadmap for today. Each step on this chart is a part of the live demo you're about to experience, making it a practical walkthrough of what GoPlus can do for you.*
             ''')
    
    pass

