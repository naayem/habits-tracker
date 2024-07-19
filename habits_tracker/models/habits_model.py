from uuid import UUID
from supabase import Client
from abc import ABC, abstractmethod


class HabitModel(ABC):
    @abstractmethod
    def create_habit(self, user_id: UUID, name: str, type: str) -> None:
        pass

    @abstractmethod
    def get_habits(self, user_id: UUID) -> list:
        pass

    @abstractmethod
    def update_habit(self, habit_id: int, name: str, type: str) -> None:
        pass

    @abstractmethod
    def delete_habit(self, habit_id: int) -> None:
        pass


class SupabaseHabitModel(HabitModel):
    def __init__(self, supabase_client: Client):
        self.client: Client = supabase_client

    def create_habit(self, user_id: UUID, name: str, type: str) -> None:
        self.client.table('habits').insert({"user_id": user_id, "habit_name": name, "habit_type": type}).execute()

    def get_habits(self, user_id: UUID) -> list:
        response = self.client.table('habits').select("*").eq("user_id", user_id).execute()
        return response.data

    def update_habit(self, habit_id: int, name: str, type: str) -> None:
        self.client.table('habits').update({"habit_name": name, "habit_type": type}).eq('habit_id', habit_id).execute()

    def delete_habit(self, habit_id: int) -> None:
        self.client.table('habits').delete().eq('habit_id', habit_id).execute()
