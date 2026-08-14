import streamlit as st
import app
import tablebase
connection = tablebase.connect()
st.html("""
    <style>
    div.st-key-sgi {
        background-color: #e9ffe9f4;
        border-color: #4f003d;
        border-radius: 10px;
        border-width: 3px;
        border-style: solid;
        padding: 10px;
        padding-bottom: 30px;
    }
    </style>
""")





st.set_page_config(page_title= "Sign up")
if "sign" not in st.session_state:
    st.session_state.sign = None
if st.session_state.sign == None:
    with st.form(key="sign_up"):
        st.subheader("Sign up")
        username = st.text_input("Enter your username: ")
        password = st.text_input("Enter your Password: ")   
        submitted = st.form_submit_button(label="Submit")
        if submitted:
            if tablebase.check_username(connection, username):
                st.write("Username already exists - pick another username")
            else:
                hashed_password = tablebase.hash_password(password)
                tablebase.add_users(connection, username, hashed_password)
                user_id = tablebase.return_user_id(connection, username)
                st.session_state["user_id"] = user_id
                st.session_state.sign = True


if st.session_state.sign == True:
    col1, col2, = st.columns(2)
    with col1:
        st.divider()
        st.image("https://i.pinimg.com/736x/fe/96/83/fe9683a84d774ea541980ea7b5afc25b.jpg", width = 500)
        st.divider()
    with col2:
        st.divider()
        st.subheader("SIGNED IN!")
        st.write("Thank you for joining habit tracker")
        st.divider()
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("add_progress.py", label="Add Progress", icon="➕")
        st.page_link("visual_habit_analysis.py", label="Visual analysis of your progress", icon="📈")
        st.divider()
        

