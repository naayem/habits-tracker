import streamlit as st
import os


# Function to list cron jobs
def list_cron_jobs():
    try:
        with open("/etc/cron.d/my-cron-job", "r") as cron_file:
            return cron_file.readlines()
    except FileNotFoundError:
        return []


# Funct
# ion to add a cron job
def add_cron_job(command, schedule):
    cron_job = f"{schedule} {command} >> /var/log/cron.log 2>&1"
    with open("/etc/cron.d/my-cron-job", "a") as cron_file:
        cron_file.write(cron_job + "\n")
    os.system("service cron reload")
    st.success("Cron job added!")


# Function to remove a cron job
def remove_cron_job(command):
    with open("/etc/cron.d/my-cron-job", "r") as cron_file:
        lines = cron_file.readlines()
    with open("/etc/cron.d/my-cron-job", "w") as cron_file:
        for line in lines:
            if command not in line:
                cron_file.write(line)
    os.system("service cron reload")
    st.success("Cron job removed!")


# Function to read cron log
def read_cron_log():
    try:
        with open("/var/log/cron.log", "r") as log_file:
            return log_file.read()
    except FileNotFoundError:
        return "Cron log file not found."


# Streamlit UI
st.title("Cron Job Manager")

st.header("Current Cron Jobs")
cron_jobs = list_cron_jobs()
if cron_jobs:
    for job in cron_jobs:
        st.text(job.strip())
else:
    st.text("No cron jobs found.")

st.header("Add Cron Job")
st.write("0 9 * * * python /app/task_9am.py")

schedule = st.text_input("Schedule (e.g., '* * * * *' for every minute)")
command = st.text_input("Command (e.g., 'python /path/to/script.py')")
if st.button("Add Cron Job"):
    add_cron_job(command, schedule)

st.header("Remove Cron Job")
remove_command = st.text_input("Command to Remove (exact match)")
if st.button("Remove Cron Job"):
    remove_cron_job(remove_command)

st.header("Cron Job Log")
if st.button("Refresh Log"):
    cron_log = read_cron_log()
    st.text_area("Cron Log", cron_log, height=200)
else:
    cron_log = read_cron_log()
    st.text_area("Cron Log", cron_log, height=200)
