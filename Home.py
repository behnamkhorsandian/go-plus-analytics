# STREAMLIT
import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.app_logo import add_logo


# --- PAGE CONFIG (BROWSER TAB) ---
st.set_page_config(page_title="GoPlus", page_icon=":robot_face:",
                   layout="centered", initial_sidebar_state="expanded")
add_logo("images/gopluslogo.png", height=128)


# ---- LOAD ASSETS ----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")


# --- MAIN PAGE ---
with st.container():
        st.title("GoPlus Analytics")

        st.write('''
            Welcome to GoPlus, your gateway to next-level learning through the power of AI. \n
            In the following presentation, we have decided to use the **4D Framework** which is the prefect workflow for data-driven solutions.
             ''')

        st.write('''
            ## 4D Framework:
            
            When you are in a data driven project, the process can often feel like an endless maze with multiple potential path to follow. \n
            The right question can provide direction and purpose. But on the other hand, if you are not prepared enough for how you are going to approach your data, you can easily get lost in the process. \n
            The 4D (four dimensions) framework can serve as a guide as you navigate through the project.
             ''')

        st.divider()
        st.image("images/4d_framework.png")
        st.divider()
        
        st.write('''
                For each unique audience and priject, the four dimensions of the framework can give critical context and keep the analytics more focused.
                So Lets explain the tailor made version of this framework for this project:
                ''')
        
        layout = grid([1, 6], vertical_align="center")
        layout.image("images/4d_client.png")
        layout.write('''
                #
                ### Client:  Al Maarifah Colleges (Medical)
                #
                ''')
        
        layout.image("images/4d_problem.png")
        layout.write('''
                #
                ### Problem:
                How to identify the gaps in students performance across the different subjects and domains to be able to provide personalized solutions to enhance the performance of each student.
                #
                ''')
        
        layout.image("images/4d_outcome.png")
        layout.write('''
                #
             ### Outcome:
             Enhance Student's scores in standardized tests - this will have a direct impact on the perception of the school.
             #
             ''')

        st.divider()
        st.write('''
             ### KPI & Metrics:
             Tools we can use to highlight the problem, monitor the effectiveness, and define the achievement of the desired outcome.
             This is the part that clients start to interect with our platform.
             Out solution provides a visualization of all data points in easy to understand format with the ability to interact with the platform through questions to obtain the desired data on the fly. 
             #
             ''')
        st.image("images/metrics.png")

        st.info("This is the part that we present our progress on the **solutions** to you and get your feedback.")
        st.divider()
        
        layout = grid([1, 6], vertical_align="center")
        layout.image("images/4d_solution.png")
        layout.write('''
                ### Solution:
                To give you an idea of how we do this, let's take a look at our workflow, briefly captured in the chart you see on the screen.\n
                ''')
        st.write('''
                This chart is more than just a visual, it's the backbone of the presentation and, more importantly, it's how our solution is going to work at it's core. 
                \n We'll use a simple demo to walk you through the technical steps of our project with you:
                ''')
        st.image("images/goplus_workflow.png")