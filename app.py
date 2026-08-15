import streamlit as st
import tablebase
#Injecting CSS
st.html("""
    <style>
    .stMainBlockContainer {
        padding-top: 5rem !important;
    }
    div.st-key-info {
        background-color: #e9ffe9f4;
        border-color: #4f003d;
        border-radius: 10px;
        border-width: 3px;
        border-style: solid;
        padding: 10px;
        padding-bottom: 30px;
    }
    div.st-key-title{
        border-bottom: 2px dotted #4f003d;
    }
    div.st-key-sub{
        border-top: 3px dotted #4f003d;
        border-bottom: 3px dotted #4f003d;
        padding: 10px;
        margin-bottom: 50px;
    }
    div.st-key-habit{
        background-color: #e9ffe9f4;
        border-radius: 10px;
        border-width: 3px;
        border-style: solid;
        padding:10px;
    }
    </style>
""")




if "user_id" in st.session_state:
    user_id = st.session_state["user_id"]
    user_id = user_id
else:
    user_id = False
st.set_page_config(page_title="Home")
connection = tablebase.connect()
tablebase.create_completion_table(connection)
tablebase.create_user_table(connection)
tablebase.create_habits_table(connection)
with st.container(key="habit"):
    st.title("Habit Tracker")
with st.container(key="sub"):    
    st.write("Hii! This is a tracker for tracking your water intake, exercise and reading time in order to encourage you to be a little more productive!")
col1, col2= st.columns(2)


with st.container(key = "ainfo"):
    with col1:
        st.write("Habit tracking naturally builds a series of visual cues. When you look at the calendar and see your streak, you will be reminded to act again [...] A habit tracker is a simple way to log your behavior, and the mere act of tracking a behavior can spark the urge to change it.")
        st.page_link("https://jamesclear.com/habit-tracker", label="-James Clear (Author of Atomic Habits)")
    with col2:
        #Table of contents with links to importance of water, reading and exercise
        with st.container(key="info"):
            with st.container(key="title"):
                st.subheader("Information:")
            st.page_link("https://www.healthline.com/health/food-nutrition/why-is-water-important", label="Importance of Water", icon="📖")
            st.page_link("https://www.95percentgroup.com/insights/reading-importance/", label="Importance of Reading", icon="🏃‍♀️")
            st.page_link("https://www.mayoclinic.org/healthy-lifestyle/fitness/in-depth/exercise/art-20048389", label="Importance of Exercise", icon="💧")

    

connection.close()