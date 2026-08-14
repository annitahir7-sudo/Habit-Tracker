import streamlit as st
import tablebase
import datetime
st.set_page_config(page_title="Add Progress")
#Injecting CSS to add style
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
    div.st-key-v{
        background-color: #e9ffe9f4;
        border-radius: 10px;
        border-width: 5px;
        border-style: dashed;
        padding:10px;
    }
    div.st-key-x{
            background-color: #e9ffe9f4;
            border-radius: 10px;
            border-width: 5px;
            border-style: dashed;
            padding:10px;
    }
    div.st-key-prog{
            background-color: #e9ffe9f4;
            border-radius: 10px;
            border-width: 3px;
            border-style: solid;
            padding:10px;
        }
    </style>
""")




with st.container(key="prog"):
    st.title("Add Progress")
#Initializing user_id
if "user_id" in st.session_state:
    user_id = st.session_state["user_id"]
    user_id = user_id
else:
    user_id = False
day = datetime.datetime.now()
day = day.date()
connection = tablebase.connect()

#Check if the user has completed their goal and entered a valid amount
def progress(user_id, habit, amount, selected_date):
    goal = tablebase.return_goal(connection, user_id, habit)
    goal = goal[0]
    goal = float(goal)
    try:
        amount = float(amount)
        if amount > goal or amount==goal:
            completed = "Yes"
            st.balloons()
            st.success("Well done for completing your goal!!!")
        else:
            completed = "No"
            st.badge("Amazing effort !")
    except:
        st.write("Enter a valid amount")
        st.rerun()
    #Add the amount, date and habit into the table completion
    tablebase.add_progress(connection, user_id, selected_date, habit, completed, amount)
#Give the user a choice to choose current date or different date to log their progress on and add to compeltion table
def selected_date_func():
    selected_date = day
    st.divider()
    st.subheader("Date")
    st.write("Choose if you would like to record your progress for today or a previous day:")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            x =  st.button(day.strftime("%d %b %Y"))
    with col2:
        with st.container(border=True):
            prev = st.date_input("Select a date:", value = None)
    if x:
        selected_date = day
    elif prev:
        selected_date = prev
    st.divider()
    return selected_date
#Allows the user to add their progress for a habit
def add_habit_prog():
    habits = tablebase.see_habits(connection, user_id)
    if "reading_am" not in st.session_state:
        st.session_state.reading_am = None
    if "exercise_am" not in st.session_state:
        st.session_state.exercise_am = None
    if "water_am" not in st.session_state:
        st.session_state.water_am = None
    with st.container():
        #Show the habits the user has added
        for habit in habits:
            try:
                habit = habit[0]
            except:
                pass
            if "Reading" in habit:
                st.session_state.reading_am = True
            if "Exercise" in habit:
                st.session_state.exercise_am = True
            if "Water" in habit:
                st.session_state.water_am = True                      
            if "readingbt" not in st.session_state:
                st.session_state.readingbt = None
            if "exercisebt" not in st.session_state:
                st.session_state.exercisebt = None
            if "waterbt" not in st.session_state:
                st.session_state.waterbt = None
        #Add progress for the reading habit
        if st.session_state.reading_am and st.session_state.exercisebt == None and st.session_state.waterbt == None:
            if "reading_s" not in st.session_state:
                st.session_state.reading_s = None
            if st.session_state.reading_s == None:
                reading = st.button("Reading", icon = "📖", key="reading_bt")
                if reading:
                    st.session_state.readingbt = True
                    st.session_state.reading_s = True
                    st.rerun()
            if st.session_state.reading_s:
                st.header("Reading")
                if "date_st" not in st.session_state:
                    st.session_state.date_st = None
                selected_date = selected_date_func()
                if selected_date:
                    st.session_state.date_st = True
                if st.session_state.date_st == True:
                    with st.container(horizontal=True):
                        amount = st.number_input("Enter the length of time: ", value = None, placeholder ="...mins", key="reading_length")
                        submit = st.button(label="Add", key="reading_submit")
                        if submit:
                            progress(user_id, "Reading", amount, selected_date) 
        #Add the progress for the exercise habit           
        if st.session_state.exercise_am and st.session_state.readingbt == None and st.session_state.waterbt == None:
            if "exercise_s" not in st.session_state:
                st.session_state.exercise_s = None
            if st.session_state.exercise_s == None:
                exercise = st.button("Exercise", icon = "🏃‍♀️", key="exercise_bt")
                if exercise:
                    st.session_state.exercisebt = True
                    st.session_state.exercise_s = True
            if st.session_state.exercise_s:
                st.header("Exercise")
                if "date_st" not in st.session_state:
                    st.session_state.date_st = None
                selected_date = selected_date_func()
                if selected_date:
                    st.session_state.date_st = True
                if st.session_state.date_st == True:
                    with st.container(horizontal=True):
                        amount = st.number_input("Enter the length of time: ", value = None, placeholder ="...mins", key="exercise_length")
                        submit = st.button(label="Add", key="exercise_submit")
                        if submit:
                            progress(user_id, "Exercise", amount, selected_date)
        #Add the progress for the exercise habit
        if st.session_state.water_am and st.session_state.readingbt == None and st.session_state.exercisebt == None:
            if "water_s" not in st.session_state:
                st.session_state.water_s = None
            if st.session_state.water_s == None:
                water = st.button("Water", icon = "💧", key="water_bt")
                if water:
                    st.session_state.waterbt = True
                    st.session_state.water_s = True
            if st.session_state.water_s:
                st.header("Water")
                if "date_st" not in st.session_state:
                    st.session_state.date_st = None
                selected_date = selected_date_func()
                if selected_date:
                    st.session_state.date_st = True
                if st.session_state.date_st == True:
                    with st.container(horizontal=True):
                        amount = st.number_input("Enter the length of time: ", value = None, placeholder ="...ml", key="water_amount")
                        submit = st.button(label="Add", key="water_submit")
                        if submit:
                            progress(user_id, "Water", amount, selected_date)

     
def add_progress(user_id):
    prev_habits = tablebase.check_if_habits(connection, user_id)
    if prev_habits:
        if "add" not in st.session_state:
            st.session_state.add = None
        if st.session_state.add == None:
            st.divider()
            with st.container(horizontal = True):
                st.write("Add Progress")
                add = st.button("➕")
                st.divider()
                if add:
                    st.session_state.add = True
        if st.session_state.add:
            add_habit_prog()
    else:
        st.write("Add some habits in order to add progress!")

#Check user has logged in
if user_id:
    add_progress(user_id)
else:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ERROR!!!")
    st.write("Please Log in or Sign up")
    with col2:
        with st.container(key="v"):
            st.page_link("login.py", label="Log in", icon="🪵")
        with st.container(key="x"):
            st.page_link("signup.py", label="Sign up", icon="🛑")

#Go back to add more progress for habits
with st.bottom:
    go_bac = st.button("Back")
    if go_bac:
        st.session_state.reading_s = None
        st.session_state.readingbt = None
        st.session_state.exercisebt = None
        st.session_state.waterbt = None
        st.session_state.exercise_s = None
        st.session_state.water_s = None
        st.session_state.date_st = None
        st.session_state.add = None
        st.session_state.back = None
        st.rerun()