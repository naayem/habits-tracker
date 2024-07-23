import streamlit as st
from datetime import datetime, timedelta


from habits_tracker.models.habits_model import HabitModel
from habits_tracker.models.logs_model import LogsModel
from habits_tracker.models.user_model import UserModel


class LogHabitForm():
    def __init__(self, user_model: UserModel, habit_model: HabitModel, logs_model: LogsModel):
        self.habit_model = habit_model
        self.user_model = user_model
        self.logs_model = logs_model

    def log_habit_form(self):
        st.title("Log Habit Form")
        USER_ID = self.user_model.get_user_id()
        date_option = st.selectbox("Choisissez la date à loguer", ["Aujourd'hui", "Hier", "Un autre jour"])

        if date_option == "Un autre jour":
            log_date = st.date_input("Choisissez la date")
        else:
            log_date = datetime.now().date() if date_option == "Aujourd'hui" else datetime.now().date() - timedelta(days=1)

        form_data = {}
        existing_data = self.logs_model.retrieve_logs_for_date(USER_ID, log_date)

        with st.form(key='daily_habit_form'):
            habits = self.habit_model.get_habits(USER_ID)
            habit_types = [[habit["habit_id"], habit["habit_name"], habit["habit_type"]] for habit in habits]
            for habit_id, habit_name, habit_type in habit_types:
                if habit_name in existing_data:
                    default_value = existing_data.get(habit_name, {'value': False if habit_type == "boolean" else 0})['value']
                else:
                    default_value = False if habit_type == "boolean" else 0

                if habit_type == "boolean":
                    form_data[habit_id] = st.checkbox(habit_name, value=default_value)
                elif habit_type == "numeric":
                    form_data[habit_id] = st.number_input(habit_name, min_value=0, value=int(default_value))

            submitted = st.form_submit_button("Soumettre")
            if submitted:
                st.write(form_data)
                # Save the form data
                log_form = {log_date: {habit_id: form_data[habit_id] for habit_id in form_data}}
                try:
                    self.logs_model.create_logs_for_date(log_form)
                    st.success("Logs saved successfully!")
                    # Add email sending functionality here if required
                except Exception as e:
                    st.error(f"Error saving logs: {str(e)}")

    def form_page(self):
        st.write("### Engagement à dire la vérité")
        st.write("Je promets de dire la vérité, toute la vérité. Je dois assumer de ne pas avoir tenu mes habitudes. Chaque échec fait de moi quelqu'un d'un peu plus nul.")

        agree = st.checkbox("Je m'engage à dire la vérité")

        if agree:
            st.write("### Formulaire de Rapport Quotidien")
            self.log_habit_form()
