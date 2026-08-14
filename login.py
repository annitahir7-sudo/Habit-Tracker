import streamlit as st
import app
import tablebase
connection = tablebase.connect()
st.set_page_config(page_title= "Log in")

if "login" not in st.session_state:
    st.session_state.login = None
if st.session_state.login == None:
    with st.form(key="log_in"):
        st.subheader("Log in")
        username = st.text_input("Enter your username: ")
        password = st.text_input("Enter your Password: ")
        submitted = st.form_submit_button(label="Submit")
        if submitted:
            try:
                user_id = tablebase.return_user_id(connection, username)
                st.session_state["user_id"] = user_id
                if tablebase.check_password(connection, username, password):
                    st.session_state.login = True
            except:
                st.write("Username or password not correct")

if st.session_state.login == True:
    col1, col2, = st.columns(2)
    with col1:
        st.divider()
        st.image("https://illust8.com/wp-content/uploads/2022/12/cat_chashiro_temaneki_17680.png", width = 500)
        st.divider()
    with col2:
        st.divider()
        st.subheader("LOGGED IN!")
        st.divider()
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("add_progress.py", label="Add Progress", icon="➕")
        st.page_link("visual_habit_analysis.py", label="Visual analysis of your progress", icon="📈")
        st.divider()
        