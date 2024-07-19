from supabase import create_client
from habits_tracker.config import MailClientConfig, HabitTrackerConfig, SupabaseConfig
from habits_tracker.models.habits_model import SupabaseHabitModel
from habits_tracker.models.logs_model import SupabaseLogsModel
from habits_tracker.models.user_model import SupabaseUserModel
from habits_tracker.utils import load_env_from_yaml
import streamlit as st
from habits_tracker.views.authenticator import StreamlitAuthenticator
from habits_tracker.views.habit_manager import HabitsManager
from habits_tracker.views.log_habit_form import LogHabitForm
from habits_tracker.views.log_manager import LogManager


# Load environment variables from YAML
load_env_from_yaml(".secrets.yaml")

# Load configurations
habit_tracker_config = HabitTrackerConfig.from_env()
mail_client_config = MailClientConfig.from_env()
supabase_config = SupabaseConfig.from_env()


@st.cache_resource
def init_connection():
    url = supabase_config.SUPABASE_URL
    key = supabase_config.SUPABASE_KEY
    return create_client(url, key)


supabase_client = init_connection()
log_model = SupabaseLogsModel(supabase_client)
habit_model = SupabaseHabitModel(supabase_client)
user_model = SupabaseUserModel(supabase_client)
st_auth = StreamlitAuthenticator(user_model)
habits_manager = HabitsManager(habit_model, user_model)
logHabitForm = LogHabitForm(user_model, habit_model, log_model)
logManager = LogManager(user_model, habit_model, log_model)

st.title("Contrat d'Habitudes Quotidiennes")

st_auth.authenticator_sidebar()

page = None
if user_model.get_user_id():
    page = st.sidebar.selectbox("Select Functionality to Test", [
        "Habits Manager",
        "User Logs",
        "Log Habit Form"
    ])

if page == "Habits Manager":
    habits_manager.habits_manager_page()
elif page == "User Logs":
    logManager.log_page()
elif page == "Log Habit Form":
    logHabitForm.form_page()

# FormProcessor.process_form(habit_tracker_config, mail_client_config)
