import streamlit as st
from crontab import CronTab

# Initialize the current user's crontab
cron = CronTab(user=True)

# Function to list cron jobs
def list_cron_jobs():
    jobs = []
    for job in cron:
        jobs.append(str(job))
    return jobs

# Function to add a cron job
def add_cron_job(command, schedule):
    job = cron.new(command=f"{command} >> /var/log/cron.log 2>&1", comment=command)
    schedule_parts = schedule.split()
    job.setall(' '.join(schedule_parts[:5]))  # Setting schedule
    cron.write()
    st.success("Cron job added!")

# Function to remove a cron job
def remove_cron_job(command):
    jobs = cron.find_command(command)
    for job in jobs:
        cron.remove(job)
    cron.write()
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
