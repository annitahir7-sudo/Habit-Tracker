import streamlit as st
import tablebase
connection = tablebase.connect()
st.html("""
    <style>
    div.st-key-add_habit{
        background-color: #e9ffe9f4;
        border-radius: 10px;
        border-width: 3px;
        border-style: solid;
        padding:10px;
    }
    div.st-key-click{
        border-top: 3px dotted #4f003d;
        border-bottom: 3px dotted #4f003d;
        padding: 10px;
        margin-bottom: 50px;
    }
    div.st-key-l{
        background-color: #e9ffe9f4;
        border-radius: 10px;
        border-width: 3px;
        border-style: dotted;
        padding:10px;
    }
    div.st-key-s{
            background-color: #e9ffe9f4;
            border-radius: 10px;
            border-width: 3px;
            border-style: dotted;
            padding:10px;
        }
    </style>
""")

st.set_page_config(page_title="Add Habits")
if "user_id" in st.session_state:
    user_id = st.session_state["user_id"]

else:
    user_id = False
#Fix pop up (on all with fun facts)

def reading_form(user_id):
    if "read_form" not in st.session_state:
        st.session_state.read_form = None
    if st.session_state.read_form == None:
        with st.form(key="reading"):
            st.subheader("Reading")
            with st.popover("Fun Fact"):
                st.write("The studies have shown that adults who regularly read fiction are more likely to engage in charity and volunteer work. Perhaps its time to replace the slogan “Make love, not war” with “Read fiction, not media”. Although media is often fiction, so it could get a little confusing.")
            goal = st.slider("Enter your goal time per day (mins) : ", 5, 1440 )
            st.divider()
            frequency = st.selectbox("Pick a frequency", ["Daily", "Weekly", "Monthly"])
            submitted = st.form_submit_button(label="Submit")
            if submitted:
                tablebase.add_habits(connection, user_id, "Reading", frequency, goal)
                st.session_state.read_form = True
    if st.session_state.read_form == True:
        st.subheader("Reading!!! Amazing!")
        st.caption("You can now pick another habit or add progress")
def exercise_form(user_id):
    if "exercise_form" not in st.session_state:
        st.session_state.exercise_form = None
    if st.session_state.exercise_form == None:
        with st.form(key="exercise"):
            st.subheader("Exercise")
            with st.popover("Fun Fact"):
                st.write("Not only does exercise improve your body, it helps your mental function by increasing serotonin in the brain, which leads to improved mental clarity.")
            goal = st.slider("Enter your goal time per day (mins) : ", 5, 1440 )
            name = st.radio("Enter the type of exercise: ", ["Cardio", "Strength", "Flexibility", "Other"])
            if name == "Other":
                type = st.text_input("Enter the exercise name: ")
            st.divider()
            frequency = st.selectbox("Pick a frequency", ["Daily", "Weekly", "Monthly"])
            submitted = st.form_submit_button(label="Submit")
            if submitted:
                tablebase.add_habits(connection,user_id, "Exercise", frequency, goal) 
                st.session_state.exercise_form = True
                st.subheader("Exercise! Excellent choice for physical as well as mental health")
                st.caption("You can now pick another habit or add progress")
def water_form(user_id):
    if "water_form" not in st.session_state:
        st.session_state.water_form = None
    if st.session_state.water_form == None:
        with st.form(key="water_form"):
            st.subheader("WATERRR")
            with st.popover("Fun Fact", width="stretch"):
                st.write("Water intake is associated with improved skin barrier. With dehydration, the skin can become more vulnerable to skin disorders.")
            goal = st.slider("Enter your goal amount (ml):",0, 3000, 2000)
            st.divider()
            frequency = st.selectbox("Pick a frequency", ["Daily", "Weekly", "Monthly"])
            submitted = st.form_submit_button(label="Submit")
            if submitted:
                tablebase.add_habits(connection,user_id, "Water", frequency, goal)
                st.session_state.water_form = True
    if st.session_state.water_form == True:
            st.subheader("Drinking enough water is often underestimated. Well done!")
            st.caption("You can now pick another habit or add progress")

def main(user_id):
    habits = tablebase.see_habits(connection, user_id)
    if "selected_form" not in st.session_state:
        st.session_state.selected_form = None
    with st.container(horizontal=True):
        reading = st.button("📖", width ="stretch")
        exercise = st.button("🏃‍♀️", width ="stretch")
        water = st.button("💧", width ="stretch")
        if "rtrue" not in st.session_state:
            st.session_state.rtrue = None
        if "etrue" not in st.session_state:
            st.session_state.rtrue = None
        if "wtrue" not in st.session_state:
            st.session_state.rtrue = None
        for habit in habits:
            try:
                habit = habit[0]
            except:
                pass
            if "Reading" in habit:
                st.session_state.rtrue = True
            if "Exercise" in habit:
                st.session_state.etrue = True
            if "Water" in habit:
                st.session_state.wtrue = True
            
    if reading:
        if st.session_state.rtrue == True:
            st.badge("Already Added habit", color="red")
        else:
            st.session_state.selected_form = "reading"
    elif exercise:
        if st.session_state.etrue == True:
            st.badge("Already Added habit", color="yellow")
        else:
            st.session_state.selected_form = "exercise"
    elif water:
        if st.session_state.wtrue == True:
            st.badge("Already Added habit", color="blue")
        else:
            st.session_state.selected_form = "water"
    if st.session_state.selected_form == "reading":
        if user_id:
            reading_form(user_id)
    elif st.session_state.selected_form == "exercise":
        if user_id:
            exercise_form(user_id)
    elif st.session_state.selected_form == "water":
        if user_id:
            water_form(user_id)
    st.divider()
    #Add some more stuff or make it manually switch to another tab

with st.container(key="add_habit"):
    st.header("Add Habits")
with st.container(key="click"):
    st.write("Click on one of the buttons to add a new habit.")

if user_id:
    main(user_id)
else:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ERROR!!!")
        st.write("Please Log in or Sign up")
    with col2:
        with st.container(key="l"):
            st.page_link("login.py", label="Log in", icon="🪵")
        with st.container(key="s"):
            st.page_link("signup.py", label="Sign up", icon="🛑")

connection.close()
