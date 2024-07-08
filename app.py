from habits_tracker.config import MailClientConfig, HabitTrackerConfig
import streamlit as st
from habits_tracker.form_processor import FormProcessor


# Load configurations
habit_tracker_config = HabitTrackerConfig.from_env()
mail_client_config = MailClientConfig.from_env()

st.title("Contrat d'Habitudes Quotidiennes")

st.write("### Engagement à dire la vérité")
st.write("Je promets de dire la vérité, toute la vérité. Je dois assumer de ne pas avoir tenu mes habitudes. Chaque échec fait de moi quelqu'un d'un peu plus nul.")

agree = st.checkbox("Je m'engage à dire la vérité")

if agree:
    st.write("### Formulaire de Rapport Quotidien")
    FormProcessor.process_form(habit_tracker_config, mail_client_config)
