import streamlit as st
import json
import pandas as pd

# Load the JSON data
with open('habits_log.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data)

# Replace True and False with custom symbols
df = df.replace({True: 'X', False: ''})

# CSS to wrap the text in the table cells
st.markdown(
    """
    <style>
    .dataframe td, .dataframe th {
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the table
st.dataframe(df)
