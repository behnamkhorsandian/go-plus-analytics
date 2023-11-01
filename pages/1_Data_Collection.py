# ESSENTIALS
import time

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
    st.title("Data Collection")
    st.divider()
    layout = grid([1,3] , vertical_align="center")
    layout.image("images/data_collection_outline.png")
    layout.write('''
                First up is Data Collection. In GoPlus, you can upload a variety of formats—PDFs, Excel files, videos, you name it. 
                They can be Question banks, Grades, or resources.\n
                There are two ways to use our solution for your system:\n\n
                #
                ''')
    
    
    st.image("images/data_collection_process.png")
    st.divider()
    
    layout = grid([1,1] , vertical_align="center")
    with layout.container():
        st.write('''
                 ### `Using via API`
                 point 1: this this this this that that that that this this this this.
                 point 2: this this this this that that that that this this this this.
                 point 3: this this this this that that that that this this this this.
                 ''')
    
    with layout.container():
        st.write('''
                 ### `Accessing DB`
                 point 1: this this this this that that that that this this this this.
                 point 2: this this this this that that that that this this this this.
                 point 3: this this this this that that that that this this this this.
                 ''')
    
    st.divider() 
    st.write('''
            For this demo we are going to upload the files the same way you can do in our platform.
            ''')
    st.image("images/data_collection.png")
    
   

    
    # FILE UPLOAD
    with st.form("Feed"):
        files = st.file_uploader("Resources:", type=['pdf', 'csv', 'mp4'], accept_multiple_files=True, help="Article files you want to autotag.")
        
        if st.form_submit_button("Upload and Process", use_container_width=True):
            buffer = st.progress(0.0, text="AI Analysis in progress...")
            count = 0
            for file in files:
                time.sleep(1)
                st.toast("something")
                count += 1
                buffer.progress((count/len(files)), text=f"AI Analysis in progress: {count} of {len(files)}")
            buffer.empty()
            st.success("Done!")
        
