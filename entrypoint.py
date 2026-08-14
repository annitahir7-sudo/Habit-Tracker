import streamlit as st

st.logo("💗", size = "large")
home = st.Page("app.py", title=" ____Home____", icon="🏡")
sign_up = st.Page("signup.py", title="____Sign up____",icon="🔑")
login = st.Page("login.py", title="____Login____", icon="🌸")
add_habits = st.Page("add_habits.py", title="____Add Habits____", icon="🫙")
add_progress = st.Page("add_progress.py", title="____Add Progress____", icon="🏗️")
visual_habit_analysis = st.Page("visual_habit_analysis.py", title = "____Visual Analysis____", icon="📈")
pg = st.navigation([home, sign_up, login, add_habits, add_progress, visual_habit_analysis], position = "top")
pg.run()

with st.sidebar:
    with st.expander("Book Recs", icon="📚"):
        st.page_link("https://jamesclear.com/atomic-habits", label ="Atomic Habits", icon="⚛️")
        st.page_link("https://www.amazon.co.uk/Getting-Things-Done-Stress-free-Productivity/dp/0349408947", label = "Getting Thingss Done",icon="🔨")
        st.page_link("https://www.amazon.co.uk/Eat-That-Frog-Important-Things/dp/1444765426", label = "Eat That Frog",icon="🐸")
    st.image("https://images.unsplash.com/photo-1566847438217-76e82d383f84?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    st.caption("CUTEEEEE CATS ARGH")
    st.caption("Photo by The Lucky Neko")
    st.subheader("How would you rate this tracker:")
    st.caption("(The cats are 100% not there to influence your decisions.)")
    satisfaction = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")
    if selected is not None:
        st.write("Thank you for your feedback!")
#with st.bottom:
   # st.caption("HABIT TRACKER")