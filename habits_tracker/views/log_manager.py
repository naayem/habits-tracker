import pandas as pd
import streamlit as st
from datetime import date, timedelta


from habits_tracker.models.habits_model import HabitModel
from habits_tracker.models.logs_model import LogsModel
from habits_tracker.models.user_model import UserModel


def display_habit_logs_table(data):
    def transform_data(data):
        # Prepare a list to collect rows for the DataFrame
        rows = []

        for log_date, habits in data.items():
            for habit_name, habit_info in habits.items():
                value = habit_info['value']
                if habit_info['type'] == 'numeric':
                    value = float(value)
                elif habit_info['type'] == 'boolean':
                    value = 'X' if value else ' '
                rows.append({
                    'Date': log_date,
                    'Habit': habit_name,
                    'Value': value
                })

        # Create a DataFrame
        df = pd.DataFrame(rows)

        # Pivot the DataFrame to have dates as columns and habits as rows
        df_pivot = df.pivot(index='Habit', columns='Date', values='Value')

        return df_pivot

    # Transform the data
    df_pivot = transform_data(data)

    # Display the DataFrame in Streamlit
    st.title("Habit Logs Table")
    st.table(df_pivot)


class LogManager():
    def __init__(self, user_model: UserModel, habit_model: HabitModel, logs_model: LogsModel):
        self.habit_model = habit_model
        self.user_model = user_model
        self.logs_model = logs_model

    def test_retrieve_user_logs(self):
        USER_ID = self.user_model.get_user_id()
        st.title("Retrieve User Logs")
        start_date = st.date_input("Start Date", date.today() - timedelta(days=30))
        end_date = st.date_input("End Date", date.today())

        if st.button("Retrieve Logs"):
            try:
                user_logs = self.logs_model.retrieve_user_logs(USER_ID, start_date, end_date)
                st.write("User logs retrieved successfully!")
                display_habit_logs_table(user_logs)
            except Exception as e:
                st.error(f"Error retrieving user logs: {str(e)}")

    def test_create_single_log(self):
        st.title("Create Single Log")
        habits = self.habit_model.get_habits(self.user_model.get_user_id())
        habit_names = {habit["habit_name"]: habit["habit_id"] for habit in habits}
        selected_habit_name = st.selectbox("Select a habit", list(habit_names.keys()))
        selected_habit_id = habit_names[selected_habit_name]
        habit_id = st.write("Habit ID:", selected_habit_id)
        log_date = st.date_input("Log Date", date.today())
        log_value = st.number_input("Log Value", value=0.0)

        if st.button("Create Log"):
            try:
                self.logs_model.create_log_single(selected_habit_id, log_date, log_value)
                st.success(f"Log for habit '{habit_id}' on date '{log_date}' created successfully!")
            except Exception as e:
                st.error(f"Error creating log: {str(e)}")

    def log_page(self):
        self.test_retrieve_user_logs()
        self.test_create_single_log()
