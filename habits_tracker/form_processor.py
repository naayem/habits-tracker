import streamlit as st
from datetime import datetime, timedelta
import json
from .config import HABITS, LOG_FILE, PENALTY_AMOUNT
from .email_service import EmailService


class FormProcessor:
    @staticmethod
    def process_form(session_state):
        date_option = st.selectbox("Choisissez la date à loguer", ["Aujourd'hui", "Hier", "Un autre jour"])

        if date_option == "Un autre jour":
            log_date = st.date_input("Choisissez la date")
        else:
            log_date = datetime.now().date() if date_option == "Aujourd'hui" else datetime.now().date() - timedelta(days=1)

        form_data = {}
        existing_data = FormProcessor.load_existing_data(log_date)

        with st.form(key='daily_habit_form'):
            for habit, habit_type in HABITS.items():
                if habit in existing_data:
                    default_value = existing_data[habit]
                else:
                    default_value = False if habit_type == "boolean" else 0

                if habit_type == "boolean":
                    form_data[habit] = st.checkbox(habit, value=default_value)
                elif habit_type == "number":
                    form_data[habit] = st.number_input(habit, min_value=0, value=default_value)

            submitted = st.form_submit_button("Soumettre")

            if submitted:
                FormProcessor.log_data(log_date, form_data)
                total_penalty = FormProcessor.calculate_penalty(form_data)
                st.metric(total_penalty)
                message = FormProcessor.generate_report_message(log_date, form_data, total_penalty)
                EmailService.send_email("Rapport quotidien soumis", message)
                st.success("Rapport soumis avec succès")

    @staticmethod
    def load_existing_data(log_date):
        try:
            with open(LOG_FILE, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        log_date_str = log_date.strftime("%Y-%m-%d")
        return data.get(log_date_str, {})

    @staticmethod
    def log_data(log_date, form_data):
        try:
            with open(LOG_FILE, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        log_date_str = log_date.strftime("%Y-%m-%d")
        data[log_date_str] = form_data

        with open(LOG_FILE, "w") as file:
            json.dump(data, file, indent=4)

    # ! Dummy Penalty
    @staticmethod
    def calculate_penalty(form_data):
        total_penalty = 0
        for habit, value in form_data.items():
            if isinstance(value, bool) and not value:
                total_penalty += PENALTY_AMOUNT
            elif isinstance(value, int) and value == 0:
                total_penalty += PENALTY_AMOUNT
        return total_penalty

    @staticmethod
    def generate_report_message(log_date, form_data, total_penalty):
        message = f"Rapport quotidien pour le {log_date}:\n"
        for habit, value in form_data.items():
            message += f"- {habit}: {'Oui ' + value if value else 'Non' if isinstance(value, bool) else value}\n"
        message += f"\nPénalité totale: {total_penalty} CHF"
        return message
