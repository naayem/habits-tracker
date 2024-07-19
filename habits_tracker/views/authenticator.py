import streamlit as st
from habits_tracker.models.user_model import UserModel


class StreamlitAuthenticator():
    def __init__(self, user_model: UserModel):
        self.user_model = user_model

    def authenticator_sidebar(self):
        if st.sidebar.checkbox('Register'):
            st.sidebar.subheader("Register")
            email = st.sidebar.text_input("Email")
            password = st.sidebar.text_input("Password", type='password')
            username = st.sidebar.text_input("username")
            if st.sidebar.button("Register"):
                response = self.user_model.signup(email, password, username)
                st.sidebar.success("User registered successfully!") if response.get('user') else st.sidebar.error("Error: " + response['error'])

        # Login form
        if st.sidebar.checkbox('Login'):
            st.sidebar.subheader("Login")
            email = st.sidebar.text_input("Email", key='login_email')
            password = st.sidebar.text_input("Password", type='password', key='login_password')
            if st.sidebar.button("Login"):
                response = self.user_model.login(email, password)
                if response.user.aud == "authenticated":
                    st.sidebar.success("Logged in successfully!")
                    st.sidebar.write(self.user_model.get_user_id())
                    st.session_state['user'] = self.user_model.get_user_id()
                else:
                    st.sidebar.error("Error: " + response)
