# app.py

import streamlit as st
from habits_tracker.penalty_checker import PenaltyChecker
from habits_tracker.form_processor import FormProcessor

st.title("Contrat d'Habitudes Quotidiennes")

st.write("### Engagement à dire la vérité")
st.write("Je promets de dire la vérité, toute la vérité. Je dois assumer de ne pas avoir tenu mes habitudes. Chaque échec fait de moi quelqu'un d'un peu plus nul.")

agree = st.checkbox("Je m'engage à dire la vérité")

if agree:
    st.write("### Formulaire de Rapport Quotidien")
    FormProcessor.process_form(st.session_state)

# Vérification des soumissions tardives
PenaltyChecker.check_late_submission(st.session_state)
PenaltyChecker.check_midnight_submission(st.session_state)
