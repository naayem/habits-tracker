#!/bin/bash

# Start the cron service
service cron start

# Start Streamlit
streamlit run app.py
