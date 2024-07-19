from supabase import Client
from abc import ABC, abstractmethod


class UserModel(ABC):
    @abstractmethod
    def signup(self, email: str, password: str) -> None:
        pass

    @abstractmethod
    def login(self, email: str, password: str) -> dict:
        pass

    @abstractmethod
    def get_user_id(self):
        pass

    @abstractmethod
    def get_username(self):
        pass


class SupabaseUserModel(UserModel):
    def __init__(self, supabase_client: Client):
        self.client: Client = supabase_client

    def signup(self, email: str, password: str) -> None:
        self.client.auth.sign_up({"email": email, "password": password})

    def login(self, email: str, password: str) -> dict:
        return self.client.auth.sign_in_with_password({"email": email, "password": password})

    def get_user_id(self):
        if self.client.auth.get_user():
            return self.client.auth.get_user().user.id
        else:
            return self.client.auth.get_user()

    def get_username(self):
        if self.client.auth.get_user():
            return self.client.auth.get_user().user.user_metadata.get('username')
        else:
            return self.client.auth.get_user()
