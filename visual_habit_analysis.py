import streamlit as st
import tablebase
import pandas as pd
import altair as alt
connection = tablebase.connect()
#Inject CSS
st.html("""
    <style>
    div.st-key-q{
        background-color: #e9ffe9f4;
        border-radius: 10px;
        border-width: 3px;
        border-style: dotted;
        padding:10px;
    }
    div.st-key-w{
            background-color: #e9ffe9f4;
            border-radius: 10px;
            border-width: 3px;
            border-style: dotted;
            padding:10px;
    }
    div.st-key-visual{
            background-color: #e9ffe9f4;
            border-radius: 10px;
            border-width: 3px;
            border-style: solid;
            padding:10px;
        }
    </style>
""")




#user_id initialization
if "user_id" in st.session_state:
    user_id = st.session_state["user_id"]
    try:
        user_id = user_id[0]
    except:
        pass
else:
    user_id = False


with st.container(key="visual"):
    st.header("Visual Progress")

#Puts the results of the sql query in a pandas dataframe 
def reading_chart(user_id):
    reading = pd.read_sql_query("""
                        SELECT habit, amount, date
                        FROM completion
                        WHERE user_id = ?
                        """, connection, params=(user_id,))
    
    return reading

reading_df = reading_chart(user_id)

#Lets the chart detect when the mouse is hovering over a point
hover = alt.selection_point(
    fields=["date"],
    nearest = True,
    on="mouseover",
    empty = "none",  
)

#Defines the line chart
lines = (
    alt.Chart(reading_df, title="x").mark_line().encode(
        x="date",
        y="amount",
        color = "habit"
    )
)
points = lines.transform_filter(hover).mark_circle(size=65)
tooltips = (alt.Chart(reading_df).mark_rule().encode(x="yearmonthdate(date)", y="amount", opacity = alt.condition(hover, alt.value(0.3), alt.value(0)), tooltip = [alt.Tooltip("date", title = "Date"), alt.Tooltip("amount", title="Amount")]).add_params(hover))

data_layer = lines + points + tooltips

#Add annotations to the graph
ANNOTATIONS = []
complete_date = tablebase.select_completed_date(connection, user_id, "Yes")
#Add annotations for dates where the goal was completed for a habit
for date in complete_date:
    date = date[0]
    date = str(date)
    complete_amount = tablebase.select_completed_amount(connection, user_id, date, "Yes")
    for a in complete_amount:
        complete_amount = a[0]
    ANNOTATIONS.append((date, complete_amount, "👑", "Completed your goal!!!" ))
annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "amount", "marker", "description"])
annotations_df.date = pd.to_datetime(annotations_df.date)
#Scatter plot for annotations
annotation_layer = (
    alt.Chart(annotations_df).mark_text(size=20,dx=-10, dy=0, align="left",).encode(x="date:T", y=alt.Y("amount:Q"), text = "marker", tooltip="description")
)
combined_chart = data_layer + annotation_layer
#Check if user has logged in
if user_id:
    #Display chart
    st.altair_chart(combined_chart, use_container_width=True)
    st.write("For a better graph remember to track your habits everyday!")
else:
    #Direct user to log in 
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ERROR!!!")
        st.write("Please Log in or Sign up")
    with col2:
        with st.container(key="q"):
            st.page_link("login.py", label="Log in", icon="🪵")
        with st.container(key="w"):
            st.page_link("signup.py", label="Sign up", icon="🛑")