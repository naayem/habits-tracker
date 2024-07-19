from datetime import date, datetime, timedelta
import pandas as pd
import streamlit as st
from supabase import create_client

# Assuming SupabaseLogsModel is defined in a module named `models`
from habits_tracker.models.logs_model import LogsModel, SupabaseLogsModel
from habits_tracker.models.habits_model import HabitModel, SupabaseHabitModel
from habits_tracker.models.user_model import SupabaseUserModel, UserModel
from habits_tracker.views.authenticator import StreamlitAuthenticator
from habits_tracker.views.habit_manager import HabitsManager


@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase_client = init_connection()
logs_model = SupabaseLogsModel(supabase_client)
habits_model = SupabaseHabitModel(supabase_client)
user_model = SupabaseUserModel(supabase_client)
st_auth = StreamlitAuthenticator(user_model)
habits_manager = HabitsManager(habits_model, user_model)

# Mock user ID for testing
USER_ID = user_model.get_user_id()


class LogHabitForm():
    def __init__(self, habit_model: HabitModel, user_model: UserModel, logs_model: LogsModel):
        self.habit_model = habit_model
        self.user_model = user_model
        self.logs_model = logs_model

    def log_habit_form(self):
        st.title("Log Habit Form")
        date_option = st.selectbox("Choisissez la date à loguer", ["Aujourd'hui", "Hier", "Un autre jour"])

        if date_option == "Un autre jour":
            log_date = st.date_input("Choisissez la date")
        else:
            log_date = datetime.now().date() if date_option == "Aujourd'hui" else datetime.now().date() - timedelta(days=1)

        form_data = {}
        existing_data = self.logs_model.retrieve_logs_for_date(USER_ID, log_date)

        with st.form(key='daily_habit_form'):
            habits = habits_model.get_habits(USER_ID)
            habit_types = {habit["habit_name"]: habit["habit_type"] for habit in habits}
            for habit_name, habit_type in habit_types.items():
                if habit_name in existing_data:
                    default_value = existing_data.get(habit_name, {'value': False if habit_type == "boolean" else 0})['value']
                else:
                    default_value = False if habit_type == "boolean" else 0

                if habit_type == "boolean":
                    form_data[habit_name] = st.checkbox(habit_name, value=default_value)
                elif habit_type == "numeric":
                    form_data[habit_name] = st.number_input(habit_name, min_value=0, value=int(default_value))

            submitted = st.form_submit_button("Soumettre")
            if submitted:
                # Save the form data
                log_form = {log_date: {habit_name: form_data[habit_name] for habit_name in form_data}}
                try:
                    self.logs_model.create_logs_for_date(log_form)
                    st.success("Logs saved successfully!")
                    # Add email sending functionality here if required
                except Exception as e:
                    st.error(f"Error saving logs: {str(e)}")


def main():
    st.sidebar.title("Test SupabaseLogsModel")
    st_auth.authenticator_sidebar()

    page = None
    if user_model.get_user_id():
        page = st.sidebar.selectbox("Select Functionality to Test", [
            "Habits Manager",
            "Create Single Log",
            "Create Logs for Date",
            "Retrieve Logs for Date",
            "Retrieve User Logs",
            "Log Habit Form"
        ])

    if page == "Habits Manager":
        habits_manager.habits_manager_page()
    elif page == "Create Single Log":
        display_habits()
        test_create_single_log()
    elif page == "Create Logs for Date":
        test_create_logs_for_date()
    elif page == "Retrieve Logs for Date":
        test_retrieve_logs_for_date()
    elif page == "Retrieve User Logs":
        test_retrieve_user_logs()
    elif page == "Log Habit Form":
        process_form()


def display_habits():
    st.write("Tracked Habits")
    st.write(supabase_client.auth.get_user().user.id)
    st.table(habits_model.get_habits(supabase_client.auth.get_user().user.id))
    if st.button("Refresh"):
        st.rerun()


def test_create_single_log():
    st.title("Create Single Log")
    habits = habits_model.get_habits(supabase_client.auth.get_user().user.id)
    habit_names = {habit["habit_name"]: habit["habit_id"] for habit in habits}
    selected_habit_name = st.selectbox("Select a habit", list(habit_names.keys()))
    selected_habit_id = habit_names[selected_habit_name]
    habit_id = st.write("Habit ID:", selected_habit_id)
    log_date = st.date_input("Log Date", date.today())
    log_value = st.number_input("Log Value", value=0.0)

    if st.button("Create Log"):
        try:
            logs_model.create_log_single(selected_habit_id, log_date, log_value)
            st.success(f"Log for habit '{habit_id}' on date '{log_date}' created successfully!")
        except Exception as e:
            st.error(f"Error creating log: {str(e)}")


def test_create_logs_for_date():
    st.title("Create Logs for Date")
    log_date = st.date_input("Log Date", date.today())

    num_habits = st.number_input("Number of Habits", min_value=1, value=1)
    log_form = {}

    for i in range(num_habits):
        habit_id = st.text_input(f"Habit ID {i+1}", key=f"habit_id_{i}")
        log_value = st.number_input(f"Log Value {i+1}", value=0.0, key=f"log_value_{i}")
        log_form.setdefault(log_date, {})[habit_id] = log_value

    if st.button("Create Logs"):
        try:
            logs_model.create_logs_for_date(log_form)
            st.success(f"Logs for date '{log_date}' created successfully!")
        except Exception as e:
            st.error(f"Error creating logs: {str(e)}")


def test_retrieve_logs_for_date():
    st.title("Retrieve Logs for Date")
    log_date = st.date_input("Log Date", date.today())
    form_data = {}
    if st.button("Retrieve Logs"):
        try:
            date_logs = logs_model.retrieve_logs_for_date(USER_ID, log_date)
            st.write(date_logs)
            for log in date_logs:
                if date_logs[log]["type"] == "boolean":
                    form_data[log] = st.checkbox(log, value=bool(date_logs[log]["value"]))
                elif date_logs[log]["type"] == "numeric":
                    form_data[log] = st.number_input(log, min_value=0.0, value=date_logs[log]["value"], step=1.0)
            st.write("Logs retrieved successfully!")
            st.json(date_logs)
        except Exception as e:
            st.error(f"Error retrieving logs: {str(e)}")


def test_retrieve_user_logs():
    st.title("Retrieve User Logs")
    start_date = st.date_input("Start Date", date.today() - timedelta(days=30))
    end_date = st.date_input("End Date", date.today())

    if st.button("Retrieve Logs"):
        try:
            user_logs = logs_model.retrieve_user_logs(USER_ID, start_date, end_date)
            st.write("User logs retrieved successfully!")
            st.write(user_logs)
            display_habit_logs_table(user_logs)
        except Exception as e:
            st.error(f"Error retrieving user logs: {str(e)}")


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
    st.dataframe(df_pivot)


logHabitForm = LogHabitForm(user_model, habits_model, logs_model)


def process_form():
    logHabitForm.log_habit_form()


if __name__ == "__main__":
    main()
