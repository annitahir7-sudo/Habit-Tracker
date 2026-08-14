import sqlite3
import bcrypt

CREATE_USER_TABLE = """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_name TEXT, password TEXT);""" #Maybe change password type
CREATE_HABITS_TABLE = """CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, frequency TEXT, goal INTEGER);"""
CREATE_COMPLETION_TABLE = """CREATE TABLE IF NOT EXISTS completion (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, habit TEXT, completed TEXT, amount INTEGER);""" # Change date type
INSERT_USER = """INSERT INTO users (user_name, password) VALUES (?, ?);"""
INSERT_HABITS = """INSERT INTO habits (user_id, name, frequency, goal) VALUES (?,?,?,?);"""
INSERT_PROGRESS = """INSERT INTO completion (user_id, date, habit, completed, amount) VALUES (?,?,?,?,?);"""
RETURN_USER_ID = """SELECT id FROM users WHERE user_name = ?;"""
CHECK_PASSWORD = """SELECT password FROM users WHERE user_name = ?;"""
SELECT_HABITS = """SELECT name from habits WHERE user_id = ?;"""
CHECK_USERNAME = """SELECT * FROM users WHERE user_name = ?;"""
RETURN_GOAL = """SELECT goal FROM habits WHERE user_id =? AND name = ?;"""
COMPLETED_DATE = """SELECT date FROM completion WHERE user_id = ? AND completed = ?"""
COMPLETED_AMOUNT = """SELECT amount FROM completion WHERE user_id = ? AND date = ? AND completed = ?"""




def connect():
    return sqlite3.connect("tracker.db")

#Create tables
def create_user_table(connection):
   with connection:
       connection.execute(CREATE_USER_TABLE)
def create_habits_table(connection):
    with connection:
        connection.execute(CREATE_HABITS_TABLE)
def create_completion_table(connection):
    with connection:
        connection.execute(CREATE_COMPLETION_TABLE)


#Hash  and check password
def hash_password(password):
    res = password.encode("utf-8")
    s = bcrypt.gensalt()
    h = bcrypt.hashpw(res, s)
    return h
def check_password(connection, user_name, password):
    with connection:
        hashed = connection.execute(CHECK_PASSWORD, (user_name,))
        hashed = hashed.fetchone()[0]
        return bcrypt.checkpw(password.encode("utf-8"), hashed)
    
#Check if the user has added any habits
def check_if_habits(connection, user_id):
    with connection:
        habits = connection.execute(SELECT_HABITS, (user_id,))
        habits = habits.fetchall()
        if habits:
            return True
        else:
            return False
#Return user id for use in the other functions (used to only select the habits, goal, amount.etc of that user and not another users)
def return_user_id (connection, user_name):
    with connection:
        result = connection.execute(RETURN_USER_ID, (user_name,))
        id = result.fetchone()
        id = id[0]
        return id
#Add new users to users tbale
def add_users(connection, user_name, password):
    with connection:
        connection.execute(INSERT_USER, (user_name, password))
#Add habits into habit table
def add_habits(connection, user_id, name, frequency, goal):
    with connection:
        connection.execute(INSERT_HABITS, (user_id, name, frequency, goal))
#Add progress to completion table
def add_progress(connection, user_id, date, habit, completed, amount):
    with connection:
        connection.execute(INSERT_PROGRESS, (user_id, date, habit, completed, amount))
#Show all habits user has added
def see_habits(connection, user_id):
    with connection:
        result = connection.execute(SELECT_HABITS, (user_id,))
        habits = result.fetchall()
        return habits
        
#Check if there is not another user with the same username
def check_username(connection, user_name):
    with connection:
        row = connection.execute(CHECK_USERNAME, (user_name,))
        row = row.fetchone()
        if row is not None:
            return True
        else:
            return False
#Return the goal a user set for a habit
def return_goal(connection, user_id, name):
    with connection:
        g = connection.execute(RETURN_GOAL, (user_id, name))
        g = g.fetchall()
        return g[0]
#Return the dates of the habits that were completed (the user had reached their goal for that habit on that day)
def select_completed_date(connection, user_id, completed="Yes"):
    with connection:
        complete_date = connection.execute(COMPLETED_DATE, (user_id, completed))
        complete_date = complete_date.fetchall()
        return complete_date
#Return the amount on the date the goal for a habit was achieved
def select_completed_amount(connection, user_id, date, completed = "Yes"):
    with connection:
        complete = connection.execute(COMPLETED_AMOUNT, (user_id, date, completed))
        complete = complete.fetchall()
        return complete
