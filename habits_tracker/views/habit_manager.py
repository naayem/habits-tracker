import streamlit as st
from supabase import create_client

from habits_tracker.models.habits_model import HabitModel, SupabaseHabitModel
from habits_tracker.models.logs_model import SupabaseLogsModel
from habits_tracker.models.user_model import SupabaseUserModel, UserModel
from habits_tracker.views.authenticator import StreamlitAuthenticator


class HabitsManager:
    def __init__(self, habit_model: HabitModel, user_model: UserModel):
        self.habit_model = habit_model
        self.user_model = user_model

    def display_habits(self):
        st.write(f"Tracked Habits of {self.user_model.get_username()}")
        st.table(self.habit_model.get_habits(self.user_model.get_user_id()))
        if st.button("Refresh"):
            st.rerun()

    def add_habit(self):
        st.write("Add a new Habit to track")
        with st.form(key='add_habit_form'):
            habit_name = st.text_input("Habit Name")
            habit_type = st.selectbox("Habit Type", ["numeric", "boolean"])
            if st.form_submit_button("Add new habit"):
                result = self.habit_model.create_habit(self.user_model.get_user_id(), habit_name, habit_type)
                self.display_message(result)

    def update_habit(self):
        habits = self.habit_model.get_habits(self.user_model.get_user_id())
        habit_names = {habit["habit_name"]: habit["habit_id"] for habit in habits}
        selected_habit_name = st.selectbox("Select a habit to update", list(habit_names.keys()))
        selected_habit_id = habit_names[selected_habit_name]
        with st.form(key='update_habit_form'):
            habit_name = st.text_input("Habit Name", selected_habit_name)
            habit_type = st.selectbox("Habit Type", ["numeric", "boolean"])
            if st.form_submit_button("Update habit"):
                result = self.habit_model.update_habit(selected_habit_id, habit_name, habit_type)
                self.display_message(result)

    def delete_habit(self):
        habits = self.habit_model.get_habits(self.user_model.get_user_id())
        habit_names = {habit["habit_name"]: habit["habit_id"] for habit in habits}
        selected_habit_name = st.selectbox("Select a habit to delete", list(habit_names.keys()))
        selected_habit_id = habit_names[selected_habit_name]
        with st.form(key='delete_habit_form'):
            st.write("selected_habit_id:", selected_habit_id)
            if st.form_submit_button("Delete habit"):
                result = self.habit_model.delete_habit(selected_habit_id)
                self.display_message(result)

    def display_message(self, result):
        if result is None:
            st.success("Operation Success I guess (result = None)")
        elif result["status"] == "success":
            st.success(result["message"])
        else:
            st.error(result["message"])

    def habits_manager_page(self):
        self.display_habits()
        self.add_habit()
        self.update_habit()
        self.delete_habit()


@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase_client = init_connection()
logs_model = SupabaseLogsModel(supabase_client)
habits_model = SupabaseHabitModel(supabase_client)
user_model = SupabaseUserModel(supabase_client)
SA = StreamlitAuthenticator(user_model)
HM = HabitsManager(habits_model, user_model)

if __name__ == '__main__':
    SA.authenticator_sidebar()
    if user_model.get_user_id():
        HM.habits_manager_page()
